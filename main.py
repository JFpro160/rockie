from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector  # Para conectarse a Aurora
from mysql.connector import Error
import os

AURORA_DB_IP = os.environ.get("AURORA_DB_IP")
AURORA_DB_USER = os.environ.get("AURORA_DB_USER")
AURORA_DB_PASSWORD = os.environ.get("AURORA_DB_PASSWORD")
AURORA_DB_NAME = os.environ.get("AURORA_DB_NAME")

app = FastAPI()

# Modelo de datos de rockie
class Rockie(BaseModel):
    id_estudiante: int
    nombre: str
    sombrero: Optional[str] = None
    cara: Optional[str] = None
    cuerpo: Optional[str] = None
    mano: Optional[str] = None

# Conectar a la base de datos Aurora (MySQL)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=AURORA_DB_IP,
            user=AURORA_DB_USER,
            password=AURORA_DB_PASSWORD,
            database=AURORA_DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")

# Endpoint GET para obtener la información de un rockie por ID desde Aurora
@app.get("/rockie/{id_estudiante}", response_model=Rockie)
def obtener_rockie(id_estudiante: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM rockies WHERE id_estudiante = %s"
    cursor.execute(query, (id_estudiante,))
    rockie = cursor.fetchone()
    
    if rockie:
        return rockie
    else:
        raise HTTPException(status_code=404, detail="Rockie no encontrado")

# Endpoint POST para crear un nuevo rockie en Aurora
@app.post("/rockie/", response_model=Rockie)
def crear_rockie(rockie: Rockie):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO rockies (id_estudiante, nombre, sombrero, cara, cuerpo, mano) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (rockie.id_estudiante, rockie.nombre, rockie.sombrero, rockie.cara, rockie.cuerpo, rockie.mano)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        return rockie
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el rockie: {e}")

# Endpoint PUT para actualizar los datos de un rockie en Aurora
@app.put("/rockie/{id_estudiante}", response_model=Rockie)
def actualizar_rockie(id_estudiante: int, rockie: Rockie):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE rockies 
    SET nombre = %s, sombrero = %s, cara = %s, cuerpo = %s, mano = %s
    WHERE id_estudiante = %s
    """
    values = (rockie.nombre, rockie.sombrero, rockie.cara, rockie.cuerpo, rockie.mano, id_estudiante)
    
    cursor.execute(query, values)
    connection.commit()
    
    return rockie


