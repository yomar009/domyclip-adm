import sqlite3

# Importa la función para obtener la fecha actual
from datetime import datetime

def obtener_fecha_actual():
    return datetime.today().strftime("%Y-%m-%d")

def crear_cxc(cursor, id_CXC, user_id, edificio_id, fecha_vencimiento, estado):

    fecha_emision = obtener_fecha_actual()

    cursor.execute("""
        INSERT INTO CuentasCobrar (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado))

def agregar_detalle_cxc(cursor, id_CXC, user_id, tipo, monto, total, descripcion, estado):

    cursor.execute("""
        INSERT INTO CXCDetalle (id_CXC, user_id, tipo, monto, total, descripcion, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_CXC, user_id, tipo, monto, total, descripcion, estado))

# Conexión a la base de datos
conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

# Crear la CXC


# Preguntar al usuario por los datos de la CXC
id_CXC= int(input("Ingresa el nuemero de CXC: "))
user_id = int(input("Ingrese el ID del usuario: "))
edificio_id = int(input("Ingrese el ID del edificio: "))
fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
estado = input("Ingrese el estado inicial de la CXC (Pendiente/Pagada): ")

# Preguntar al usuario por los detalles de la CXC
tipo = input("Ingrese el tipo de detalle (ADM, PARQ, MUL, EXT.): ")
monto = float(input("Ingrese el monto: "))
total = monto
descripcion = input("Ingrese la descripción del detalle: ")

crear_cxc(cursor, id_CXC, user_id, edificio_id, fecha_vencimiento, estado)

agregar_detalle_cxc(cursor, id_CXC, user_id, tipo, monto, total, descripcion, estado)

# Guardar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()


print("cuenta por cobrar creado exitosamente")