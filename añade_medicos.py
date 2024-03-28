import mysql.connector as conector
import time
import random
import string

# Lista de palabras para generar nombres y apellidos
nombres = ["Juan", "María", "José", "Ana", "Carlos", "Laura", "David", "Sara", "Daniel", "Elena"]
apellidos = ["García", "Martínez", "López", "González", "Rodríguez", "Fernández", "Pérez", "Sánchez", "Ramírez", "Torres"]

# Lista de especialidades médicas
especialidades = ["Cardiología", "Dermatología", "Endocrinología", "Gastroenterología", 
                  "Ginecología", "Neurología", "Oftalmología", "Oncología", 
                  "Ortopedia", "Pediatría", "Psiquiatría", "Radiología", "Urología"]

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

# Generar y añadir un número de médicos a la tabla
num_medicos = 11000  # Puedes cambiar el número de médicos que deseas insertar aquí

start_time = time.time()
for i in range(1, num_medicos + 1):
    dni = ''.join(random.choices(string.digits, k=8))
    especialidad = random.choice(especialidades)
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    telefono = ''.join(random.choices(string.digits, k=9))
    persona_type = 'Medico'
    # Insertar datos en la tabla persona
    insert_persona_query = "INSERT INTO persona (dni, nombre, apellidos, telefono, persona_type) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_persona_query, (dni, nombre, apellido, telefono, persona_type))
    # Insertar datos en la tabla médico
    insert_medico_query = "INSERT INTO medico (dni, especialidad) VALUES (%s, %s)"
    cursor.execute(insert_medico_query, (dni, especialidad))
    if i % 1000 == 0:
        connection.commit()  # Hacer commit cada 1000 inserciones
        print(f"Insertados {i} médicos.")

connection.commit()  # Hacer commit de las inserciones restantes
print(f"¡Se añadieron {num_medicos} médicos correctamente!")
print("Tiempo transcurrido:", time.time() - start_time)

# Cerrar cursor y conexión
cursor.close()
connection.close()
