import mysql.connector as conector
import time
import random
import string

# Lista de palabras para generar descripciones
palabras_descripcion = [
    "terapia de relajación", "terapia cognitivo-conductual", "terapia física", "terapia ocupacional", 
    "terapia de grupo", "terapia familiar", "terapia de pareja", "terapia de exposición", 
    "terapia de aceptación y compromiso", "terapia de arte", "terapia musical", "terapia de juego", 
    "terapia psicoanalítica", "terapia humanista", "terapia gestáltica", "terapia breve",
    "terapia de luz", "terapia de sonido", "terapia con animales", "terapia con plantas", 
    "terapia acuática", "terapia de masajes", "terapia de calor", "terapia de frío", 
    "terapia de aroma", "terapia magnética", "terapia de yoga", "terapia de meditación", 
    "terapia de hipnosis", "terapia de reflexología", "terapia de acupuntura", "terapia de biofeedback", 
    "terapia de estimulación eléctrica", "terapia de realidad virtual"
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


# Generar y añadir un número de filas a la tabla
num_filas = 11000  # Puedes cambiar el número de filas que deseas insertar aquí

start_time = time.time()
for i in range(1, num_filas + 1):
    codigo_terapia = ''.join(random.choices(string.ascii_uppercase, k=10))
    descripcion = ' '.join(random.sample(palabras_descripcion, random.randint(1, 3)))
    duracion = random.randint(30, 180)  # Duración en minutos
    insert_query = "INSERT INTO terapia (codigo_de_terapia, descripcion, duracion) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (codigo_terapia, descripcion, duracion))
    if i % 1000 == 0:
        connection.commit()  # Hacer commit cada 1000 inserciones
        print(f"Insertadas {i} filas.")

connection.commit()  # Hacer commit de las inserciones restantes
print(f"¡Se añadieron {num_filas} filas correctamente!")
print("Tiempo transcurrido:", time.time() - start_time)

# Cerrar cursor y conexión
cursor.close()
connection.close()
