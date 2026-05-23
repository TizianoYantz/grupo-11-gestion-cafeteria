from database import conectar

conexion = conectar()

conexion.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    disponible INTEGER NOT NULL
)
""")

conexion.close()

print("Base de datos creada")