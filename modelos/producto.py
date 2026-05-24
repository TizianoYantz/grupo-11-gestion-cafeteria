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