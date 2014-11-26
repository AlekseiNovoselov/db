from API.connection import connect
import MySQLdb

def clear(request):
    try:
        connection = connect()
        with connection:
            cursor = connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE Followers")
            cursor.execute("TRUNCATE TABLE Forums")
            cursor.execute("TRUNCATE TABLE Posts")
            cursor.execute("TRUNCATE TABLE Subscriptions")
            cursor.execute("TRUNCATE TABLE Threads")
            cursor.execute("TRUNCATE TABLE Users")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            cursor.close()
        connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Cant drop DataBase")
