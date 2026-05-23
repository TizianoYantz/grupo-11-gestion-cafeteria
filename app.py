from flask import Flask, render_template, request, redirect
from database import conectar

app = Flask(__name__)

# Ruta principal → Home
@app.route("/")
def home():
    return render_template("home.html")

# Inventario → conecta con la base
@app.route("/inventario")
def inventario():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return render_template("index.html", productos=productos)

# Crear producto
@app.route("/crear", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO productos
        (nombre, categoria, precio, stock, disponible)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, categoria, precio, stock, True)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        return redirect("/inventario")

    return render_template("crear_producto.html")

# Editar producto
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        sql = """
        UPDATE productos
        SET nombre = %s,
            categoria = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        """
        valores = (nombre, categoria, precio, stock, id)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        return redirect("/inventario")

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return render_template("editar_producto.html", producto=producto)

# Eliminar producto
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()
    return redirect("/inventario")

# Vender producto
@app.route("/vender/<int:id>", methods=["POST"])
def vender_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT stock FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    stock_actual = producto[0]

    if stock_actual > 0:
        nuevo_stock = stock_actual - 1
        cursor.execute(
            "UPDATE productos SET stock = %s WHERE id = %s",
            (nuevo_stock, id)
        )
        conexion.commit()

    conexion.close()
    return redirect("/inventario")
