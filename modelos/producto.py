# modelos/producto.py

from database import conectar

class Producto:
    def __init__(self, id_producto=None, nombre=None, categoria=None, precio=0, stock=0, disponible=True):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.disponible = disponible

    # CREAR PRODUCTO
    def crear_producto(self):
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO productos
        (nombre, categoria, precio, stock, disponible)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            self.nombre,
            self.categoria,
            self.precio,
            self.stock,
            True
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

    # LISTAR PRODUCTOS
    @staticmethod
    def listar_productos():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, categoria, precio, stock, disponible FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        return productos


    # OBTENER PRODUCTO
    @staticmethod
    def obtener_producto(id):

        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM productos WHERE id = %s",
            (id,)
        )

        fila = cursor.fetchone()

        conexion.close()

        if fila:

            producto = Producto(
                fila["nombre"],
                fila["categoria"],
                fila["precio"],
                fila["stock"]
            )

            producto.id = fila["id"]

            return producto

        return None

        

        return None

    # EDITAR PRODUCTO
    def editar_producto(self, id):
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE productos
        SET nombre = %s,
            categoria = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        """

        valores = (
            self.nombre,
            self.categoria,
            self.precio,
            self.stock,
            id
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

    # ELIMINAR PRODUCTO
    @staticmethod
    def eliminar_producto(id):
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conexion.commit()
        conexion.close()

    # Método vender
    def vender(self, cantidad):
        if cantidad <= 0:
            print("Cantidad inválida")
            return
        if self.stock >= cantidad:
            self.stock -= cantidad
            print(f"Se vendieron {cantidad} unidades de {self.nombre}")
        else:
            print("No hay suficiente stock")

    # Método reponer stock
    def reponer_stock(self, cantidad):
        if cantidad > 0:
            self.stock += cantidad
            print(f"Stock actualizado: {self.stock}")

    # Método sin stock
    def sin_stock(self):
        return self.stock == 0

    # Método calcular valor stock
    def calcular_valor_stock(self):
        return self.precio * self.stock

    # Método actualizar precio
    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self.precio = nuevo_precio

    def __str__(self):
        return f"{self.nombre} - ${self.precio} - Stock: {self.stock}"
