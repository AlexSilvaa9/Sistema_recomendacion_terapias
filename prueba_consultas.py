import time
import mysql.connector

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'Es3cuele',
    'host': 'localhost',
    'database': 'Recomendacion_terapias',
    'raise_on_warnings': True
}
def clear_cache():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("FLUSH TABLES")
        print("Caché de la base de datos limpiada correctamente.")
    except mysql.connector.Error as err:
        print("Error al limpiar la caché:", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Consultas antes de la creación de los índices invisibles
queries_before = [
    "SELECT dni, descripcion FROM paciente p, paciente_enfermedad pe, enfermedad e WHERE p.dni=pe.paciente_dni AND pe.enfermedad_codigo_enfermedad=e.codigo_enfermedad AND p.dni='95592093';",
    "SELECT p.dni, t.codigo_de_terapia, t.descripcion, t.duracion, pr.fecha_inicio FROM paciente p, prescripcion pr, terapia t WHERE p.dni=pr.paciente_dni AND pr.terapia_codigo_de_terapia=t.codigo_de_terapia AND p.dni='95592093' ORDER BY pr.fecha_inicio DESC;",
    "SELECT p.dni, t.codigo_de_terapia, t.descripcion, t.duracion FROM paciente p, prescripcion pr, terapia t WHERE p.dni=pr.paciente_dni AND pr.terapia_codigo_de_terapia=t.codigo_de_terapia AND pr.validacion=1 AND p.dni='95592093';"
]

# Consultas después de la creación de los índices invisibles
queries_after = [
    "/*+ INDEX(paciente_enfermedad idx_paciente_dni_enfermedad) INDEX(enfermedad idx_codigo_enfermedad) */ SELECT dni, descripcion FROM paciente p, paciente_enfermedad pe, enfermedad e WHERE p.dni=pe.paciente_dni AND pe.enfermedad_codigo_enfermedad=e.codigo_enfermedad AND p.dni='95592093';",
    "/*+ INDEX(prescripcion idx_paciente_dni_prescripcion) INDEX(terapia idx_codigo_de_terapia) */ SELECT p.dni, t.codigo_de_terapia, t.descripcion, t.duracion, pr.fecha_inicio FROM paciente p, prescripcion pr, terapia t WHERE p.dni=pr.paciente_dni AND pr.terapia_codigo_de_terapia=t.codigo_de_terapia AND p.dni='95592093' ORDER BY pr.fecha_inicio DESC;",
    "/*+ INDEX(prescripcion idx_paciente_dni_validacion) INDEX(terapia idx_codigo_de_terapia) */ SELECT p.dni, t.codigo_de_terapia, t.descripcion, t.duracion FROM paciente p, prescripcion pr, terapia t WHERE p.dni=pr.paciente_dni AND pr.terapia_codigo_de_terapia=t.codigo_de_terapia AND pr.validacion=1 AND p.dni='95592093';"
]

# Función para ejecutar y medir el tiempo de las consultas
def measure_performance(queries, index_name=None):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        for query in queries:
            if index_name:
                query = query.replace('INDEX(index_name)', index_name)
            start_time = time.time()
            cursor.execute(query)
            end_time = time.time()
            print(f"Tiempo de ejecución de la consulta: {end_time - start_time} segundos")
        cursor.close()
    except mysql.connector.Error as err:
        print("Error al conectar:", err)
    finally:
        if connection.is_connected():
            connection.close()
clear_cache
# Medir rendimiento antes de crear los índices invisibles
print("Rendimiento antes de crear los índices invisibles:")
measure_performance(queries_before)

# Crear índices invisibles
# index_creation_queries = [
#     "CREATE INDEX idx_paciente_dni_enfermedad ON paciente_enfermedad(paciente_dni, enfermedad_codigo_enfermedad) INVISIBLE;",
#     "CREATE INDEX idx_paciente_dni_prescripcion ON prescripcion(paciente_dni, terapia_codigo_de_terapia) INVISIBLE;",
#     "CREATE INDEX idx_paciente_dni_validacion ON prescripcion(paciente_dni, validacion, terapia_codigo_de_terapia) INVISIBLE;"
# ]

# try:
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     for query in index_creation_queries:
#         cursor.execute(query)
#     connection.commit()
#     print("Índices invisibles creados correctamente.")
# except mysql.connector.Error as err:
#     print("Error al crear índices invisibles:", err)
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()

# Medir rendimiento después de crear los índices invisibles
print("\nRendimiento después de crear los índices invisibles:")
measure_performance(queries_after)

