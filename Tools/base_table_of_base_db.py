import pymysql

with pymysql.connect(host="localhost", user="root", passwd="", port=3306) as conn:
    cur = conn.cursor()
    cur.execute('SHOW DATABASES')
    databases = cur.fetchall()
    for db_t in databases:
        db = db_t[0]
        cur.execute('USE %s' % db)
        cur.execute('SHOW TABLES')
        tables = cur.fetchall()
        for tab_t in tables:
            tab = tab_t[0]
            cur.execute('SELECT COUNT(1) FROM %s' % tab)
            result = cur.fetchone()
            if result:
                print('%s %s %s' % (db, tab, result))
