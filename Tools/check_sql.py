#!/usr/bin/python3.6
import re, os, sys

def read_file(sql_file):
    if os.path.exists(sql_file):
        with open(sql_file, 'r', encoding='utf-8') as fp:
            return fp.readlines()
    else:
        return None

class parse_insert:

    def __init__(self, database, tables, sql_file, get_sql):
        self._db = database
        self._tabs = tables
        self._insert_flag = False
        self._re_db_flag = r'^\s*insert\s+into\s+`\S+`\.`\S+`\s*\('
        self._re_db = r'^\s*insert\s+into\s+`%s`\.`\S+`\s*\(' % self._db
        self._re_tabs = self.get_re_tables(self._tabs)
        self._re_insert_start = r'^\s*insert\s+into\s+'
        self._re_insert_end = r';'
        self._sql = get_sql(sql_file)
        self.sql = []
        self.parse_sql()

    def get_re_tables(self, tables):
        re_tabs = []
        for tab in tables:
            re_tabs.append(r'^(\s*insert\s+into\s+[^()]+`%s`\s+\()' % tab.strip('\n'))
        print(re_tabs)
        return re_tabs


    def parse_sql(self):
        def parse_insert_db(re_db_flag, sql, re_db, flag):
            if re.search(re_db_flag, sql, re.I | re.M):
                if not re.search(re_db, sql, re.I | re.M):
                    flag = True
                    sql = re.sub('^', '/*', sql, re.I|re.M)
            return sql, flag

        def parse_insert_start(re_insert_start, sql, re_tabs, flag):
            if re.search(re_insert_start, sql, re.I | re.M):
                for re_tab in re_tabs:
                    if re.search(re_tab, sql, re.I | re.M):
                        print(re_tab, sql)
                        return sql, flag
                flag = True
                sql = re.sub(r'^', '/*', sql, re.I | re.M)
            return sql, flag

        def parse_insert_end(re_insert_end, sql, flag):
            if re.search(re_insert_end, sql, re.I | re.M):
                flag = False
                return re.sub(self._re_insert_end, ';*/', sql, 1, re.I | re.M), flag
            else:
                return sql, flag

        if self._sql:
            for line in self._sql:
                sql = line
                if not self._insert_flag:
                    sql, self._insert_flag = parse_insert_db(self._re_db_flag,
                                                             sql,
                                                             self._re_db,
                                                             self._insert_flag)
                    print(sql)
                if not self._insert_flag:
                    sql, self._insert_flag = parse_insert_start(self._re_insert_start,
                                                                sql,
                                                                self._re_tabs,
                                                                self._insert_flag)
                    #print(sql)
                if self._insert_flag:
                    sql, self._insert_flag = parse_insert_end(self._re_insert_end,
                                                              sql,
                                                              self._insert_flag)
                self.sql.append(sql)


if __name__ == '__main__':
    #if len(sys.argv) != 3:
    #    print('Plz usage: %s <sql_file> <tables_file>')
    #    exit(1)
    sql_file = 'riskpotral-dml.sql'
    tables_file = 'riskportal'
    #sql_file = sys.argv[1]
    #save_sql_file = 'new.' + sql_file
    #tables_file = sys.argv[2]
    if os.path.exists(sql_file) and os.path.exists(tables_file):
        db_name = os.path.basename(tables_file)
        tables = read_file(tables_file)
        sql = parse_insert(db_name, tables, sql_file, read_file)
        #print(sql.sql)
        #with open(save_sql_file, 'w') as fp:
        #    fp.writelines(sql.sql)


