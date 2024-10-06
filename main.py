from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector  # Para conectarse a Aurora
from mysql.connector import Error
import os

AURORA_DB_IP = "3.230.28.178"
AURORA_DB_USER = "root"
AURORA_DB_PASSWORD = "utec"
AURORA_DB_NAME = "mysql"
AURORA_DB_PORT = 8002

app = FastAPI()

# Modelo de datos de rockie
class Rockie(BaseModel):
    id_estudiante: int
    nombre: str
    sombrero: Optional[int] = None  # ID del accesorio
    cara: Optional[int] = None  # ID del accesorio
    cuerpo: Optional[int] = None  # ID del accesorio
    mano: Optional[int] = None  # ID del accesorio

# Modelo de datos de accesorio
class Accesorio(BaseModel):
    nombre: str
    tipo: str  # Por ejemplo: sombrero, cara, cuerpo, mano
    dynamo_id: str  # Referencia a la tienda en DynamoDB

# Conectar a la base de datos Aurora (MySQL)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=AURORA_DB_IP,
            user=AURORA_DB_USER,
            password=AURORA_DB_PASSWORD,
            database=AURORA_DB_NAME,
	    port=AURORA_DB_PORT
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")

# ------------------- Endpoints para los Rockies -------------------

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

# ------------------- Endpoints para los Accesorios -------------------

# Endpoint GET para obtener todos los accesorios
@app.get("/accesorios/")
def obtener_accesorios():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM accesorios"
    cursor.execute(query)
    accesorios = cursor.fetchall()
    
    return accesorios

# Endpoint GET para obtener un accesorio por ID
@app.get("/accesorio/{id_accesorio}")
def obtener_accesorio(id_accesorio: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM accesorios WHERE id_accesorio = %s"
    cursor.execute(query, (id_accesorio,))
    accesorio = cursor.fetchone()
    
    if accesorio:
        return accesorio
    else:
        raise HTTPException(status_code=404, detail="Accesorio no encontrado")

# Endpoint POST para crear un nuevo accesorio
@app.post("/accesorio/", response_model=Accesorio)
def crear_accesorio(accesorio: Accesorio):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO accesorios (nombre, tipo, dynamo_id) VALUES (%s, %s, %s)"
    values = (accesorio.nombre, accesorio.tipo, accesorio.dynamo_id)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        return accesorio
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el accesorio: {e}")

# Endpoint PUT para actualizar un accesorio por ID
@app.put("/accesorio/{id_accesorio}", response_model=Accesorio)
def actualizar_accesorio(id_accesorio: int, accesorio: Accesorio):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE accesorios 
    SET nombre = %s, tipo = %s, dynamo_id = %s
    WHERE id_accesorio = %s
    """
    values = (accesorio.nombre, accesorio.tipo, accesorio.dynamo_id, id_accesorio)
    
    cursor.execute(query, values)
    connection.commit()
    
    return accesorio

