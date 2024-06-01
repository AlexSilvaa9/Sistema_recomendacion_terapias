import mysql.connector as conector
import time
import random
import string

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

# Obtener DNIs de pacientes existentes
cursor.execute("SELECT dni FROM paciente")
pacientes = cursor.fetchall()

# Obtener códigos de enfermedades existentes
cursor.execute("SELECT codigo_enfermedad FROM enfermedad")
enfermedades = cursor.fetchall()

# Generar y añadir registros a la tabla paciente_enfermedad
num_registros = 11000  # Puedes cambiar el número de registros que deseas insertar aquí

start_time = time.time()
for i in range(1, num_registros + 1):
    dni_paciente = random.choice(pacientes)[0]
    codigo_enfermedad = random.choice(enfermedades)[0]
    insert_query = "INSERT INTO paciente_enfermedad (paciente_dni, enfermedad_codigo_enfermedad) VALUES (%s, %s)"
    cursor.execute(insert_query, (dni_paciente, codigo_enfermedad))
    if i % 1000 == 0:
        connection.commit()  # Hacer commit cada 1000 inserciones
        print(f"Insertados {i} registros.")

connection.commit()  # Hacer commit de las inserciones restantes
print(f"¡Se añadieron {num_registros} registros correctamente!")
print("Tiempo transcurrido:", time.time() - start_time)

# Cerrar cursor y conexión
cursor.close()
connection.close()
