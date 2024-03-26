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
            usuario_id INTEGER NOT NULL,
            edificio_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apartamentos INTEGER NOT NULL,
            direccion TEXT NOT NULL,
            porteria TEXT NOT NULL,
            nit TEXT NOT NULL,
            porcentaje INTEGER,
            Banco1 TEXT,
            Banco2 TEXT,
            Banco3 TEXT,
            Banco4 TEXT,
            Banco5 TEXT,
            estrucRC1 TEXT,
            estrucRC2 TEXT,
            estrucRC3 TEXT,
            estrucRC4 TEXT,
            estrucRC5 TEXT,
            UNIQUE(ID)
                   )''')

# Creación de la tabla propietarios
def crear_tabla_propietarios(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Propietarios (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            edificio_id INTEGER NOT NULL,
            apto TEXT NOT NULL,
            bloque TEXT NOT NULL,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            parq TEXT,
            cedula TEXT NOT NULL,
            celular TEXT NOT NULL,
            direccion TEXT NOT NULL,
            correo TEXT,
            cuotaADM REAL,
            cuotaPARQ REAL,
            cuotaEXT REAL,
            multa REAL,
            intereses REAL,
            fecha_emision DATE NOT NULL,
            fecha_vencimiento DATE NOT NULL,
            estado INTEGER,
            FOREIGN KEY (edificio_id) REFERENCES Edificios(edificio_id)
        )''')


def crear_tabla_CuentasCobrar(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS CuentasCobrar (
                id_CXC INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                edificio_id INTEGER NOT NULL,
                fecha_emision DATE NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                estado TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Propietarios(user_id)
            )''')

def crear_tabla_Detalle_CXC(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS CXCDetalle (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                id_CXC INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                monto REAL,
                pagado REAL,
                total REAL,
                descripcion TEXT,
                estado TEXT NOT NULL,
                FOREIGN KEY (id_CXC) REFERENCES CuentasCobrar(id_CXC),
                FOREIGN KEY (user_id) REFERENCES Propietarios(user_id)
            )''')
    
def crear_tabla_ResivosCaja(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS ReciboCaja (
                id_RC INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                edificio_id INTEGER NOT NULL,
                fecha DATE,
                descripcion TEXT,
                tipopago TEXT,
                valor REAL,
                estado TEXT,
                FOREIGN KEY (user_id) REFERENCES Propietarios(user_id)
            )''')

def crear_tabla_Detalle_RC(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS RCDetalles (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                id_RC INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                cruceID INTEGER NOT NULL,
                monto REAL,
                estado TEXT,
                FOREIGN KEY (id_RC) REFERENCES CuentasCobrar(id_RC),
                FOREIGN KEY (user_id) REFERENCES Propietarios(user_id)
            )''')


# Crear tabla de usuarios
crear_tabla_usuarios(cursor)

# Crear tabla de edificios
crear_tabla_edificios(cursor)

# Crear tabla de propietarios
crear_tabla_propietarios(cursor)

# Crear tabla de cuentas de cobro
crear_tabla_CuentasCobrar(cursor)
# Crear tabla de detalles CXC
crear_tabla_Detalle_CXC(cursor)

# Crear tabla de resivos de caja
crear_tabla_ResivosCaja(cursor)
# Crear tabla de detalles RC
crear_tabla_Detalle_RC(cursor)

# Insertar datos en la tabla de usuarios
usuarios = [
    {'username': 'ProAdm','correo': None,'password': 'admin'},
    {'username': 'Prodos','correo': None,'password': 'admin'}
    ]


edificios = [
    {'usuario_id': 'ProAdm', 'edificio_id': 1, 'nombre': 'Edificio A', 'apartamentos': 12, 'direccion': 'Calle 123', 'porteria': '+57-305 3545453', 'nit': '123456', 'porcentaje':'15.1', 'Banco1': 'Bancolombia','Banco2': 'Nequi','Banco3': 'Davivienda','Banco4': 'Daviplata','Banco5': 'Falabella','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'ProAdm', 'edificio_id': 2, 'nombre': 'Edificio B', 'apartamentos': 5, 'direccion': 'Calle 123', 'porteria': '+57-305 3545453', 'nit': '123456', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'ProAdm', 'edificio_id': 3, 'nombre': 'Edificio C', 'apartamentos': 1, 'direccion': 'Calle 123', 'porteria': '+57-305 3545453', 'nit': '123456', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'ProAdm', 'edificio_id': 4, 'nombre': 'Edificio D', 'apartamentos': 1, 'direccion': 'Calle 123', 'porteria': '+57-305 3545453', 'nit': '123456', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'Prodos', 'edificio_id': 5, 'nombre': 'Edificio E', 'apartamentos': 1, 'direccion': 'Calle 456', 'porteria': '+57-305 3545453', 'nit': '789012', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'Prodos', 'edificio_id': 6, 'nombre': 'Edificio F', 'apartamentos': 1, 'direccion': 'Calle 456', 'porteria': '+57-305 3545453', 'nit': '789012', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'Prodos', 'edificio_id': 7, 'nombre': 'Edificio G', 'apartamentos': 1, 'direccion': 'Calle 456', 'porteria': '+57-305 3545453', 'nit': '789012', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',},
    {'usuario_id': 'Prodos', 'edificio_id': 8, 'nombre': 'Edificio H', 'apartamentos': 2, 'direccion': 'Calle 456', 'porteria': '+57-305 3545453', 'nit': '789012', 'porcentaje':'10.0', 'Banco1': '','Banco2': '','Banco3': '','Banco4': '','Banco5': '','estrucRC1':'Multa','estrucRC2':'Intereses','estrucRC3':'Administracion','estrucRC4':'parqueadero','estrucRC5':'Arrendamientos',}
    ]


propietarios = [
    {'edificio_id': 1, 'apto': '101', 'bloque': '1', 'nombres': 'Juan Dario', 'apellidos': 'Perez Zapata', 'parq': '12', 'cedula': '123456789', 'celular': '123-456-7890', 'direccion': 'calle 58a #45-45', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '102', 'bloque': '1', 'nombres': 'María Teresa', 'apellidos': 'Gomez Castaño', 'parq': '14', 'cedula': '987654321', 'celular': '987-654-3210', 'direccion': 'calle 60 #50-30', 'correo': 'maria@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '103', 'bloque': '1', 'nombres': 'Miguel', 'apellidos': 'García', 'parq': '11', 'cedula': '111111111', 'celular': '111-111-1111', 'direccion': 'calle 50 #40-30', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '104', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '101', 'bloque': '2', 'nombres': 'Pedro', 'apellidos': 'Rodriguez', 'parq': '21', 'cedula': '111222333', 'celular': '111-222-333', 'direccion': 'carrera 75 #34-20', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '102', 'bloque': '2', 'nombres': 'Luisa', 'apellidos': 'Martinez', 'parq': '34', 'cedula': '444555666', 'celular': '444-555-666', 'direccion': 'carrera 80 #40-15', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '101', 'bloque': '3', 'nombres': 'Carlos', 'apellidos': 'Gonzalez', 'parq': '45', 'cedula': '555666777', 'celular': '555-666-777', 'direccion': 'avenida 5 #25-10', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '102', 'bloque': '3', 'nombres': 'Ana', 'apellidos': 'Lopez', 'parq': '57', 'cedula': '666777888', 'celular': '666-777-888', 'direccion': 'carrera 85 #30-50', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '101', 'bloque': '4', 'nombres': 'Sofia', 'apellidos': 'Hernandez', 'parq': '61', 'cedula': '777888999', 'celular': '777-888-999', 'direccion': 'carrera 90 #45-60', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '102', 'bloque': '4', 'nombres': 'Javier', 'apellidos': 'Diaz', 'parq': '72', 'cedula': '888999000', 'celular': '888-999-000', 'direccion': 'calle 70 #20-35', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '101', 'bloque': '5', 'nombres': 'Laura', 'apellidos': 'Ramirez', 'parq': '85', 'cedula': '999000111', 'celular': '999-000-111', 'direccion': 'carrera 95 #15-25', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 1, 'apto': '102', 'bloque': '5', 'nombres': 'Daniel', 'apellidos': 'Santos', 'parq': '95', 'cedula': '123789456', 'celular': '123-789-456', 'direccion': 'avenida 10 #40-55', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 2, 'apto': '111', 'bloque': '1', 'nombres': 'Miguel', 'apellidos': 'García', 'parq': '11', 'cedula': '111111111', 'celular': '111-111-1111', 'direccion': 'calle 50 #40-30', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 2, 'apto': '112', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 2, 'apto': '113', 'bloque': '2', 'nombres': 'Adrián', 'apellidos': 'Martínez', 'parq': '22', 'cedula': '333333333', 'celular': '333-333-3333', 'direccion': 'avenida 70 #55-40', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 2, 'apto': '114', 'bloque': '2', 'nombres': 'Paula', 'apellidos': 'Díaz', 'parq': '24', 'cedula': '444444444', 'celular': '444-444-4444', 'direccion': 'carrera 80 #60-35', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 2, 'apto': '115', 'bloque': '3', 'nombres': 'Gabriel', 'apellidos': 'Ramírez', 'parq': None, 'cedula': '555555555', 'celular': '555-555-5555', 'direccion': 'calle 90 #70-50', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': None, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 3, 'apto': '101', 'bloque': '5', 'nombres': 'Laura', 'apellidos': 'Ramirez', 'parq': '85', 'cedula': '999000111', 'celular': '999-000-111', 'direccion': 'carrera 95 #15-25', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 4, 'apto': '102', 'bloque': '5', 'nombres': 'Daniel', 'apellidos': 'Santos', 'parq': '95', 'cedula': '123789456', 'celular': '123-789-456', 'direccion': 'avenida 10 #40-55', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 5, 'apto': '112', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 6, 'apto': '113', 'bloque': '2', 'nombres': 'Adrián', 'apellidos': 'Martínez', 'parq': '22', 'cedula': '333333333', 'celular': '333-333-3333', 'direccion': 'avenida 70 #55-40', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 7, 'apto': '104', 'bloque': '1', 'nombres': 'Elena', 'apellidos': 'López', 'parq': '13', 'cedula': '222222222', 'celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 8, 'apto': '101', 'bloque': '2', 'nombres': 'Pedro', 'apellidos': 'Rodriguez', 'parq': '21', 'cedula': '111222333', 'celular': '111-222-333', 'direccion': 'carrera 75 #34-20', 'correo': 'juan@gmail.com', 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':True},
    {'edificio_id': 8, 'apto': '102', 'bloque': '2', 'nombres': 'Luisa', 'apellidos': 'Martinez', 'parq': '34', 'cedula': '444555666', 'celular': '444-555-666', 'direccion': 'carrera 80 #40-15', 'correo': None, 'cuotaADM': 100, 'cuotaPARQ': 50, 'cuotaEXT': 0, 'multa': 0, 'intereses': 0, 'fecha_emision':'2024-03-10','fecha_vencimiento':'2024-03-31','estado':False}
    ]

CuentasCobrar = [
    {"id_CXC": 1,"user_id": 1, "edificio_id": 1, "fecha_emision": "2024-02-16","fecha_vencimiento": "2024-03-16","estado": "Contabilizado",},
    {"id_CXC": 2,"user_id": 2, "edificio_id": 1, "fecha_emision": "2024-03-01","fecha_vencimiento": "2024-03-31","estado": "Pendiente",},
    {"id_CXC": 3,"user_id": 3, "edificio_id": 1, "fecha_emision": "2024-03-15","fecha_vencimiento": "2024-04-15","estado": "Pendiente",},
    {"id_CXC": 4,"user_id": 4, "edificio_id": 1, "fecha_emision": "2024-03-01","fecha_vencimiento": "2024-03-31","estado": "Anulado",},
    ]

DetallesCXC = [
    {"id_CXC": 1,"user_id": 1,"tipo": "Administracion","monto": 100,"pagado": 0,"total": 100,"descripcion": "Cuota mensual de administración","estado": "Contabilizado",},
    {"id_CXC": 1,"user_id": 1,"tipo": "Parqueadero","monto": 50,"pagado": 0,"total": 50,"descripcion": "Cuota mensual de parqueadero","estado": "Contabilizado",},
    {"id_CXC": 2,"user_id": 2,"tipo": "Administracion","monto": 120,"pagado": 50,"total": 70,"descripcion": "Cuota mensual de administración","estado": "Pendiente",},
    {"id_CXC": 2,"user_id": 2,"tipo": "Parqueadero","monto": 60,"pagado": 0,"total": 60,"descripcion": "Cuota mensual de parqueadero","estado": "Pendiente",},
    {"id_CXC": 3,"user_id": 3,"tipo": "Extraordinario","monto": 200,"pagado": 0,"total": 200,"descripcion": "Mantenimiento de la piscina","estado": "Pendiente",},
    {"id_CXC": 4,"user_id": 4,"tipo": "Administracion","monto": 100,"pagado": 0,"total": 100,"descripcion": "Cuota mensual de administración","estado": "Anulado",},
    {"id_CXC": 4,"user_id": 4,"tipo": "Intereses","monto": 10,"pagado": 0,"total": 10,"descripcion": "Intereses por mora","estado": "Anulado",},
    {"id_CXC": 4,"user_id": 4,"tipo": "Multa","monto": 10,"pagado": 0,"total": 10,"descripcion": "Multa no representacion en junta","estado": "Anulado",},
    ]

ReciboCaja =[
    {'id_RC': 1, 'user_id': 2, "edificio_id": 1, 'fecha': '2024-03-02', 'descripcion': 'Bancolombia', 'tipopago': 'trasferencia', 'valor': 50, 'estado': 'Pendiente'},
    {'id_RC': 2, 'user_id': 3, "edificio_id": 1, 'fecha': '2024-03-02', 'descripcion': 'Bancolombia', 'tipopago': 'trasferencia', 'valor': 50, 'estado': 'Pendiente'},    
    ]

DetallesRC = [
    {"id_RC": 1, "user_id": 2, "cruseID": 3, "monto": 50, "estado": "Pendiente",},
    {"id_RC": 2, "user_id": 3, "cruseID": 3, "monto": 50, "estado": "Pendiente",},
    {"id_RC": 2, "user_id": 3, "cruseID": 3, "monto": 50, "estado": "Pendiente",},
    ]
#1 trasferencias  2 web  3 efectivo

# Insertar datos de prueba en la tabla Usuarios
for usuario in usuarios:
    cursor.execute("""
        INSERT INTO Usuarios (username, correo, password) 
        VALUES (?, ?, ?)""",
        tuple(usuario.values()))

# Insertar datos de prueba en la tabla Edificios
for edificio in edificios:
    cursor.execute("""
        INSERT INTO Edificios (usuario_id, edificio_id, nombre, apartamentos, direccion, porteria, nit, porcentaje, Banco1, Banco2, Banco3, Banco4, Banco5, estrucRC1, estrucRC2 ,estrucRC3 ,estrucRC4 ,estrucRC5) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(edificio.values()))

# Insertar datos de prueba en la tabla Propietarios
for propietario in propietarios:
    cursor.execute("""
        INSERT INTO Propietarios (edificio_id, apto, bloque, nombres, apellidos, parq, cedula, celular, direccion, correo, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento, estado) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)""",
        tuple(propietario.values()))



# Insertar datos de prueba en la tabla CuentasCobrar
for cuenta in CuentasCobrar:
    cursor.execute("""
        INSERT INTO CuentasCobrar (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        tuple(cuenta.values()))

for detallecxc in DetallesCXC:
    cursor.execute("""
        INSERT INTO CXCDetalle (id_CXC, user_id, tipo, monto, pagado, total, descripcion, estado) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(detallecxc.values()))



# Insertar datos en ReciboCaja
for recibo in ReciboCaja:
    cursor.execute("""
        INSERT INTO ReciboCaja (id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(recibo.values()))

# Insertar datos en DetallesRC
for detallerc in DetallesRC:
    cursor.execute("""
        INSERT INTO RCDetalles (id_RC, user_id, cruceID, monto, estado) 
        VALUES (?, ?, ?, ?, ?)""",
        tuple(detallerc.values()))
    
# Guardar los cambios
conn.commit()
# Cerrar la conexión con la base de datos
conn.close()

print("Datos subidos correctamente.")
