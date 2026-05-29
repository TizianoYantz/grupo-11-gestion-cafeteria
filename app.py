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
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        nuevo_producto = Producto(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
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
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        producto = Producto(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
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

@app.route("/venta", methods=["GET", "POST"])
def venta():

    if request.method == "POST":

        producto_id = int(request.form["producto_id"])
        cantidad = int(request.form["cantidad"])

        producto = Producto.obtener_producto(producto_id)

        if producto.stock < cantidad:
            return "Stock insuficiente"

        venta = Venta()

        venta.agregar_producto(producto, cantidad)

        producto.stock -= cantidad

        producto.editar_producto(producto_id)

        return redirect("/inventario")

    productos = Inventario.listar_productos()

    return render_template(
        "venta.html",
        productos=productos
    )

app.run(debug=True)
