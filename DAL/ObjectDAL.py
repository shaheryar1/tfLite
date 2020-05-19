import mysql.connector
from mysql.connector import MySQLConnection, Error
import config
from DAL.DAL import DAL
from DTO.Object_DTO import ObjectDTO
class ObjectDAL(DAL):


    def insertObject(self, dto):

        try:
            mydb = self.getConnection()
            mycursor = mydb.cursor()
            sql = "INSERT INTO objects  (object_id,name,price,status) " \
                                                         "VALUES (%s,%s,%s,%s)"
            val = (dto.object_id, dto.name,dto.price,dto.status)
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



