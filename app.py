from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__, static_url_path='/login')
app.secret_key = 'admin'  # Configura la clave secreta

# Redirigir la ruta base '/' a la página de inicio de sesión '/login'
@app.route('/')
def home():
    return redirect(url_for('login'))

# Configura la conexión a la base de datos SQLite
DATABASE = 'database.db'

# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not obtener_usuario(username):
            agregar_usuario(username, password)
            return redirect(url_for('login'))
        else:
            return render_template('registro.html', error='El nombre de usuario ya está en uso.')
    return render_template('registro.html')

# Función para obtener un usuario por nombre de usuario
def obtener_usuario(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE username = ?', (username,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario
# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(username, password):
    if not obtener_usuario(username):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True  # Usuario agregado correctamente
    return False  # Nombre de usuario ya en uso




# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar credenciales
        if check_credentials(username, password):
            session['username'] = username
            return redirect('/indexEdi')  # Redirigir a la página de inicio después de iniciar sesión
        else:
            error_message = 'Usuario o contraseña incorrectos'
    
    return render_template('login.html', error_message=error_message)

# Función para verificar credenciales
def check_credentials(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None






# Ruta del editor después del inicio de sesión
@app.route('/indexEdi')
def indexEdi():
    if 'username' in session:
        # Obtener los edificios asociados al usuario
        username = session['username']
        edificios = get_edificios_por_usuario(username)
        return render_template('indexEdi.html', username=username, edificios=edificios)
    else:
        return redirect('/login')

# Función para obtener los edificios asociados a un usuario
def get_edificios_por_usuario(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT edificio_id, nombre, apartamentos, direccion, nit FROM Edificios WHERE usuario_id = ?", (username,))
    edificios = cursor.fetchall()
    print(edificios)
    conn.close()
    return edificios




# Obtener el nombre del edificio
def obtener_nombre_edificio(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Edificios WHERE edificio_id = ?", (edificio_id,))
    nombre_edificio = cursor.fetchone()[0]
    conn.close()
    return nombre_edificio

# Obtener bloques por edificio
def obtener_bloques(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bloque FROM Propietarios WHERE edificio_id = ?", (edificio_id,))
    bloques = [row[0] for row in cursor.fetchall()]
    conn.close()
    return bloques

# Obtener propietarios por bloque
def obtener_propietarios_por_bloque(edificio_id, bloque):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, nombres, apellidos, apto, cedula, celular, direccion, parq, correo, valoradmin, valorparq, cuotaextra FROM Propietarios WHERE edificio_id = ? AND bloque = ?", (edificio_id, bloque))
    propietarios = cursor.fetchall()
    conn.close()
    return propietarios


def obtener_multas_e_intereses_por_edificio(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT apto, bloque, fecha, CXC, CuotaAMD, Interes, Multa, CuotaExtra, ValorTotal, estado FROM CuentasCobrar WHERE edificio_id = ? AND (Interes > 0 OR Multa > 0) ORDER BY fecha", (edificio_id,))
    multas_e_intereses = cursor.fetchall()
    conn.close()
    
    # Transformar las tuplas en diccionarios para facilitar el acceso a los campos en la plantilla
    multas_e_intereses_dict = []
    for item in multas_e_intereses:
        multas_e_intereses_dict.append({
            'apto': item[0],
            'bloque': item[1],
            'fecha': item[2],
            'CXC': item[3],
            'CuotaAMD': item[4],
            'Interes': item[5],
            'Multa': item[6],
            'CuotaExtra': item[7],
            'ValorTotal': item[8],
            'estado': item[9]
        })
    
    return multas_e_intereses_dict






# Ruta para la página de estadísticas
@app.route('/estadisticas/<int:edificio_id>/')
def estadisticas(edificio_id):
    # Verificar si el usuario ha iniciado sesión
    if 'username' in session:
        username = session['username']
    else:
        return redirect('/login')

    # Obtener el nombre del edificio
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    # Verificar si se encontró el edificio
    if not nombre_edificio:
        # Si el edificio no existe, puedes manejar el error aquí o redirigir a una página de error
        return render_template('error.html', message="El edificio no existe")

    return render_template('estadisticas.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username)

# Ruta para la página principal de propietarios
@app.route('/propietarios/<int:edificio_id>/')
def propietarios(edificio_id):
        
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    bloques = obtener_bloques(edificio_id)  # Agregar esta línea para obtener los bloques

    propietarios_por_bloque = {}
    for bloque in bloques:
        propietarios_por_bloque[bloque] = obtener_propietarios_por_bloque(edificio_id, bloque)

    return render_template('propietarios.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, 
                           username=username, bloques=bloques, propietarios_por_bloque=propietarios_por_bloque)

# Ruta para la actualización de datos del propietario
@app.route('/actualizar_propietario', methods=['POST'])
def actualizar_propietario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.form['user_id']  
        nombres = request.form['nombre']
        apellidos = request.form['apellido']
        bloque_id = request.form['bloque_id']
        cedula = request.form['cedula']
        celular = request.form['celular']
        direccion = request.form['direccion']
        parq = request.form['parq']
        correo = request.form['correo']

        # Realizar la actualización en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Propietarios SET nombres=?, apellidos=?, cedula=?, bloque=?, celular=?, direccion=?, parq=?, correo=? WHERE user_id=?", (nombres, apellidos, cedula, bloque_id, celular, direccion, parq, correo, user_id))

        conn.commit()
        conn.close()

        return '', 204




# Ruta para la página de pagos
@app.route('/pagos/<int:edificio_id>/')
def pagos(edificio_id):

    if 'username' in session:# Verificar si el usuario ha iniciado sesión
        username = session['username']# Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    bloques = obtener_bloques(edificio_id)  # Agregar esta línea para obtener los bloques
    
    propietarios_por_bloque = {}
    for bloque in bloques:
        propietarios_por_bloque[bloque] = obtener_propietarios_por_bloque(edificio_id, bloque)

    # Obtener todas las multas e intereses del edificio
    multas_e_intereses_por_edif = obtener_multas_e_intereses_por_edificio(edificio_id)

    # Filtrar multas e intereses
    multas = [item for item in multas_e_intereses_por_edif if item['Multa'] > 0]
    intereses = [item for item in multas_e_intereses_por_edif if item['Interes'] > 0]

    return render_template('pagos.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio,
                           username=username, bloques=bloques, propietarios_por_bloque=propietarios_por_bloque,
                           multas=multas, intereses=intereses)

# Ruta para la actualización de datos del propietario
@app.route('/actualizar_cobros', methods=['POST'])
def actualizar_cobros_propietario():  # Cambia el nombre de la función
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.form['user_id']  
        valoradmin = request.form['valoradmin']  # Nuevo campo "Admin"
        valorparq = request.form['valorparq']  # Nuevo campo "Parq"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Propietarios SET valoradmin=?, valorparq=? WHERE user_id=?", (valoradmin, valorparq, user_id))

        conn.commit()
        conn.close()

        return '', 204




# Ruta para la página de contabilidad
@app.route('/contabilidad/<int:edificio_id>/')
def contabilidad(edificio_id):
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    
    return render_template('contabilidad.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username)


# Ruta para la página de informes
@app.route('/informes/<int:edificio_id>/')
def informes(edificio_id):
    if 'username' in session:# Verificar si el usuario ha iniciado sesión
        username = session['username']# Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    

    return render_template('informes.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username)

# Ruta para la página de configuración
@app.route('/configuracion/<int:edificio_id>/')
def configuracion(edificio_id):
    if 'username' in session:# Verificar si el usuario ha iniciado sesión
        username = session['username']# Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    

    return render_template('configuracion.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username)








@app.route('/activar_riego')
def activar_riego():
    # Lógica para activar el riego (puedes llamar a una función específica aquí)
    # ...

    return 'Riego 10 minutos'

@app.route('/activar_ventilacion')
def activar_ventilacion():
    # Lógica para activar la ventilación (puedes llamar a una función específica aquí)
    # ...

    return 'Ventilación 10 minutos'

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    app.run(debug=True, host='0.0.0.0')
