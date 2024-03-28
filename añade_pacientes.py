import mysql.connector as conector
import time
import random
import string

# Lista de palabras para generar nombres y apellidos
nombres = ["Juan", "María", "José", "Ana", "Carlos", "Laura", "David", "Sara", "Daniel", "Elena"]
apellidos = ["García", "Martínez", "López", "González", "Rodríguez", "Fernández", "Pérez", "Sánchez", "Ramírez", "Torres"]

# Establecer la conexión a la base de datos
try:
    connection = conector.connect(
        host="localhost",
        user="root",
        password="Es3cuele",
        database="Recomendacion_terapias"
    )
    print("Conexión a la base de datos 'Recomendacion_terapias' establecida correctamente.")
except conector.Error as err:
    print("Error al conectar:", err)
    exit()

# Crear un cursor
cursor = connection.cursor()

# Generar y añadir un número de pacientes a la tabla
num_pacientes = 11000  # Puedes cambiar el número de pacientes que deseas insertar aquí

start_time = time.time()
for i in range(1, num_pacientes + 1):
    dni = ''.join(random.choices(string.digits, k=8))
    nss = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    telefono = ''.join(random.choices(string.digits, k=9))
    persona_type = 'Paciente'
    # Insertar datos en la tabla persona
    insert_persona_query = "INSERT INTO persona (dni, nombre, apellidos, telefono, persona_type) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_persona_query, (dni, nombre, apellido, telefono, persona_type))
    # Insertar datos en la tabla paciente
    insert_paciente_query = "INSERT INTO paciente (dni, nss) VALUES (%s, %s)"
    cursor.execute(insert_paciente_query, (dni, nss))
    if i % 1000 == 0:
        connection.commit()  # Hacer commit cada 1000 inserciones
        print(f"Insertados {i} pacientes.")

connection.commit()  # Hacer commit de las inserciones restantes
print(f"¡Se añadieron {num_pacientes} pacientes correctamente!")
print("Tiempo transcurrido:", time.time() - start_time)

# Cerrar cursor y conexión
cursor.close()
connection.close()
