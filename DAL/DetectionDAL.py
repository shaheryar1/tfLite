import mysql.connector
from mysql.connector import MySQLConnection, Error
import config
from DAL.DAL import DAL
from DTO.Detection_DTO import DetectionDTO
class DetectionDAL(DAL):


    def __init__(self):
        pass



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
            return True
