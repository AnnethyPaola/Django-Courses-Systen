import mysql.connector;

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Annethy2514",
#  database="coursesdb"
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE coursesdb")
print("ALL DONE!")
