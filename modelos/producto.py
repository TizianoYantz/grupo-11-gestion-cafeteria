from database import conectar

class Producto:
    def __init__(self, id_producto=None, nombre=None, categoria=None,
                 precio=0, stock=0, disponible=True):
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
            self.stock > 0
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

    # LISTAR PRODUCTOS
    @staticmethod
    def listar_productos():
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, categoria, precio, stock, disponible
            FROM productos
        """)

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
            return Producto(
                id_producto=fila["id"],
                nombre=fila["nombre"],
                categoria=fila["categoria"],
                precio=fila["precio"],
                stock=fila["stock"],
                disponible=fila["disponible"]
            )

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
            stock = %s,
            disponible = %s
        WHERE id = %s
        """

        valores = (
            self.nombre,
            self.categoria,
            self.precio,
            self.stock,
            self.stock > 0,
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

        cursor.execute(
            "DELETE FROM productos WHERE id = %s",
            (id,)
        )

        conexion.commit()
        conexion.close()
    
    @staticmethod
    def obtener_categorias():
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT DISTINCT categoria
            FROM productos
            ORDER BY categoria
        """)

        categorias = [fila[0] for fila in cursor.fetchall()]

        conexion.close()

        return categorias    