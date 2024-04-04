import mysql.connector as conector
import time
import random
import string

# Lista de palabras para generar descripciones
palabras_descripcion = [
    "dolor", "fiebre", "tos", "dolor de cabeza", "fatiga", "náuseas", "vómitos", 
    "dolor de garganta", "diarrea", "mareos", "dolor de estómago", "estornudos", 
    "insomnio", "debilidad", "sudoración", "escalofríos", "conjuntivitis", "dolor de espalda",
    "alergias", "asma", "bronquitis", "artritis", "gastritis", "conjuntivitis", 
    "infección", "hipertensión", "migraña", "obesidad", "osteoporosis", "psoriasis",
    "depresión", "ansiedad", "diabetes", "cáncer", "hipotiroidismo", "hipertiroidismo",
    "cabeza", "cuello", "hombro", "brazo", "codo", "muñeca", "mano", "dedo", "pecho",
    "espalda", "cintura", "cadera", "pierna", "rodilla", "tobillo", "pie", "dedo del pie", 
    "ojo", "nariz", "boca", "labio", "diente", "lengua", "cara", "oreja"
]

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

# Generar y añadir un millón de filas a la tabla
start_time = time.time()
for i in range(1, 11000):
    codigo_enfermedad = ''.join(random.choices(string.ascii_uppercase, k=10))
    descripcion = ' '.join(random.sample(palabras_descripcion, random.randint(1, 3)))
    insert_query = "INSERT INTO enfermedad (codigo_enfermedad, descripcion) VALUES (%s, %s)"
    cursor.execute(insert_query, (codigo_enfermedad, descripcion))
    if i % 1000 == 0:
        connection.commit()  # Hacer commit cada 1000 inserciones
        print(f"Insertadas {i} filas.")

connection.commit()  # Hacer commit de las inserciones restantes
print("¡Se añadieron filas correctamente!")
print("Tiempo transcurrido:", time.time() - start_time)

# Cerrar cursor y conexión
cursor.close()
connection.close()
