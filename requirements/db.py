# db.py
import pymysql

def connect_pymysql():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="cricbuzzdb"
    )
