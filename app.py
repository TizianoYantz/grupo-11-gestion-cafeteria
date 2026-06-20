from flask import Flask, render_template, request, redirect
import json
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.reporte import Reporte   

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Home.html")


# ---------------- INVENTARIO ----------------

@app.route("/crear", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        categoria = request.form["categoria"].strip().title()
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

@app.route("/inventario")
def inventario():

    productos = Producto.listar_productos()
    categorias = Producto.obtener_categorias()

    buscar = request.args.get("buscar", "")
    categoria = request.args.get("categoria", "")
    orden = request.args.get("orden", "")

    # Buscar por nombre
    if buscar:
        productos = [
            p for p in productos
            if buscar.lower() in p[1].lower()
        ]

    # Filtrar categoría
    if categoria:
        productos = [
            p for p in productos
            if p[2].strip().lower() == categoria.strip().lower()
        ]

    # Ordenar
    if orden == "nombre":
        productos.sort(key=lambda p: p[1].lower())

    elif orden == "precio_asc":
        productos.sort(key=lambda p: float(p[3]))

    elif orden == "precio_desc":
        productos.sort(
            key=lambda p: float(p[3]),
            reverse=True
        )

    return render_template(
        "Inventario.html",
        productos=productos,
        categorias=categorias
    )
    
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    if request.method == "POST":

        print("ENTRO AL POST")

        nombre = request.form["nombre"].strip()
        categoria = request.form["categoria"].strip().title()
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        print(nombre, categoria, precio, stock)

        producto = Producto(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
        )

        producto.editar_producto(id)

        print("PRODUCTO ACTUALIZADO")

        return redirect("/inventario")

    producto = Producto.obtener_producto(id)

    return render_template(
        "editar_producto.html",
        producto=producto
    )

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    Producto.eliminar_producto(id)
    return render_template("Inventario.html", productos=Producto.listar_productos())

@app.route("/reponer/<int:id>", methods=["GET", "POST"])
def reponer_producto(id):
    producto = Producto.obtener_producto(id)

    if request.method == "POST":
        cantidad = int(request.form["cantidad"])

        producto.stock += cantidad

        producto.editar_producto(id)

        return redirect("/inventario")

    return render_template(
        "reponer_producto.html",
        producto=producto
    )
    
# ---------------- VENTAS ----------------
@app.route("/venta", methods=["GET", "POST"])
def venta():
    if request.method == "POST":
        productos_json = request.form.get("productos_json")
        productos_lista = json.loads(productos_json) if productos_json else []

        if not productos_lista:
            return render_template("venta.html", productos=Producto.listar_productos(), error="No se seleccionaron productos")

        venta = Venta()
        for item in productos_lista:
            producto_id = int(item["id"])
            cantidad = int(item["cantidad"])
            datos = Producto.obtener_producto(producto_id)

            if datos.stock < cantidad:
                return render_template("venta.html", productos=Producto.listar_productos(), error=f"Stock insuficiente para {datos.nombre}")

            producto = Producto(
                id_producto=datos.id,
                nombre=datos.nombre,
                categoria=datos.categoria,
                precio=datos.precio,
                stock=datos.stock - cantidad,
                disponible=datos.disponible
            )

            venta.agregar_producto(producto, cantidad)
            producto.editar_producto(producto_id)

        venta.guardar_venta()
        venta.productos = []

        return render_template("venta.html", productos=Producto.listar_productos(), success=True)

    productos = Producto.listar_productos()
    return render_template("venta.html", productos=productos)

# ---------------- REPORTES ----------------
@app.route("/reportes")
def reportes():
    return render_template("reportes.html")

@app.route("/reportes/productos")
def reporte_productos():
    productos = Reporte.productos_sin_stock()
    return render_template("reportes_productos.html", productos=productos)

@app.route("/reportes/ventas")
def reporte_ventas():
    detalle = Reporte.detalle_ventas_del_dia()
    return render_template("reportes_ventas.html", detalle=detalle)



# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)

