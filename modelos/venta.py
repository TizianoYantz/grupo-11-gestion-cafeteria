from database import conectar

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

    def guardar_venta(self):
        pass