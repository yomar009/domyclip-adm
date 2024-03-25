from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

# Importa la función para obtener la fecha actual
def obtener_fecha_actual():
    return datetime.today().strftime("%Y-%m-%d")

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
    cursor.execute("SELECT user_id, nombres, apellidos, apto, cedula, celular, direccion, parq, correo, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento, estado FROM Propietarios WHERE edificio_id = ? AND bloque = ?", (edificio_id, bloque))
    propietarios = cursor.fetchall()

    # Convertir el estado numérico a texto ("activo" o "desactivado")
    for i, propietario in enumerate(propietarios):
        estado_num = propietario[16]  # Último elemento de la tupla, que es el campo "estado"
        if estado_num == 1:
            propietarios[i] = propietario[:16] + ('activo',)  # Reemplazar el último elemento con "activo"
        elif estado_num == 0:
            propietarios[i] = propietario[:16] + ('desactivado',)  # Reemplazar el último elemento con "desactivado"

    conn.close()
    return propietarios

def obtener_cuentas_por_cobrar_fecha(edificio_id, fecha_emision=None, user_id_ed=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if fecha_emision and user_id_ed:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado, P.nombres, P.apellidos,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.fecha_emision = ? AND CC.user_id = ? 
        """, (edificio_id, fecha_emision, user_id_ed))
    elif fecha_emision:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado, P.nombres, P.apellidos,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.fecha_emision = ?
        """, (edificio_id, fecha_emision))
    elif user_id_ed:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado, P.nombres, P.apellidos,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.user_id = ?
        """, (edificio_id, user_id_ed))
    else:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado, P.nombres, P.apellidos,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ?
        """, (edificio_id,))
    
    cuentas = cursor.fetchall()
    
    cuentas_por_cobrar = {}
    for cuenta in cuentas:
        id_CXC, user_id, fecha_emision, fecha_vencimiento, estado, nombres, apellidos, detalle_id, tipo, monto, pagado, total, descripcion = cuenta
        nombre_usuario = f"{nombres} {apellidos}"
        if id_CXC not in cuentas_por_cobrar:
            cuentas_por_cobrar[id_CXC] = {
                'id_CXC': id_CXC,
                'user_id': user_id,
                'usuario': nombre_usuario,
                'fecha_emision': fecha_emision,
                'fecha_vencimiento': fecha_vencimiento,
                'estado': estado,
                'detalles': []
            }
        if tipo is not None:  # Si hay detalles asociados
            cuentas_por_cobrar[id_CXC]['detalles'].append({
                'detalle_id': detalle_id,  # Asegúrate de incluir el ID del detalle
                'tipo': tipo,
                'monto': monto,
                'pagado': pagado,
                'total': total,
                'descripcion': descripcion
            })
    
    cuentas_por_cobrar_list = list(cuentas_por_cobrar.values())
    
    conn.close()
    return cuentas_por_cobrar_list

# ----------------------------------------------CXC--------CXC----------
def obtener_ultimo_id_cxc(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_CXC) FROM CuentasCobrar WHERE edificio_id = ?", (edificio_id,))
    resultado = cursor.fetchone()
    ultimo_id_cxc = resultado[0] if resultado[0] is not None else 0
    conn.close()  # Cierra la conexión después de obtener el ID
    return ultimo_id_cxc


def crear_cxc(id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CuentasCobrar (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado))
    conn.commit()  # Confirma los cambios en la base de datos
    conn.close()  # Cierra la conexión después de crear la cuenta por cobrar

def agregar_detalle_cxc(id_CXC, user_id, tipo, monto, total, descripcion, estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CXCDetalle (id_CXC, user_id, tipo, monto, total, descripcion, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_CXC, user_id, tipo, monto, total, descripcion, estado))
    conn.commit()  # Confirma los cambios en la base de datos
    conn.close()  # Cierra la conexión después de agregar el detalle a la cuenta por cobrar

def eliminar_cxc(id_CXC, user_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Eliminar entrada de CuentasCobrar
        cursor.execute("DELETE FROM CuentasCobrar WHERE id_CXC = ? AND user_id = ?", (id_CXC, user_id))
        # Eliminar entradas relacionadas de CXCDetalles
        cursor.execute("DELETE FROM CXCDetalle WHERE id_CXC = ? AND user_id = ?", (id_CXC, user_id))

        conn.commit()  # Confirma los cambios en la base de datos
        conn.close()   # Cierra la conexión
    except sqlite3.Error as e:
        print("Error al eliminar la CXC:", e)

def eliminar_detalle_cxc(detalle_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Eliminar el detalle específico de la tabla CXCDetalle
        cursor.execute("DELETE FROM CXCDetalle WHERE id = ?", (detalle_id,))

        conn.commit()  # Confirma los cambios en la base de datos
        conn.close()   # Cierra la conexión
    except sqlite3.Error as e:
        print("Error al eliminar el detalle de la CXC:", e)

def editar_detalle_cxc(detalle_id, descripcion, monto):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Actualizar la descripción y el monto del detalle específico en la tabla CXCDetalle
        cursor.execute("UPDATE CXCDetalle SET descripcion = ?, monto = ? WHERE id = ?", (descripcion, monto, detalle_id))

        conn.commit()  # Confirma los cambios en la base de datos
        conn.close()   # Cierra la conexión
    except sqlite3.Error as e:
        print("Error al editar el detalle de la CXC:", e)

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

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        return '', 204




@app.route('/pagos/<int:edificio_id>/')
def pagos(edificio_id):

    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    user_id = session.get('user_id')  # Obtener el user_id del usuario logueado
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    bloques = obtener_bloques(edificio_id)  # Agregar esta línea para obtener los bloques
    
    propietarios_por_bloque = {}
    for bloque in bloques:
        propietarios_por_bloque[bloque] = obtener_propietarios_por_bloque(edificio_id, bloque)
    
    return render_template('pagos.html', edificio_id=edificio_id, user_id=user_id, nombre_edificio=nombre_edificio,
                           username=username, bloques=bloques, propietarios_por_bloque=propietarios_por_bloque,
                           )



# Ruta para la actualización de datos del propietario
@app.route('/actualizar_cobros', methods=['POST'])
def actualizar_cobros_propietario():  # Cambia el nombre de la función
    if request.method == 'POST':
        edificio_id = request.form['modal_edificio_id']
        # Obtener los datos del formulario
        user_id = request.form['user_id']  
        cuotaADM = request.form['cuotaADM']  # Campo "Admin"
        cuotaPARQ = request.form['cuotaPARQ']  # Campo "Parq"
        cuotaEXT = request.form['cuotaEXT']  # Campo "Cuota Extra"
        multa = request.form['multa']  # Campo "Multa"
        intereses = request.form['intereses']  # Campo "Intereses"
        fecha_emision = request.form['fecha_emision']  # Campo "fecha_emision"
        fecha_vencimiento = request.form['fecha_vencimiento']  # Campo "fecha_vencimiento"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Propietarios SET cuotaADM=?, cuotaPARQ=?, cuotaEXT=?, multa=?, intereses=?, fecha_emision=?, fecha_vencimiento=? WHERE user_id=?", (cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento, user_id))

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        return redirect(f'/pagos/{edificio_id}/')

# Ruta para actualizar las fechas de emisión y vencimiento de todos los propietarios de un edificio
@app.route('/crear_plantilla', methods=['POST'])
def crear_plantilla():
    if request.method == 'POST':
        # Obtener las fechas de emisión y vencimiento del formulario
        edificio_id = request.form['edificio_id']
        fecha_emision = request.form['fecha_emision']
        fecha_vencimiento = request.form['fecha_vencimiento']

        # Conectar a la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Actualizar las fechas de emisión y vencimiento de los propietarios del edificio
        cursor.execute("UPDATE Propietarios SET fecha_emision=?, fecha_vencimiento=? WHERE edificio_id=?", (fecha_emision, fecha_vencimiento, edificio_id))

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        # Redireccionar a la página de pagos del edificio actualizado
        return redirect(f'/pagos/{edificio_id}/')

# Ruta para la contabilización automática
@app.route('/contabilizar_automatico/<int:edificio_id>/', methods=['GET'])
def contabilizar_automatico(edificio_id):


    # Obtener el último id_CXC del edificio
    ultimo_id_cxc = obtener_ultimo_id_cxc(edificio_id)
    # Conectar a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Crear cuentas de cobro para cada propietario
    cursor.execute("SELECT user_id, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento FROM Propietarios WHERE edificio_id = ? AND (cuotaADM != 0 OR cuotaPARQ != 0 OR multa != 0 OR intereses != 0)", (edificio_id,))
    propietarios = cursor.fetchall()

    # Confirmar y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    for propietario in propietarios:
        ultimo_id_cxc += 1  # Incrementar el id_CXC
        id_CXC = ultimo_id_cxc
        user_id, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento = propietario
        
        # Crear la cuenta de cobro
        crear_cxc(id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, "Pendiente")
        
        # Agregar detalles a la cuenta de cobro
        if cuotaADM != 0:
            agregar_detalle_cxc(id_CXC, user_id, "ADM", cuotaADM, cuotaADM, "Cuota de Administración", "Pendiente")
        if cuotaPARQ != 0:
            agregar_detalle_cxc(id_CXC, user_id, "PARQ", cuotaPARQ, cuotaPARQ, "Cuota de Parqueadero", "Pendiente")
        if cuotaEXT != 0:
            agregar_detalle_cxc(id_CXC, user_id, "EXT", cuotaEXT, cuotaEXT, "Cuota Extra Fija", "Pendiente")
        if multa != 0:
            agregar_detalle_cxc(id_CXC, user_id, "MUL", multa, multa, "Multa Administrativa por inasistencia", "Pendiente")
        if intereses != 0:
            agregar_detalle_cxc(id_CXC, user_id, "INT", intereses, intereses, "Intereses", "Pendiente")

    print("Contabilización automática realizada para el edificio ID:", edificio_id)
    
    # Puedes redireccionar a alguna página después de realizar la contabilización automática
    return redirect(f'/pagos/{edificio_id}/')

@app.route('/crear_deuda', methods=['POST'])
def crear_multa():
    id_CXC = request.form['id_CXC']  # Obtener la ID_CXC del formulario
    user_id = request.form['user_id']  
    tipo = request.form['tipo']  # Obtener el tipo de multa del formulario
    monto = request.form['monto']
    total = None
    descripcion = request.form['descripcion']
    estado = 'pendiente'  # Valor predeterminado
    edificio_id = request.form['edificio_id']  # Obtener edificio_id
    
    agregar_detalle_cxc(id_CXC, user_id, tipo, monto, total, descripcion, estado)  # El total se establece en 0

    return redirect(f'/contabilidad/{edificio_id}/')

@app.route('/eliminar_cxc', methods=['POST'])
def eliminar_cxc_route():
    id_CXC = request.form['id_CXC']  # Obtener la ID_CXC del formulario
    user_id = request.form['user_id']  
    edificio_id = request.form['edificio_id']  # Obtener edificio_id

    eliminar_cxc(id_CXC, user_id)

    return redirect(f'/contabilidad/{edificio_id}/')

@app.route('/eliminar_detalle_cxc', methods=['POST'])
def eliminar_detalle_cxc_route():
    detalle_id = request.form['detalle_id']  # Obtener el ID del detalle del formulario
    edificio_id = request.form['edificio_id']  # Obtener edificio_id

    eliminar_detalle_cxc(detalle_id)  # Llama a la función eliminar_detalle_cxc con el detalle_id
    #print("Eliminando detalle ID", detalle_id)
    
    return redirect(f'/contabilidad/{edificio_id}/')

@app.route('/editar_detalle_cxc', methods=['POST'])
def editar_detalle_cxc_route():
    detalle_id = request.form['detalle_id']  # Obtener el ID del detalle del formulario
    descripcion = request.form['descripcion']  # Obtener la nueva descripción del formulario
    monto = request.form['monto']  # Obtener el nuevo monto del formulario
    edificio_id = request.form['edificio_id']  # Obtener el ID del edificio del formulario
    
    editar_detalle_cxc(detalle_id, descripcion, monto)  # Llama a la función para editar el detalle
    print("Editando detalle", detalle_id)
    
    return redirect(f'/contabilidad/{edificio_id}/')


# Ruta para la página de contabilidad
@app.route('/contabilidad/<int:edificio_id>/')
def contabilidad(edificio_id):
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    
    user_id_ed = request.args.get('user_id') # Obtener el user_id
    fecha_emision = request.args.get('fecha_emision')  # Obtener la fecha de emisión filtrada
    
    cuentas_por_cobrar = []

    if fecha_emision is None:  # Si no se proporciona fecha_emision, establecer la fecha del día
        fecha_emision = obtener_fecha_actual()
        
    if fecha_emision:
        cuentas_por_cobrar = obtener_cuentas_por_cobrar_fecha(edificio_id, fecha_emision=fecha_emision, user_id_ed=user_id_ed)
    else:
        cuentas_por_cobrar = obtener_cuentas_por_cobrar_fecha(edificio_id, user_id_ed=user_id_ed)

    return render_template('contabilidad.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username, cuentas_por_cobrar=cuentas_por_cobrar)



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
