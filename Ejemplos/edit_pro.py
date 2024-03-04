import sqlite3

def actualizar_propietario():
    # Conectarse a la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Modificar el nombre y apellidos del propietario
    nuevo_nombre = 'Mario'
    nuevo_apellido = 'Toro Gomez'
    edificio_id = 1
    apto = '103'
    bloque = '1'

    cursor.execute('''
        UPDATE propietarios
        SET nombres = ?,
            apellidos = ?
        WHERE edificio_id = ? AND bloque = ? AND apto = ?
    ''', (nuevo_nombre, nuevo_apellido, edificio_id, bloque, apto))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print("Propietario modificado correctamente.")

# Llamamos a la función para actualizar el propietario
actualizar_propietario()
