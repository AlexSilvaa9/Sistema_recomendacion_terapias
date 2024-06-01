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

# Obtener DNIs de médicos existentes
cursor.execute("SELECT dni FROM medico")
medicos = cursor.fetchall()

# Obtener códigos de terapias existentes
cursor.execute("SELECT codigo_de_terapia FROM terapia")
terapias = cursor.fetchall()

# Generar y añadir registros a la tabla prescripcion
num_registros = 11000  # Puedes cambiar el número de registros que deseas insertar aquí

start_time = time.time()
for i in range(1, num_registros + 1):
    fecha_inicio = time.strftime('%Y-%m-%d', time.localtime(random.randint(0, int(time.time()))))
    paciente_dni = random.choice(pacientes)[0]
    medico_dni = random.choice(medicos)[0]
    terapia_codigo = random.choice(terapias)[0]
    insert_query = "INSERT INTO prescripcion (fecha_inicio, validacion, paciente_dni, medico_dni, terapia_codigo_de_terapia) VALUES (%s, 0, %s, %s, %s)"
    cursor.execute(insert_query, (fecha_inicio, paciente_dni, medico_dni, terapia_codigo))
    if i % 1000 == 0:
        connection.commit()  # Hacer commit cada 1000 inserciones
        print(f"Insertadas {i} prescripciones.")

connection.commit() # Hacer commit de las inserciones restantes
print(f"¡Se añadieron {num_registros} prescripciones correctamente!")
print("Tiempo transcurrido:", time.time() - start_time)

# Cerrar cursor y conexión
cursor.close()
connection.close()
