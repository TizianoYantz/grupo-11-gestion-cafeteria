import mysql.connector

def conectar():

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cafeteria"
    )

    return conexion