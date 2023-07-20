import sqlite3

def conectar():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    return conn, c

def crear_tablas():
    conn, c = conectar()

    # Creamos la tabla "clientes"
    c.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL
        )
    """)

    # Creamos la tabla "Pedidos"
    c.execute("""
        CREATE TABLE IF NOT EXISTS Pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_proveedor INTEGER,
        codigo_producto TEXT,
        cantidad INTEGER,
        nombre_producto TEXT,
        precio_local REAL,
        precio_dolar REAL,
        FOREIGN KEY (id_cliente) REFERENCES clientes (id),
        FOREIGN KEY (id_proveedor) REFERENCES proveedores (id)
    )
    """)

    # Creamos la tabla "proveedores"
    c.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
if __name__ == "__main__":
    crear_tablas()
