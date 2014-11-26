import MySQLdb

def connect():
     return MySQLdb.connect(host='localhost', port=3306, db='myDB1',
                         user='root', passwd='123',
                         charset='utf8')

def execQuery(query, params):
    connection = None
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        if not result:
            result = cursor.lastrowid
        connection.commit()
    except Exception as e:
        raise Exception({"code":"UNKNOWN ERROR","message":str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return result



