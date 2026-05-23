#POO - esta dividido en 3 clases principales, Producto, Venta e Inventario

class Producto:

    def __init__(self, id_producto, nombre, categoria, precio, stock, estado=True):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.estado = estado

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



class Venta:

    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto, cantidad):
        self.productos.append((producto, cantidad))

    def calcular_total(self):

        total = 0

        for producto, cantidad in self.productos:
            total += producto.precio * cantidad

        return total

    def generar_resumen(self):

        for producto, cantidad in self.productos:
            print(f"{producto.nombre} x{cantidad}")

        print(f"TOTAL: ${self.calcular_total()}")
        

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