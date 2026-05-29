from flask import Flask, render_template, request, redirect
from database import conectar
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.inventario import Inventario

app = Flask(__name__)

# HOME como pantalla inicial
@app.route("/")
def home():
    return render_template("Home.html")

# CREAR PRODUCTO
@app.route("/crear", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        nuevo_producto = Producto(
            nombre,
            categoria,
            precio,
            stock
        )
        nuevo_producto.crear_producto()
        return redirect("/inventario")

    return render_template("crear_producto.html")

# INVENTARIO
@app.route("/inventario")
def inventario():
    productos = Producto.listar_productos()
    return render_template("Inventario.html", productos=productos)

# EDITAR PRODUCTO
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        producto = Producto(
            nombre,
            categoria,
            precio,
            stock
        )
        producto.editar_producto(id)
        return redirect("/inventario")

    producto = Producto.obtener_producto(id)
    return render_template("editar_producto.html", producto=producto)

# ELIMINAR PRODUCTO
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    Producto.eliminar_producto(id)
    return redirect("/inventario")

if __name__ == "__main__":
    app.run(debug=True)
