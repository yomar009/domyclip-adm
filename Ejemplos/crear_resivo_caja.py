import sqlite3


def crear_rc(cursor,id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado):
    cursor.execute('''
        INSERT INTO ReciboCaja (id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado)
        VALUES (?, ?, ?, ?, ?, ?, ? ,?)
    ''', (id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado))

# Insertar los datos en la tabla RCDetalles
def agregar_detalle_rc(cursor, id_RC, user_id, cruceID, monto, estado):
    cursor.execute('''
        INSERT INTO RCDetalles (id_RC, user_id, cruceID, monto, estado)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_RC, user_id, cruceID, monto, estado))

# Conexión a la base de datos
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Obtener los datos del usuario desde la terminal
user_id = int(input("Ingrese el ID del usuario: "))
edificio_id = int(input("Ingrese el ID del edificio: "))
fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
descripcion = input("Ingrese la descripción banco: ")
tipopago = input("Ingrese el tipo de pago: ")
valor = float(input("Ingrese el valor: "))
estado = input("Ingrese el estado: ")

cruceID = int(input("Ingrese el ID del cruce CXC: "))
id_RC = int(input("Ingrese el ID RC: "))
monto = valor

crear_rc(cursor, id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado)
agregar_detalle_rc(cursor, id_RC, user_id, cruceID, monto, estado)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Recibo de caja creado exitosamente")
# Obtener los datos del usuario desde la terminal
