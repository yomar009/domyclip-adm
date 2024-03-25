import sqlite3
from datetime import datetime

# Obtener el edificio_id
edificio_id = int(input("Ingrese el ID del edificio: "))


def obtener_ultimo_id_cxc(cursor, edificio_id):
    cursor.execute("SELECT MAX(id_CXC) FROM CuentasCobrar WHERE edificio_id = ?", (edificio_id,))
    resultado = cursor.fetchone()
    ultimo_id_cxc = resultado[0] if resultado[0] is not None else 0
    return ultimo_id_cxc

def crear_cxc(cursor, id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado):
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


# Obtener el último id_CXC del edificio
ultimo_id_cxc = obtener_ultimo_id_cxc(cursor, edificio_id)

# Crear cuentas de cobro para cada propietario
cursor.execute("SELECT user_id, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento FROM Propietarios WHERE edificio_id = ? AND (cuotaADM != 0 OR cuotaPARQ != 0 OR multa != 0 OR intereses != 0)", (edificio_id,))
propietarios = cursor.fetchall()

for propietario in propietarios:
    ultimo_id_cxc += 1  # Incrementar el id_CXC
    id_CXC = ultimo_id_cxc
    user_id, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento = propietario
    
    # Crear la cuenta de cobro
    crear_cxc(cursor, id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, "Pendiente")
    
    # Agregar detalles a la cuenta de cobro
    if cuotaADM != 0:
        agregar_detalle_cxc(cursor, id_CXC, user_id, "ADM", cuotaADM, cuotaADM, "Cuota de Administración", "Pendiente")
    if cuotaPARQ != 0:
        agregar_detalle_cxc(cursor, id_CXC, user_id, "PARQ", cuotaPARQ, cuotaPARQ, "Cuota de Parqueadero", "Pendiente")
    if cuotaEXT != 0:
        agregar_detalle_cxc(cursor, id_CXC, user_id, "EXT", cuotaEXT, cuotaEXT, "Cuota Extra", "Pendiente")
    if multa != 0:
        agregar_detalle_cxc(cursor, id_CXC, user_id, "MUL", multa, multa, "Multa", "Pendiente")
    if intereses != 0:
        agregar_detalle_cxc(cursor, id_CXC, user_id, "INT", intereses, intereses, "Intereses", "Pendiente")

# Guardar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()

print("Cuentas de cobro creadas exitosamente para los propietarios con valores distintos de cero en cuotaADM, cuotaPARQ, multa e intereses.")
