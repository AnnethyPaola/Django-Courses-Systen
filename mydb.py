import mysql.connector;

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="**",
#  database="coursesdb"
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE coursesdb")
print("ALL DONE!")
