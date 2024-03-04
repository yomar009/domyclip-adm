import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('database.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Definir la consulta SQL para obtener la información de los propietarios del edificio A del usuario ProAdm

consulta = """
    SELECT p.*
    FROM propietarios p
    INNER JOIN edificios e ON p.edificio_id = e.edificio_id
    INNER JOIN usuarios u ON e.usuario_id = u.usuario_id
    WHERE e.nombre = 'Edificio A' AND u.username = 'ProAdm'
"""

# Ejecutar la consulta
cursor.execute(consulta)

# Obtener los resultados de la consulta
propietarios = cursor.fetchall()

# Imprimir la información de los propietarios
print("Información de los propietarios del edificio A del usuario ProAdm:")
for propietario in propietarios:
    print(propietario)

# Cerrar la conexión con la base de datos
conn.close()
