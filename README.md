# API de Rockie en FastAPI

Este proyecto implementa una API en FastAPI para gestionar `Rockies` y sus accesorios, conectándose a una base de datos Aurora (MySQL).

## Requisitos previos

1. **AWS CLI** configurado con tus credenciales y región.
2. **Python 3** instalado en tu sistema.
3. Conexión a una base de datos Aurora (MySQL) ya configurada.
4. **Variables de entorno** configuradas en el sistema operativo:
   - `AURORA_DB_IP`
   - `AURORA_DB_USER`
   - `AURORA_DB_PASSWORD`
   - `AURORA_DB_NAME`

   Puedes configurarlas temporalmente en Linux usando:

   ```bash
   export AURORA_DB_IP=<Tu_IP_de_Aurora>
   export AURORA_DB_USER=<Tu_Usuario_de_Aurora>
   export AURORA_DB_PASSWORD=<Tu_Contraseña_de_Aurora>
   export AURORA_DB_NAME=<Nombre_de_Tu_Base_de_Datos>
   ```

## Configuración del entorno

### 1. Crear un entorno virtual de Python y activar el entorno

```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate
```

### 2. Instalar las dependencias

Asegúrate de tener un archivo `requirements.txt` con las siguientes dependencias:

```txt
fastapi
uvicorn
mysql-connector-python
```

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

## Uso del script de shell para automatizar el proceso

### 1. Hacer que el script sea ejecutable

Primero, asegúrate de que el script de shell sea ejecutable con el siguiente comando:

```bash
chmod +x script.sh
```

### 2. Ejecutar el script de shell

Para automatizar el proceso de creación del entorno, instalación de dependencias y ejecución del servidor FastAPI, ejecuta:

```bash
./script.sh
```

El script hará lo siguiente:

1. Crear un entorno virtual en Python.
2. Instalar las dependencias necesarias desde `requirements.txt`.
3. Ejecutar el servidor FastAPI usando Uvicorn.

### 3. Acceder a la API de Rockie

Una vez que el servidor esté corriendo, puedes acceder a la API en [http://localhost:8000](http://localhost:8000) o la IP pública de la instancia en caso de que esté desplegado.

### 4. Documentación Swagger

Puedes acceder a la documentación generada automáticamente por FastAPI en la siguiente URL:

[http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Borrar los recursos creados

Para detener y borrar la MV de base de datos o los recursos asociados, puedes usar los comandos de AWS CLI como se describió anteriormente.

## Script de Shell

Aquí está el script que automatiza el proceso de creación del entorno y ejecución del servidor FastAPI:

```bash
#!/bin/bash

# Crear un entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Instrucciones para el script de shell:

1. Haz que el script sea ejecutable:

```bash
chmod +x script.sh
```

2. Ejecuta el script:

```bash
./script.sh
