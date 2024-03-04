

# Diccionario simulado de usuarios y contraseñas
usuarios = {
    'ProAdm': 'admin',
    'Prodos': 'admin',
}

# Base de datos simulada de edificios asociados a usuarios
base_de_datos_edificios = {
    'ProAdm': [
        {'nombre': 'Edificio A', 'apartamentos': 12, 'direccion': 'Calle 123', 'nit': '123456',
            'propietarios': [
                {'id': '101', 'bloque': '1', 'nombre': 'Juan Dario', 'apellido': 'Perez Zapata', 'parq': '12', 'cedula': '123456789', 'numero_celular': '123-456-7890', 'direccion': 'calle 58a #45-45', 'correo':'juan@gmail.com'},
                {'id': '102', 'bloque': '1', 'nombre': 'María Teresa', 'apellido': 'Gomez Castaño', 'parq': '14', 'cedula': '987654321', 'numero_celular': '987-654-3210', 'direccion': 'calle 60 #50-30', 'correo':'juan@gmail.com'},
                {'id': '103', 'bloque': '1', 'nombre': 'Miguel', 'apellido': 'García', 'parq': '11', 'cedula': '111111111', 'numero_celular': '111-111-1111', 'direccion': 'calle 50 #40-30', 'correo':'juan@gmail.com'},
                {'id': '104', 'bloque': '1', 'nombre': 'Elena', 'apellido': 'López', 'parq': '13', 'cedula': '222222222', 'numero_celular': '222-222-2222', 'direccion': 'carrera 60 #45-25', 'correo':'juan@gmail.com'},
                {'id': '101', 'bloque': '2', 'nombre': 'Pedro', 'apellido': 'Rodriguez', 'parq': '21', 'cedula': '111222333', 'numero_celular': '111-222-333', 'direccion': 'carrera 75 #34-20', 'correo':'juan@gmail.com'},
                {'id': '102', 'bloque': '2', 'nombre': 'Luisa', 'apellido': 'Martinez', 'parq': '34', 'cedula': '444555666', 'numero_celular': '444-555-666', 'direccion': 'carrera 80 #40-15'},
                {'id': '101', 'bloque': '3', 'nombre': 'Carlos', 'apellido': 'Gonzalez', 'parq': '45', 'cedula': '555666777', 'numero_celular': '555-666-777', 'direccion': 'avenida 5 #25-10'},
                {'id': '102', 'bloque': '3', 'nombre': 'Ana', 'apellido': 'Lopez', 'parq': '57', 'cedula': '666777888', 'numero_celular': '666-777-888', 'direccion': 'carrera 85 #30-50'},
                {'id': '101', 'bloque': '4', 'nombre': 'Sofia', 'apellido': 'Hernandez', 'parq': '61', 'cedula': '777888999', 'numero_celular': '777-888-999', 'direccion': 'carrera 90 #45-60'},
                {'id': '102', 'bloque': '4', 'nombre': 'Javier', 'apellido': 'Diaz', 'parq': '72', 'cedula': '888999000', 'numero_celular': '888-999-000', 'direccion': 'calle 70 #20-35'},
                {'id': '101', 'bloque': '5', 'nombre': 'Laura', 'apellido': 'Ramirez', 'parq': '85', 'cedula': '999000111', 'numero_celular': '999-000-111', 'direccion': 'carrera 95 #15-25'},
                {'id': '102', 'bloque': '5', 'nombre': 'Daniel', 'apellido': 'Santos', 'parq': '95', 'cedula': '123789456', 'numero_celular': '123-789-456', 'direccion': 'avenida 10 #40-55'}
        ]},
        {'nombre': 'Edificio B', 'apartamentos': 5,  'direccion': 'Avenida 456', 'nit': '789012',
            'propietarios': [
                {'id': '111', 'bloque': '1', 'nombre': 'Miguel', 'apellido': 'García', 'parq': '11', 'cedula': '111111111', 'numero_celular': '111-111-1111', 'direccion': 'calle 50 #40-30'},
                {'id': '112', 'bloque': '1', 'nombre': 'Elena', 'apellido': 'López', 'parq': '13', 'cedula': '222222222', 'numero_celular': '222-222-2222', 'direccion': 'carrera 60 #45-25'},
                {'id': '113', 'bloque': '2', 'nombre': 'Adrián', 'apellido': 'Martínez', 'parq': '22', 'cedula': '333333333', 'numero_celular': '333-333-3333', 'direccion': 'avenida 70 #55-40'},
                {'id': '114', 'bloque': '2', 'nombre': 'Paula', 'apellido': 'Díaz', 'parq': '24', 'cedula': '444444444', 'numero_celular': '444-444-4444', 'direccion': 'carrera 80 #60-35'},
                {'id': '115', 'bloque': '3', 'nombre': 'Gabriel', 'apellido': 'Ramírez', 'parq': '35', 'cedula': '555555555', 'numero_celular': '555-555-5555', 'direccion': 'calle 90 #70-50'}
        ],'cuentas_cobro_adm':[

        ],'resibo_caja_adm':[

        ],'Zonas_comunes':[
                {'id': '38', 'nombre': 'Miguel', 'apellido': 'García', 'cedula': '111111111', 'numero_celular': '111-111-1111', 'direccion': 'calle 50 #40-30'},
        ],'cuentas_cobro_zc':[
        
        ],'resivo_caja_zc':[
        ]
        },
        {'nombre': 'Edificio C', 'apartamentos': 30,  'direccion': 'Carrera 789', 'nit': '131415'},
        {'nombre': 'Edificio D', 'apartamentos': 10,  'direccion': 'Carrera 789', 'nit': '161718'},
        {'nombre': 'Edificio E', 'apartamentos': 110, 'direccion': 'Carrera 789', 'nit': '192021'},
        {'nombre': 'Edificio F', 'apartamentos': 120, 'direccion': 'Carrera 789', 'nit': '222324'},
    ],

    'Prodos': [
        {'nombre': 'Edificio G', 'apartamentos': 70, 'direccion': 'Carrera 789', 'nit': '252627'},
        {'nombre': 'Edificio H', 'apartamentos': 65, 'direccion': 'Carrera 789', 'nit': '282930'},
        {'nombre': 'Edificio I', 'apartamentos': 54, 'direccion': 'Carrera 789', 'nit': '313233'},
    ],
}

