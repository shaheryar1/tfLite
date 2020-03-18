import mysql.connector
from mysql.connector import MySQLConnection, Error
import config
from DTO.Detection_DTO import DetectionDTO
class DetectionDAL:
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

    def insertDetection(self, dto):

        try:
            mydb = self.getConnection()
            mycursor = mydb.cursor()
            sql = "INSERT INTO detections  (object_id,confidence) " \
                                                         "VALUES (%s,%s)"
            val = (dto.object_id,dto.confidence)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
            return True
        except Error as error:

            print(error)
            return False
        finally:
            mycursor.close()
            mydb.close()
