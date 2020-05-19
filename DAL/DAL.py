import mysql.connector
from mysql.connector import MySQLConnection, Error

import config
class DAL():

    def __init__(self):
        pass

    def getConnection(self):
        sql_conn = config.mysql
        try:
            mydb = mysql.connector.connect(
                host=sql_conn['host'],
                user=sql_conn['user'],
                passwd=sql_conn['passwd'],
                database=sql_conn['database']
            )
        except:
            print("connection error")
        return mydb

    def changeBlockStatus(self,status):
        try:
            mydb = self.getConnection()
            mycursor = mydb.cursor()
            sql = "UPDATE camera_block SET block = {0} WHERE id = 1".format(status)

            mycursor.execute(sql)

            mydb.commit()
        except Error as error:
            print(error)
            return False
        finally:
            mycursor.close()
            mydb.close()
            return True