from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

class producto:
    def __init__(self,id,nombre,categoria,precio,stock,disponible=True):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.estado = disponible

    def vender(self, cantidad):
        if cantidad <= self.stock:
            self.stock -= cantidad
            return True
        return False
    
    def reponer_stock(self, cantidad):
        self.stock += cantidad

@app.route("/")
def index():

    conexion = sqlite3.connect("cafeteria.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()

    return render_template("index.html", productos=productos)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    conexion = sqlite3.connect("cafeteria.db")
    cursor = conexion.cursor()

    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        cursor.execute("""
        UPDATE productos
        SET nombre = ?, categoria = ?, precio = ?, stock = ?
        WHERE id = ?
        """, (nombre, categoria, precio, stock, id))

        conexion.commit()
        conexion.close()

        return redirect("/")

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()

    conexion.close()

    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conexion = sqlite3.connect("cafeteria.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

    conexion.commit()
    conexion.close()

    return redirect("/")

app.run(debug=True)