# importamos al framework fastapi a nuestro entorno de trabajo
# Importamos la libreria pydantic para manejar los datos y pandas para manejar los datos en formato de tabla
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# Creamos un objeto apartir de la clase FastApi
app = FastAPI()

# Importamos la base de datos con los datos de los estudiantes
df = pd.read_excel("Data50.xlsx")

# Definimos el modelo de datos utilizando Pydantic
class Students(BaseModel): # Este modelo representa la estructura de los datos que vamos a manejar
    NombreCompleto: str
    Matricula: int
    Edad: int
    Carrera: str
    Sexo: str
    Correo: str
    Facultad: str
    AñoExamen: int
    Compañero: bool
    Materia: str

# ------------------------ Instancias de la función get api framework FastApi ------------------
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Nivel 1 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1.- Obtener todos los estudiantes
@app.get("/Estudiantes/") # Nivel 1

async def get_students():
    return df.to_dict(orient="records")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Nivel 2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 2.1.- Obtener cantidad de registros en la columna sexo
@app.get("/Estudiantes/Sexo") 

async def get_students_by_sexo(count: bool = False): # Parametro de consulta para contar los registros 
    if count:
        return (df['Sexo'].value_counts().to_dict())
        
    filtered_df = df['Sexo'].dropna().unique()
    return filtered_df.tolist()

# 2.2.- Obtener estudiantes mujeres
@app.get("/Estudiantes/Mujer") 

async def get_students_women():
    filtered_df = df[df['Sexo'] == 'Mujer']
    return filtered_df.to_dict(orient="records")

# 2.3.- Obtener estudiantes hombres
@app.get("/Estudiantes/Hombre") 

async def get_students_men():
    filtered_df = df[df['Sexo'] == 'Hombre']
    return filtered_df.to_dict(orient="records")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Nivel 3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 3.1.- Obtener lista con cantidad de estudiantes Hombres y Mujeres por carrera
@app.get("/Estudiantes/Sexo/Carrera")
async def get_students_by_sexo_and_carrera():
    grouped_df = df.groupby(['Carrera', 'Sexo']).size().reset_index(name='Cantidad')
    return grouped_df.to_dict(orient="records")

# 3.2.- Obtener Estudiantes hombres de la carrera "Ingeniería en Ciencias de la Computación"
@app.get("/Estudiantes/Hombre/Ingenieria-en-Ciencias-de-la-Computacion")

async def get_students_by_carrera():
    filtered_df = df[(df['Carrera'] == 'Ingeniería en Ciencias de la Computación') & (df['Sexo'] == 'Hombre')]
    return filtered_df.to_dict(orient="records")

# 3.3.- Obtener Estudiantes en general de con quines tome la materia "Diseño de la Interacción"
@app.get("/Estudiantes/Compañero/Diseño-de-la-Interacción")

async def get_students_by_compañero():
    filtered_df = df[(df['Materia'] == 'Diseño de la Interacción') & (df['Compañero'] == 1)]
    return filtered_df.to_dict(orient="records")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Nivel 4 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 4.1.- Obtener las materias que han cursado las es estudiantes Mujeres de la carrera "Ingeniería en Tecnologías de la Información" 
@app.get("/Estudiantes/Mujeres/Ingeniería-en-Tecnologias-de-la-Información/Materia") 

async def get_students_women_ingenieria_tecnologias():
    filtered_df = df[(df['Carrera'] == 'Ingeniería en Tecnologias de la Información') & (df['Sexo'] == 'Mujer')]
    return filtered_df['Materia'].unique().tolist()

# 4.2.- Obtener las materias han cursado los estudiantes Hombres de cualquier carrera
@app.get("/Estudiantes/Hombres/Carrera/Materia") 

async def get_students_men_carrera_class():
    filtered_df = df[df['Sexo'] == 'Hombre']
    return filtered_df['Materia'].unique().tolist()

# 4.3.- Obtener los estudiantes Hombres y Mujeres De la carrera "Ingeniería en Tecnologías de la Información" que han cursado la materia "Redes y Servicios"
@app.get("/Estudiantes/Sexo/Ingeniería-en-Tecnologías-de-la-Información/Redes-y-Servicios") 

async def get_students_by_compañero():
    filtered_df = df[(df['Materia'] == 'Redes y Servicios') & (df['Carrera'] == 'Ingeniería en Tecnologías de la Información')]
    return filtered_df.to_dict(orient="records")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 5 por parametros de ruta >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 5.1.- Obtener estudiantes por seso con parametro de consulta (Extra)
@app.get("/Estudiantes/Sexo/{sexo}") # Nivel 3

async def get_students_by_sexo_param(sexo: str):
    if sexo not in ['Hombre', 'Mujer']:
        return {"error": "Sexo no válido. Debe ser 'Hombre' o 'Mujer'."}
    
    filtered_df = df[df['Sexo'] == sexo]
    return filtered_df.to_dict(orient="records")

# 5.2.- Obtener estudiantes de un sexo especifico que han cursado una materia especifica
@app.get("/Estudiantes/Sexo/{sexo}/Materia/{materia}") # Nivel 5

async def get_students_by_sexo_and_materia(sexo: str, materia: str):
    if sexo not in ['Hombre', 'Mujer']:
        return {"error": "Sexo no válido. Debe ser 'Hombre' o 'Mujer'."}
    elif materia not in df['Materia'].unique():
        return {"error": "Materia no válida. Por favor, verifique el nombre de la materia."}
    
    filtered_df = df[(df['Sexo'] == sexo) & (df['Materia'] == materia)]
    return filtered_df.to_dict(orient="records")

# 5.3.- Obtener estudiantes de un sexo especifico que han cursado una materia especifica de una carrera especifica
@app.get("/Estudiantes/Sexo/{sexo}/Materia/{materia}/Carrera/{carrera}") # Nivel 7

async def get_students_by_sexo_materia_carrera(sexo: str, materia: str, carrera: str):
    if sexo not in ['Hombre', 'Mujer']:
        return {"error": "Sexo no válido. Debe ser 'Hombre' o 'Mujer'."}
    elif materia not in df['Materia'].unique():
        return {"error": "Materia no válida. Por favor, verifique el nombre de la materia."}
    elif carrera not in df['Carrera'].unique():
        return {"error": "Carrera no válida. Por favor, verifique el nombre de la carrera."}

    filtered_df = df[(df['Sexo'] == sexo) & (df['Materia'] == materia) & (df['Carrera'] == carrera)]
    return filtered_df.to_dict(orient="records")