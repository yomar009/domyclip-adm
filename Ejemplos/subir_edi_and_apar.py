import sqlite3
from datetime import date

# Conectarse a la base de datos
conn = sqlite3.connect('database.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Verificar si las tablas existen, y si no, crearlas

# Crear la tabla Usuarios con usuario_id único y autoincremental
def crear_tabla_usuarios(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            correo TEXT UNIQUE,
            password TEXT,
            UNIQUE(usuario_id)
                   );''')

# Creación de la tabla edificios
def crear_tabla_edificios(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Edificios (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apartamentos INTEGER NOT NULL,
            direccion TEXT NOT NULL,
            nit TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
                   )''')

# Creación de la tabla propietarios
def crear_tabla_propietarios(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Propietarios (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            apto TEXT,
            bloque TEXT NOT NULL,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            parq TEXT,
            cedula TEXT NOT NULL,
            celular TEXT NOT NULL,
            direccion TEXT NOT NULL,
            correo TEXT,
            valoradmin INTERGER,
            valorparq INTERGER,
            cuotaextra INTERGER,
            FOREIGN KEY (edificio_id) REFERENCES edificios(edificio_id)
                   )''')
    

def crear_tabla_CuentasCobrar(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CuentasCobrar (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            apto TEXT NOT NULL,
            bloque TEXT NOT NULL,
            fecha TEXT NOT NULL,
            CXC INTEGER NOT NULL,
            CuotaAMD INTEGER NOT NULL,
            Interes INTEGER NOT NULL,
            Multa INTEGER NOT NULL,
            CuotaExtra INTEGER NOT NULL,
            ValorTotal INTEGER NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (edificio_id) REFERENCES Edificios(edificio_id)
        )''')

def crear_tabla_CuentasCobrarZC(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS CuentasCobrarZC (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            parq TEXT NOT NULL,
            bloque TEXT NOT NULL,
            fecha TEXT NOT NULL,
            CXC INTEGER NOT NULL,
            CuotaPAQ INTEGER NOT NULL,
            Interes INTEGER NOT NULL,
            Multa INTEGER NOT NULL,
            CuotaExtra INTEGER NOT NULL,
            ValorTotal INTEGER NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (edificio_id) REFERENCES Edificios(edificio_id)
        )''')

def crear_tabla_ReciboCobro(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS ReciboCobro (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            apto TEXT NOT NULL,
            fecha TEXT NOT NULL,
            banco TEXT NOT NULL,
            tipopago INTEGER NOT NULL,
            estado TEXT NOT NULL,
            valor INTEGER NOT NULL,
            FOREIGN KEY (edificio_id) REFERENCES Edificios(edificio_id)
        )''')

def crear_tabla_ReciboCobroZC(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS ReciboCobroZC (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            parq TEXT NOT NULL,
            fecha TEXT NOT NULL,
            banco TEXT NOT NULL,
            tipopago INTEGER NOT NULL,
            estado TEXT NOT NULL,
            valor INTEGER NOT NULL,
            FOREIGN KEY (edificio_id) REFERENCES Edificios(edificio_id)
        )''')


# Crear tabla de usuarios
crear_tabla_usuarios(cursor)

# Crear tabla de edificios
crear_tabla_edificios(cursor)

# Crear tabla de propietarios
crear_tabla_propietarios(cursor)

# Crear tabla de cuentas de cobro
crear_tabla_CuentasCobrar(cursor)

# Crear tabla de cuentas de cobro Zonas Comunes
crear_tabla_CuentasCobrarZC(cursor)

# Crear tabla de resivo de caja
crear_tabla_ReciboCobro(cursor)

# Crear tabla de resivo de caja Zonas Comunes
crear_tabla_ReciboCobroZC(cursor)


# Insertar datos en la tabla de usuarios
usuarios = [
    {'username': 'ProAdm','correo': None,'password': 'admin'},
    {'username': 'Prodos','correo': None,'password': 'admin'}
]


edificios = [
    {'usuario_id': 'ProAdm', 'edificio_id': 1, 'nombre': 'Edificio A', 'apartamentos': 12, 'direccion': 'Calle 123', 'nit': '123456'},#Numero de contacto porteria
    {'usuario_id': 'ProAdm', 'edificio_id': 2, 'nombre': 'Edificio B', 'apartamentos': 5, 'direccion': 'Calle 123', 'nit': '123456'},
    {'usuario_id': 'ProAdm', 'edificio_id': 3, 'nombre': 'Edificio C', 'apartamentos': 1, 'direccion': 'Calle 123', 'nit': '123456'},
    {'usuario_id': 'ProAdm', 'edificio_id': 4, 'nombre': 'Edificio D', 'apartamentos': 1, 'direccion': 'Calle 123', 'nit': '123456'},
    {'usuario_id': 'Prodos', 'edificio_id': 5, 'nombre': 'Edificio E', 'apartamentos': 1, 'direccion': 'Calle 456', 'nit': '789012'},
    {'usuario_id': 'Prodos', 'edificio_id': 6, 'nombre': 'Edificio F', 'apartamentos': 1, 'direccion': 'Calle 456', 'nit': '789012'},
    {'usuario_id': 'Prodos', 'edificio_id': 7, 'nombre': 'Edificio G', 'apartamentos': 1, 'direccion': 'Calle 456', 'nit': '789012'},
    {'usuario_id': 'Prodos', 'edificio_id': 8, 'nombre': 'Edificio H', 'apartamentos': 2, 'direccion': 'Calle 456', 'nit': '789012'}
]


propietarios = [
    {'edificio_id': 1, 'apto': '101', 'bloque': '1', 'nombres': 'Juan Dario', 'apellidos': 'Perez Zapata', 'parq': '12', 'cedula': '123456789', 'celular': '123-456-7890', 'direccion': 'calle 58a #45-45', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '102', 'bloque': '1', 'nombres': 'María Teresa', 'apellidos': 'Gomez Castaño', 'parq': '14', 'cedula': '987654321', 'celular': '987-654-3210', 'direccion': 'calle 60 #50-30', 'correo': 'maria@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '103', 'bloque': '1', 'nombres': 'Miguel', 'apellidos': 'García', 'parq': '11', 'cedula': '111111111', 'celular': '111-111-1111', 'direccion': 'calle 50 #40-30', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '104', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '101', 'bloque': '2', 'nombres': 'Pedro', 'apellidos': 'Rodriguez', 'parq': '21', 'cedula': '111222333', 'celular': '111-222-333', 'direccion': 'carrera 75 #34-20', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '102', 'bloque': '2', 'nombres': 'Luisa', 'apellidos': 'Martinez', 'parq': '34', 'cedula': '444555666', 'celular': '444-555-666', 'direccion': 'carrera 80 #40-15', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '101', 'bloque': '3', 'nombres': 'Carlos', 'apellidos': 'Gonzalez', 'parq': '45', 'cedula': '555666777', 'celular': '555-666-777', 'direccion': 'avenida 5 #25-10', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '102', 'bloque': '3', 'nombres': 'Ana', 'apellidos': 'Lopez', 'parq': '57', 'cedula': '666777888', 'celular': '666-777-888', 'direccion': 'carrera 85 #30-50', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '101', 'bloque': '4', 'nombres': 'Sofia', 'apellidos': 'Hernandez', 'parq': '61', 'cedula': '777888999', 'celular': '777-888-999', 'direccion': 'carrera 90 #45-60', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '102', 'bloque': '4', 'nombres': 'Javier', 'apellidos': 'Diaz', 'parq': '72', 'cedula': '888999000', 'celular': '888-999-000', 'direccion': 'calle 70 #20-35', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '101', 'bloque': '5', 'nombres': 'Laura', 'apellidos': 'Ramirez', 'parq': '85', 'cedula': '999000111', 'celular': '999-000-111', 'direccion': 'carrera 95 #15-25', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 1, 'apto': '102', 'bloque': '5', 'nombres': 'Daniel', 'apellidos': 'Santos', 'parq': '95', 'cedula': '123789456', 'celular': '123-789-456', 'direccion': 'avenida 10 #40-55', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 2, 'apto': '111', 'bloque': '1', 'nombres': 'Miguel', 'apellidos': 'García', 'parq': '11', 'cedula': '111111111', 'celular': '111-111-1111', 'direccion': 'calle 50 #40-30', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 2, 'apto': '112', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 2, 'apto': '113', 'bloque': '2', 'nombres': 'Adrián', 'apellidos': 'Martínez', 'parq': '22', 'cedula': '333333333', 'celular': '333-333-3333', 'direccion': 'avenida 70 #55-40', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 2, 'apto': '114', 'bloque': '2', 'nombres': 'Paula', 'apellidos': 'Díaz', 'parq': '24', 'cedula': '444444444', 'celular': '444-444-4444', 'direccion': 'carrera 80 #60-35', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 2, 'apto': '115', 'bloque': '3', 'nombres': 'Gabriel', 'apellidos': 'Ramírez', 'parq': None, 'cedula': '555555555', 'celular': '555-555-5555', 'direccion': 'calle 90 #70-50', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 3, 'apto': '101', 'bloque': '5', 'nombres': 'Laura', 'apellidos': 'Ramirez', 'parq': '85', 'cedula': '999000111', 'celular': '999-000-111', 'direccion': 'carrera 95 #15-25', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 4, 'apto': '102', 'bloque': '5', 'nombres': 'Daniel', 'apellidos': 'Santos', 'parq': '95', 'cedula': '123789456', 'celular': '123-789-456', 'direccion': 'avenida 10 #40-55', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 5, 'apto': '112', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 6, 'apto': '113', 'bloque': '2', 'nombres': 'Adrián', 'apellidos': 'Martínez', 'parq': '22', 'cedula': '333333333', 'celular': '333-333-3333', 'direccion': 'avenida 70 #55-40', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 7, 'apto': '104', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 8, 'apto': '101', 'bloque': '2', 'nombres': 'Pedro', 'apellidos': 'Rodriguez', 'parq': '21', 'cedula': '111222333', 'celular': '111-222-333', 'direccion': 'carrera 75 #34-20', 'correo': 'juan@gmail.com', 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0},
    {'edificio_id': 8, 'apto': '102', 'bloque': '2', 'nombres': 'Luisa', 'apellidos': 'Martinez', 'parq': '34', 'cedula': '444555666', 'celular': '444-555-666', 'direccion': 'carrera 80 #40-15', 'correo': None, 'valoradmin': 100, 'valorparq': 50, 'cuotaextra': 0}
]

CuentasCobrar = [
    {'edificio_id': 1, 'apto': '101', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 500, 'CuotaAMD': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'activa'},
    {'edificio_id': 1, 'apto': '102', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 600, 'CuotaAMD': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'anulado'},
    {'edificio_id': 1, 'apto': '103', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 700, 'CuotaAMD': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'anulado'},
    {'edificio_id': 1, 'apto': '104', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 800, 'CuotaAMD': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'activa'},
    {'edificio_id': 1, 'apto': '105', 'bloque': '2', 'fecha': '2024-02-16', 'CXC': 900, 'CuotaAMD': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'activa'}
]

CuentasCobrarZC = [
    {'edificio_id': 1, 'parq': '11', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 500, 'CuotaPAQ': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'activa'},
    {'edificio_id': 1, 'parq': '13', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 600, 'CuotaPAQ': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'anulado'},
    {'edificio_id': 1, 'parq': '16', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 700, 'CuotaPAQ': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'anulado'},
    {'edificio_id': 1, 'parq': '32', 'bloque': '1', 'fecha': '2024-02-16', 'CXC': 800, 'CuotaPAQ': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'activa'},
    {'edificio_id': 1, 'parq': '12', 'bloque': '2', 'fecha': '2024-02-16', 'CXC': 900, 'CuotaPAQ': 500, 'Interes': 200, 'Multa': 100, 'CuotaExtra': 700,'ValorTotal': 1500, 'estado': 'activa'}
]

RecivoCobro =[
    {'edificio_id': 1, 'apto': '101', 'fecha': '2024-02-16', 'banco': 'Banco A', 'tipopago': 1, 'estado': 'activa', 'valor': 1000},
    {'edificio_id': 1, 'apto': '101', 'fecha': '2024-02-16', 'banco': 'Banco A', 'tipopago': 1, 'estado': 'anulado', 'valor': 1000}

]
#1 trasferencias  2 web  3 efectivo

RecivoCobroZC = [
    {'edificio_id': 1, 'parq': '101', 'fecha': '2024-02-16', 'banco': 'Banco A', 'tipopago': 1, 'estado': 'activa', 'valor': 1000},
    {'edificio_id': 1, 'parq': '101', 'fecha': '2024-02-16', 'banco': 'Banco A', 'tipopago': 1, 'estado': 'anulado', 'valor': 1000}
]

# Insertar datos de prueba en la tabla Usuarios
for usuario in usuarios:
    cursor.execute("INSERT INTO Usuarios (username, correo, password) VALUES (?, ?, ?)", tuple(usuario.values()))

# Insertar datos de prueba en la tabla Edificios
for edificio in edificios:
    cursor.execute("INSERT INTO Edificios (usuario_id, edificio_id, nombre, apartamentos, direccion, nit) VALUES (?, ?, ?, ?, ?, ?)", tuple(edificio.values()))

# Insertar datos de prueba en la tabla Propietarios
for propietario in propietarios:
    cursor.execute("INSERT INTO Propietarios (edificio_id, apto, bloque, nombres, apellidos, parq, cedula, celular, direccion, correo, valoradmin, valorparq, cuotaextra) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(propietario.values()))

# Insertar datos de prueba en la tabla transacciones
for CuentasCobrar in CuentasCobrar:
    cursor.execute("INSERT INTO CuentasCobrar (edificio_id, apto, bloque, fecha, CXC, CuotaAMD, Interes, Multa, CuotaExtra, ValorTotal, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(CuentasCobrar.values()))

# Insertar datos de prueba en la tabla transaccionesZC
for CuentasCobrarZC in CuentasCobrarZC:
    cursor.execute("INSERT INTO CuentasCobrarZC (edificio_id, parq, bloque, fecha, CXC, CuotaPAQ, Interes, Multa, CuotaExtra, ValorTotal, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(CuentasCobrarZC.values()))

# Insertar datos de prueba en la tabla recibo_cobro
for RecivoCobro in RecivoCobro:
    cursor.execute("INSERT INTO ReciboCobro (edificio_id, apto, fecha, banco, tipopago, estado, valor) VALUES (?, ?, ?, ?, ?, ?, ?)", tuple(RecivoCobro.values()))
                   
# Insertar datos de prueba en la tabla recibo_cobro_zc
for RecivoCobroZC in RecivoCobroZC:
    cursor.execute("INSERT INTO ReciboCobroZC (edificio_id, parq, fecha, banco, tipopago, estado, valor) VALUES (?, ?, ?, ?, ?, ?, ?)", tuple(RecivoCobroZC.values()))

# Guardar los cambios
conn.commit()
# Cerrar la conexión con la base de datos
conn.close()

print("Datos subidos correctamente.")
