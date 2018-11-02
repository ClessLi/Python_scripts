import sys
import pymysql
import random
import json
try:
    with open('./DB_config.json', 'rb') as dbconfig:
        dbconfig = json.load(dbconfig)
except FileExistsError as err:
    print("FileERR数据库配置文件无效：  \n[%s]" % (err))
    exit()


class DB:
    link = dict()
    _res = ''
    _mode = "read"  # write,read
    _host = ''

    def __init__(self, dbconfig, host="master"):
        self._host = host
        self._dbconfig = dbconfig

    def connect(self, mode="read"):
        try:
            self._mode = mode
            self._dbconfig = self._dbconfig[self._host][self._mode]
            self.host = self._dbconfig['host']
            self.dbuser = self._dbconfig['dbuser']
            self.password = self._dbconfig['dbpwd']
            self.dbname = self._dbconfig['dbname']
            self.port = self._dbconfig['port']
            self._res = pymysql.cursors.DictCursor
            self.link[self._host] = pymysql.connect(self.host, self.dbuser, self.password, self.dbname, self.port)
        except Exception as err:
            print("DBERR数据库连接失败： \n[%s]" % (err))
            exit()

    def getTableName(self, tableName):
        return self._dbconfig['dbprefix'] + tableName

    '''
    查询单张表的一条记录
    '''

    def getOne(self, tableName, id):
        try:
            self.connect('read')
            tableName = self.getTableName(tableName)
            cursors = self.link[self._host].cursor(self._res)
            sql = "SELECT * FROM %s WHERE id = %d LIMIT 1"
            cursors.execute(sql % (tableName, int(id)))
            result = cursors.fetchone()
            return result
        except Exception as err:
            print("DBERR数据库查询单条记录失败： \n[%s]" % (err))
            exit()

    '''
    根据条件查询单表的内容
    '''

    def getCondition(self, tableName, condition=''):
        try:
            self.connect('read')
            cursors = self.link[self._host].cursor(self._res)
            tableName = self.getTableName(tableName)
            if (condition):
                sql = "SELECT * FROM %s WHERE %s"
                cursors.execute(sql % (tableName, condition))
            else:
                sql = "SELECT * FROM %s;"
                cursors.execute(sql % (tableName))

            result = cursors.fetchall()
            result = list(result)
            return result
        except Exception as err:
            print("DBERR数据库按条件查询记录失败： \n[%s]" % (err))
            exit()

    '''
    根据SQL语句查询
    '''

    def executeSql(self, sql, findOne='m'):
        try:
            sql = sql.lstrip()
            if (len(sql) == 0):
                return False

            operate = sql[0:6].upper()
            if (operate == "SELECT"):
                self._mode = 'read'
            elif (operate == 'INSERT' or operate == "UPDATE" or operate == 'DELETE'):
                self._mode = 'write'
            else:
                self._mode = 'write'

            self.connect(self._mode)
            cursors = self.link[self._host].cursor(self._res)

            execs = cursors.execute(sql)
            if (operate == "SELECT"):
                if ((findOne == 'm') and ("LIMIT 1" not in sql.upper())):
                    result = cursors.fetchall()
                else:
                    result = cursors.fetchone()
                return result
            else:
                return execs

        except Exception as err:
            print("DBERR数据库执行失败： \n[%s]" % (err))
            exit()

    '''
    使用字典插入单条数据
    link = DB('localhost','root','','liuyan')
    data = {"user_name":"stevegao","password" : "444444",'create_time':"2017-02-12 09:12:12", 'login_times' : "1"}
    link.insertAll('ly_user',data)
    '''

    def insert(self, table, data):
        try:
            self.connect('write')
            table = self.getTableName(table)
            tinsert = "INSERT INTO %s"
            fieldList = ' ('
            valueList = ' ('
            for field in data:
                fieldList += "`" + field + "`,"
                valueList += '"' + data[field] + '",'
            fieldList = fieldList[0:-1] + ") "
            valueList = valueList[0:-1] + ") "
            sql = tinsert + fieldList + "values " + valueList
            cursors = self.link[self._host].cursor(self._res)
            insert = cursors.execute(sql % (table))
            print(sql % (table))
            # self.link.commit()
            return insert
        except Exception as err:
            self.link.rollback()
            print("DBERR数据库插入单条记录失败：\n[%s]" % (err))
            exit()

    '''
    使用字典，批量插入数据到数据库
    link = DB('localhost','root','','liuyan')
    data = dict()
    data[0] = {"user_name":"stevegao","password" : "444444",'create_time':"2017-02-12 09:12:12", 'login_times' : "1"}
    data[1] = {"user_name":"jennygao","password" : "555555",'create_time':"2017-02-12 09:12:12", 'login_times' : "1"}
    ii = link.insertAll('ly_user',data)
    '''

    def insertAll(self, table, data):
        try:
            self.connect('write')
            table = self.getTableName(table)
            tinsert = "INSERT INTO %s"
            fieldList = ' ('
            values = ''
            oneField = data[0]
            for field in oneField:
                fieldList += "`" + field + "`,"
            fieldList = fieldList[0:-1] + ") "

            for row in data:
                valueList = '('
                for field in data[row]:
                    valueList += '"' + data[row][field] + '",'
                values += valueList[0:-1] + "),"

            sql = tinsert + fieldList + "values " + values[0:-1]
            cursors = self.link[self._host].cursor(self._res)
            insert = cursors.execute(sql % (table))
            # self.link.commit()
            return insert
        except Exception as err:
            self.link.rollback()
            print("DBERR数据库批量插入记录失败：\n[%s]" % (err))
            exit()

    def commit(self):
        self.link[self._host].commit()

    def rollback(self):
        self.link[self._host].rollback()

    '''
    关闭数据库链接
    '''

    def close(self):
        self.link[self._host].close()