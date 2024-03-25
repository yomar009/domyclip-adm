import sqlite3
DATABASE = 'database.db'

edificio_id = 1

def obtener_ultimo_id_cxc(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_CXC) FROM CuentasCobrar WHERE edificio_id = ?", (edificio_id,))
    resultado = cursor.fetchone()
    ultimo_id_cxc = resultado[0] if resultado[0] is not None else 0
    conn.close()  # Cierra la conexión después de obtener el ID
    return ultimo_id_cxc

ultimo_id_cxc = obtener_ultimo_id_cxc(edificio_id)  # Asignar el resultado de la función a una variable
print(ultimo_id_cxc)
