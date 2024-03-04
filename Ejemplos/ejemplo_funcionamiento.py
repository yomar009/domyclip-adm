import sqlite3

# Definir la conexión a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Función para iniciar sesión
def iniciar_sesion(usuario, contraseña):
    # Verificar si el usuario y la contraseña coinciden en la base de datos
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
    usuario_encontrado = cursor.fetchone()
    if usuario_encontrado:
        return usuario_encontrado
    else:
        return None

# Función para obtener los edificios asociados a un usuario
def obtener_edificios(usuario_id):
    cursor.execute("SELECT * FROM Edificios WHERE usuario_id = ?", (usuario_id,))
    edificios = cursor.fetchall()
    return edificios

# Función para obtener los propietarios de un edificio
def obtener_propietarios(edificio_id):
    cursor.execute("SELECT * FROM Propietarios WHERE edificio_id = ?", (edificio_id,))
    propietarios = cursor.fetchall()
    return propietarios

# Función para mostrar los edificios disponibles y permitir al usuario seleccionar uno
def seleccionar_edificio(edificios):
    print("Edificios disponibles:")
    for edificio in edificios:
        print(f"{edificio['edificio_id']}: {edificio['nombre']}")
    edificio_seleccionado = input("Ingrese el ID del edificio que desea seleccionar: ")
    return edificio_seleccionado

# Función para mostrar los propietarios de un edificio
def mostrar_propietarios(propietarios):
    print("Propietarios del edificio:")
    for propietario in propietarios:
        print(f"{propietario['nombres']} {propietario['apellidos']} - Apartamento: {propietario['apto']}")

