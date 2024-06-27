# Install Mysql on computer
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python
import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1029384756'
)

# prepare a cursor object
cursorObject = database.cursor()

# Create a dataBase
cursorObject.execute("CREATE DATABASE dbkiki")
# indicator
print("done")
