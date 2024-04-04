import mysql.connector
import time
import pandas as pd
from tabulate import tabulate
def consulta_tiempo(consulta, cursor):
    tiempo_inicial = time.time()  # Obtener tiempo inicial en segundos
    cursor.execute(consulta)
    cursor.fetchall()
    tiempo_final = (time.time() - tiempo_inicial) * 1000  # Calcular tiempo transcurrido en milisegundos
    return tiempo_final
def cambia_storage(cursor,tablas,type):
    for tabla in tablas:
        cursor.execute(f"ALTER TABLE `Recomendacion_terapias`.`{tabla}` ENGINE = {type};")
#####!!!!El try esta porque se va a intentar crear indices en tablas donde no existe algun campo
def add_indice_simple(cursor,tablas,campo):
    for tabla in tablas:
        try:
            cursor.execute(f"CREATE INDEX `{campo}` ON `Recomendacion_terapias`.`{tabla}` (`{campo}` ASC);")
        except mysql.connector.Error as error:
            print("Error al ejecutar la consulta:", error)
def remove_indice_simple(cursor,tablas,campo):
    try:
        for tabla in tablas:
            cursor.execute(f"DROP INDEX `{campo}` ON `Recomendacion_terapias`.`{tabla}`;")
    except mysql.connector.Error as error:
            print("Error al ejecutar la consulta:", error)
def filas_devueltas_por_examinadas(consulta, cursor):
    cursor.execute(consulta)
    filas_devueltas = len(cursor.fetchall())    
    cursor.execute("Explain "+consulta)
    filas = cursor.fetchall()
    tuplas_examinadas = sum([fila[9]for fila in filas])
    return filas_devueltas / tuplas_examinadas
def elimina_foreing_keys(cursor):
    try:
        cursor.execute("ALTER TABLE paciente_enfermedad DROP FOREIGN KEY paciente_enfermedad_ibfk_1;")
        cursor.execute("ALTER TABLE paciente_enfermedad DROP FOREIGN KEY paciente_enfermedad_ibfk_2;")
        cursor.execute("ALTER TABLE paciente_enfermedad DROP FOREIGN KEY FK_Paciente_Enfermedad_Enfermedad;")

        cursor.execute("ALTER TABLE prescripcion DROP FOREIGN KEY prescripcion_ibfk_1;")
        cursor.execute("ALTER TABLE prescripcion DROP FOREIGN KEY prescripcion_ibfk_2;")
        cursor.execute("ALTER TABLE prescripcion DROP FOREIGN KEY prescripcion_ibfk_3;")
    except mysql.connector.Error as error:
        print("Error al eliminar las foreign keys:", error)

def añade_foreing_keys(cursor):
    try:
        cursor.execute("ALTER TABLE paciente_enfermedad ADD CONSTRAINT paciente_enfermedad_ibfk_1 FOREIGN KEY (paciente_dni) REFERENCES paciente(dni);")
        cursor.execute("ALTER TABLE paciente_enfermedad ADD CONSTRAINT paciente_enfermedad_ibfk_2 FOREIGN KEY (enfermedad_codigo_enfermedad) REFERENCES enfermedad(codigo_enfermedad);")
        cursor.execute("ALTER TABLE prescripcion ADD CONSTRAINT prescripcion_ibfk_1 FOREIGN KEY (paciente_dni) REFERENCES paciente(dni);")
        cursor.execute("ALTER TABLE prescripcion ADD CONSTRAINT prescripcion_ibfk_2 FOREIGN KEY (medico_dni) REFERENCES medico(dni);")
        cursor.execute("ALTER TABLE prescripcion ADD CONSTRAINT prescripcion_ibfk_3 FOREIGN KEY (terapia_codigo_de_terapia) REFERENCES terapia(codigo_de_terapia);")
    except mysql.connector.Error as error:
        print("Error al añadir las foreign keys:", error)


# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Es3cuele",
    database="Recomendacion_terapias"
)

# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

variables = {} 

# -- consulta para coger las enfermedades de una persona
consulta1="Select dni,descripcion from paciente p,paciente_enfermedad pe,enfermedad e where p.dni=pe.paciente_dni and pe.enfermedad_codigo_enfermedad=e.codigo_enfermedad and p.dni=95592093;"

# -- consulta para coger las terapias de una persona 
consulta2="select p.dni,t.codigo_de_terapia,t.descripcion,t.duracion, pr.fecha_inicio from paciente p,prescripcion pr, terapia t where p.dni=pr.paciente_dni and pr.terapia_codigo_de_terapia=t.codigo_de_terapia and p.dni=95592093 order by pr.fecha_inicio desc;"

# -- consulta para coger las terapias de una persona validadas para que el paciente la pueda ver
consulta3="select p.dni,t.codigo_de_terapia,t.descripcion,t.duracion from paciente p,prescripcion pr, terapia t where p.dni=pr.paciente_dni and pr.terapia_codigo_de_terapia=t.codigo_de_terapia and pr.validacion=1 and p.dni=95592093;"
elimina_foreing_keys(cursor)
try:
    engines = ["InnoDB","MyISAM"]
    tablas=["enfermedad","medico","paciente","paciente_enfermedad","persona","prescripcion","terapia"]
    for engine in engines:
        print(f"\nProbando con el motor de almacenamiento {engine}:")
        cambia_storage(cursor,tablas,engine)
        
        # Consulta 1 sin índices
        consulta1_sin_indice = f"1_{engine}"
        variables[consulta1_sin_indice] = consulta_tiempo(consulta1, cursor)
        
        # Consulta 2 sin índices
        consulta2_sin_indice = f"2_{engine}"
        variables[consulta2_sin_indice] = consulta_tiempo(consulta2, cursor)

        # Consulta 3 sin índices
        consulta3_sin_indice = f"3_{engine}"
        variables[consulta3_sin_indice] = consulta_tiempo(consulta3, cursor)

       
        # Calcular filas devueltas por examinadas para cada consulta

        variables[f"sin_indice_{consulta1_sin_indice}_relacion"] = filas_devueltas_por_examinadas(consulta1, cursor)
        variables[f"sin_indice_{consulta2_sin_indice}_relacion"] = filas_devueltas_por_examinadas(consulta2, cursor)
        variables[f"sin_indice_{consulta3_sin_indice}_relacion"] = filas_devueltas_por_examinadas(consulta3, cursor)
        
 


        indices = ["terapia_codigo_de_terapia","paciente_dni","codigo_de_terapia","dni","validacion","enfermedad_codigo_enfermedad","codigo_enfermedad"]
        for indice in indices:
            add_indice_simple(cursor,tablas,indice)

            # Consulta 1 con índice
            consulta1_con_indice = f"1_{engine}_con_indice_{indice}"
            variables[consulta1_con_indice] = consulta_tiempo(consulta1, cursor)
            variables[f"{consulta1_con_indice}_relacion"] = filas_devueltas_por_examinadas(consulta1, cursor)
            
            # Consulta 2 con índice
            consulta2_con_indice = f"2_{engine}_con_indice_{indice}"
            variables[consulta2_con_indice] = consulta_tiempo(consulta2, cursor)
            variables[f"{consulta2_con_indice}_relacion"] = filas_devueltas_por_examinadas(consulta2, cursor)
            
            # Consulta 3 con índice
            consulta3_con_indice = f"3_{engine}_con_indice_{indice}"
            variables[consulta3_con_indice] = consulta_tiempo(consulta3, cursor)
            variables[f"{consulta3_con_indice}_relacion"] = filas_devueltas_por_examinadas(consulta3, cursor)
            
            
            # Eliminar índice
            remove_indice_simple(cursor,tablas,indice)
except mysql.connector.Error as error:
    print("Error al ejecutar la consulta:", error)
cambia_storage(cursor,tablas,"InnoDB")

añade_foreing_keys(cursor)
# Cerrar el cursor y la conexión
cursor.close()
conexion.close()

# Crear DataFrames separados para cada consulta
df_consulta1 = pd.DataFrame.from_dict({k: v for k, v in variables.items() if '1_' in k and '_relacion' not in k}, orient='index', columns=['Tiempo'])
df_consulta2 = pd.DataFrame.from_dict({k: v for k, v in variables.items() if '2_' in k and '_relacion' not in k}, orient='index', columns=['Tiempo'])
df_consulta3 = pd.DataFrame.from_dict({k: v for k, v in variables.items() if '3_' in k and '_relacion' not in k}, orient='index', columns=['Tiempo'])
# Agregar una columna 'Engine' a cada DataFrame
df_consulta1['Engine'] = [name.split('_')[1] for name in df_consulta1.index]
df_consulta2['Engine'] = [name.split('_')[1] for name in df_consulta2.index]
df_consulta3['Engine'] = [name.split('_')[1] for name in df_consulta3.index]

# Agregar una columna 'Índice' a cada DataFrame
df_consulta1['Índice'] = ['sin índice' if 'sin_indice' in name else name.split('_')[-1] for name in df_consulta1.index]
df_consulta2['Índice'] = ['sin índice' if 'sin_indice' in name else name.split('_')[-1] for name in df_consulta2.index]
df_consulta3['Índice'] = ['sin índice' if 'sin_indice' in name else name.split('_')[-1] for name in df_consulta3.index]

# Reorganizar los DataFrames para que coincidan con la estructura que deseas
df_consulta1 = df_consulta1.pivot_table(index='Índice', columns='Engine', values='Tiempo', aggfunc='first').reset_index()
df_consulta2 = df_consulta2.pivot_table(index='Índice', columns='Engine', values='Tiempo', aggfunc='first').reset_index()
df_consulta3 = df_consulta3.pivot_table(index='Índice', columns='Engine', values='Tiempo', aggfunc='first').reset_index()

# Renombrar las columnas
df_consulta1.columns.name = None
df_consulta2.columns.name = None
df_consulta3.columns.name = None

# Imprimir los DataFrames para cada consulta
print("Consulta 1:")
print(tabulate(df_consulta1, headers='keys', tablefmt='fancy_grid'))

# Imprimir el DataFrame de consulta 2
print("\nConsulta 2:")
print(tabulate(df_consulta2, headers='keys', tablefmt='fancy_grid'))

# Imprimir el DataFrame de consulta 3
print("\nConsulta 3:")
print(tabulate(df_consulta3, headers='keys', tablefmt='fancy_grid'))


# Tablas de relaciones
relaciones_consulta1 = pd.DataFrame.from_dict({k: v for k, v in variables.items() if '1_' in k and '_relacion' in k}, orient='index', columns=['Relación'])
relaciones_consulta2 = pd.DataFrame.from_dict({k: v for k, v in variables.items() if '2_' in k and '_relacion' in k}, orient='index', columns=['Relación'])
relaciones_consulta3 = pd.DataFrame.from_dict({k: v for k, v in variables.items() if '3_' in k and '_relacion' in k}, orient='index', columns=['Relación'])
# Agregar una columna 'Engine' a cada DataFrame
relaciones_consulta1['Engine'] = [name.split('_')[3]if 'sin_indice' in name else name.split('_')[1] for name in relaciones_consulta1.index]
relaciones_consulta2['Engine'] = [name.split('_')[3]if 'sin_indice' in name else name.split('_')[1]for name in relaciones_consulta2.index]
relaciones_consulta3['Engine'] = [name.split('_')[3]if 'sin_indice' in name else name.split('_')[1]for name in relaciones_consulta3.index]

# Agregar una columna 'Índice' a cada DataFrame
relaciones_consulta1['Índice'] = ['sin índice' if 'sin_indice' in name else name.split('_')[-2] for name in relaciones_consulta1.index]
relaciones_consulta2['Índice'] = ['sin índice' if 'sin_indice' in name else name.split('_')[-2] for name in relaciones_consulta2.index]
relaciones_consulta3['Índice'] = ['sin índice' if 'sin_indice' in name else name.split('_')[-2] for name in relaciones_consulta3.index]

# Renombrar las columnas
relaciones_consulta1.columns.name = None
relaciones_consulta2.columns.name = None
relaciones_consulta3.columns.name = None

# Imprimir los DataFrames de relaciones
print("\nRelaciones Consulta 1:")
print(tabulate(relaciones_consulta1, headers='keys', tablefmt='fancy_grid'))

print("\nRelaciones Consulta 2:")
print(tabulate(relaciones_consulta2, headers='keys', tablefmt='fancy_grid'))

print("\nRelaciones Consulta 3:")
print(tabulate(relaciones_consulta3, headers='keys', tablefmt='fancy_grid'))

