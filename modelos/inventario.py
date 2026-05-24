class Inventario:

    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, id_producto):

        for producto in self.productos:

            if producto.id == id_producto:
                self.productos.remove(producto)

    def buscar_producto(self, nombre):

        for producto in self.productos:

            if producto.nombre == nombre:
                return producto

        return None

    def listar_productos(self):

        for producto in self.productos:
            print(producto)

    def filtrar_categoria(self, categoria):

        for producto in self.productos:

            if producto.categoria == categoria:
                print(producto)

    def productos_sin_stock(self):

        for producto in self.productos:

            if producto.sin_stock():
                print(producto)

    def calcular_valor_total(self):

        total = 0

        for producto in self.productos:
            total += producto.calcular_valor_stock()

        return total       