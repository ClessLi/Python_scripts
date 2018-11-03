from MySQL.db_base import DB, getConfig


dbconfig = getConfig()


'''
向数据库插入单条数据
model = Model('test')
data = {"user_name":"stevegao","password" : "444444",'create_time':"2017-02-12 09:12:12", 'login_times' : "1"}
insert = model.table('ly_user').insert(data)
if (insert) :
    model.db.link.commit(); //提交事务
else :
    model.db.link.rollback(); //回滚事务
'''


class Model:
    lastsql = ''
    _wherestr = ''
    _orderstr = ''
    _groupstr = ''
    _limitstr = ''
    _fieldstr = ''
    _tablename = ''
    _having = ''
    _host = ""

    db = {}

    def __init__(self, host="master"):
        self._host = host
        mysql = DB(host.lower())  # 实例化数据库类
        self.db[self._host] = mysql

    def max(self, field):
        sql = self._parseStatis('max', field)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def min(self, field):
        sql = self._parseStatis('min', field)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def avg(self, field):
        sql = self._parseStatis('avg', field)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def count(self, field):
        sql = self._parseStatis('count', field)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def sum(self, field):
        sql = self._parseStatis('sum', field)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def table(self, tablename):
        pconfig = getConfig()
        prefix = pconfig[self._host]['write']['dbprefix']
        self._tablename = "`" + prefix + tablename + "`"
        return self

    def where(self, where=""):
        if (where):
            self._wherestr = self._parseWhereDict(where)
        else:
            self._wherestr = where
        return self

    def orderBy(self, order=""):
        self._orderstr = order
        return self

    def groupBy(self, groupby=""):
        self._groupstr = groupby
        return self

    def having(self, having=""):
        self._having = having
        return self

    def limit(self, limit=""):
        self._limitstr = limit
        return self

    def field(self, field="*"):
        self._fieldstr = field
        return self

    def select(self):
        sql = self._parseQuery()
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def find(self):
        sql = self._parseQuery(1)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql, 's')
        return result

    def query(self, sql):
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    '''
    插入单条数据，data类型为字典型
    '''

    def insert(self, data):
        sql = self._parseInsert(data)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    '''
    批量插入数据，data类型为字典型
    '''

    def insertAll(self, data):
        sql = self._parseInsertAll(data)
        if (sql == False):
            return sql
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql)
        return result

    def delete(self):
        sql = self._parseDelete()
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql, 's')
        return result

    def update(self, data):
        sql = self._parseSetDict(data)
        self.lastsql = sql
        result = self.db[self._host].executeSql(sql, 's')
        return result

    '''
    提交事务
    '''

    def commit(self):
        self.db[self._host].commit()

    '''
    提交回滚
    '''

    def rollback(self):
        self.db[self._host].rollback()

    '''
    解析查询语句
    '''

    def _parseQuery(self, limit=2):
        tempsql = "SELECT "
        if (self._fieldstr):
            tempsql += self._fieldstr
        else:
            tempsql += "*"
        tempsql += " FROM "

        if (self._tablename):
            tempsql += self._tablename

        if (self._wherestr):
            tempsql += " WHERE "
            tempsql += self._wherestr

        tempsql += " "

        if (self._groupstr):
            tempsql += " GROUP BY "
            tempsql += self._groupstr

        if (self._having):
            tempsql += " HAVING "
            tempsql += self._having

        if (self._orderstr):
            tempsql += " ORDER BY "
            tempsql += self._orderstr
        tempsql += " "

        if (limit == 2):
            if (self._limitstr):
                tempsql += " LIMIT "
                tempsql += self._limitstr
        else:
            tempsql += " LIMIT 1"

        return tempsql

    def _parseInsert(self, data):
        tinsert = ""
        tinsert += "INSERT INTO "

        if (self._tablename):
            tinsert += self._tablename

        fieldList = ' ('
        valueList = ' ('
        for field in data:
            fieldList += "`" + field + "`,"
            valueList += '"' + data[field] + '",'
        fieldList = fieldList[0:-1] + ") "
        valueList = valueList[0:-1] + ") "
        sql = tinsert + fieldList + "values " + valueList
        return sql

    def _parseInsertAll(self, data):
        if (data.get(0) == None):
            return False
        tinsert = ""
        tinsert += "INSERT INTO "
        if (self._tablename):
            tinsert += "`" + self._tablename + "`"
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

        sql = tinsert + fieldList + "VALUES " + values[0:-1]
        return sql

    '''
        解析查询语句
        '''

    def _parseStatis(self, func, field):
        tempsql = "SELECT "
        if (field):
            tempsql += func + "(" + field + ")"
        else:
            tempsql += func + "(" + '1' + ")"
        tempsql += " FROM "

        if (self._tablename):
            tempsql += self._tablename

        if (self._wherestr):
            tempsql += " WHERE "
            tempsql += self._wherestr

        tempsql += " "

        if (self._groupstr):
            tempsql += " GROUP BY "
            tempsql += self._groupstr

        if (self._having):
            tempsql += " HAVING "
            tempsql += self._having

        if (self._orderstr):
            tempsql += " ORDER BY "
            tempsql += self._orderstr
        tempsql += " "
        if (self._groupstr == ""):
            tempsql += " LIMIT 1"

        return tempsql

    def _parseDelete(self):

        tempsql = "DELETE "
        tempsql += " FROM "

        if (self._tablename):
            tempsql += self._tablename

        if (self._wherestr):
            tempsql += " WHERE "
            tempsql += self._wherestr

        tempsql += " "

        if (self._orderstr):
            tempsql += " ORDER BY "
            tempsql += self._orderstr
        tempsql += " "

        if (self._limitstr):
            tempsql += " LIMIT "
            tempsql += self._limitstr

        return tempsql

    def _parseUpdate(self, data):

        if (not data):
            return False

        tempsql = "UPDATE "

        if (self._tablename):
            tempsql += self._tablename

        tempsql += " SET "

        tempsql += self._parseSetDict(data)

        if (self._wherestr):
            tempsql += " WHERE "
            tempsql += self._wherestr

        tempsql += " "

        if (self._orderstr):
            tempsql += " ORDER BY "
            tempsql += self._orderstr
        tempsql += " "

        if (self._limitstr):
            tempsql += " LIMIT "
            tempsql += self._limitstr

        return tempsql

    def _parseSetDict(self, data):
        if (isinstance(data, dict)):
            temp = ""
            for field in data:
                temp += '`' + field + '` = "' + data[field] + '",'
            result = temp[0:-1]
        else:
            result = data
        return result

    def _parseWhereDict(self, data):
        if (isinstance(data, dict)):
            temp = ""
            for field in data:
                temp += '`' + field + '` = "' + data[field] + '" AND '
            result = temp.rstrip()[0:-3]
        else:
            result = data
        return result


if __name__ == '__main__':
    model = Model('test')
    data = {"user_name": "ClessLee", "password": "Mint", 'create_time': "2018-11-3 11:35:28", 'login_times': "1"}
    insert = model.table('test1').insert(data)
    if (insert):
        print(model.db)
        model.commit() #提交事务
    else:
        model.rollback() #回滚事务