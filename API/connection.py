import MySQLdb

class MyDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.init_connection_and_cursor()

    def execQuery(self, query, params):
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        if not result:
            result = self.cursor.lastrowid
        self.connection.commit()
        return result

    def init_connection_and_cursor(self):
        if not self.connection or not self.connection.open:
            self.connection = MySQLdb.connect(host='localhost', port=3306, db='myDB11',
                         user='root', passwd='123',
                         charset='utf8')
            self.cursor = self.connection.cursor()

db1 = MyDatabase()

db_connection = MySQLdb.connect(host='localhost', port=3306, db='myDB11',
                         user='root', passwd='123',
                         charset='utf8')

def connect():
    db_connection1 = db_connection
    return db_connection1

def execQuery(query, params):
    try:
        result = db1.execQuery(query, params)
        #connection = connect()
        #with connection:
        #    cursor = connection.cursor()
        #    cursor.execute(query, params)
        #    result = cursor.fetchall()
        #    cursor.close()
        #connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Select error")
    return result



