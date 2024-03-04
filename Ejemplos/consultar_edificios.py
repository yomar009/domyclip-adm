import sqlite3

# Conectarse a la base de datos
DATABASE = 'database.db'

# Definir la función para buscar edificios por usuario
def buscar_edificios_por_usuario(username):
    
    conn = sqlite3.connect(DATABASE)
    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()
    cursor.execute("SELECT edificio_id, nombre, apartamentos, direccion, nit FROM Edificios WHERE usuario_id = ?", (username,))
    edificios = cursor.fetchall()
    print(edificios)
    conn.close()
# Supongamos que quieres buscar los edificios del usuario con ID 1


# Definir la función para buscar edificios por usuario
def buscar_bloques_edificio(edificio_id):
    
    conn = sqlite3.connect(DATABASE)
    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bloque FROM Propietarios WHERE edificio_id = ?", (edificio_id,))
    edificios = cursor.fetchall()
    print(edificios)
    conn.close()


#edificios_usuario = buscar_edificios_por_usuario(username)

def buscar_propietarios_bloque(edificio_id, bloque):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    propietarios_por_bloque = {}
    
    # Obtener los propietarios del bloque especificado en el edificio especificado
    cursor.execute("SELECT bloque, nombres, apellidos, parq, cedula, celular, direccion, correo FROM Propietarios WHERE edificio_id = ? AND bloque = ?", (edificio_id, bloque))
    propietarios_por_bloque = cursor.fetchall()
    print(propietarios_por_bloque)
    conn.close()

username = 'ProAdm'
edificio_id = 1
bloque_deseado = 1

#buscar_usuario = buscar_edificios_por_usuario(username)
#edificio_bloque = buscar_bloques_edificio(edificio_id)
propietarios_bloque_1 = buscar_propietarios_bloque(edificio_id, bloque_deseado)


#print("Propietarios del Bloque 1 en el Edificio 1:")
#for propietario in propietarios_bloque_1:
#    print(propietario)
