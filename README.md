# Aninfo-Módulo-Proyectos
Módulo Proyectos del sistema para la empresa PSA - Análisis de la Información FIUBA

# Cómo comenzar:

### Requerimientos:
Python 3.6+

### Para completar los pre-commit hooks:
Eliminar la siguiente línea del archivo app/routers/user_controller.py
```
# pylint: skip-file
```

## Cómo instalar FastAPI:
Instalar el entorno virtual venv :
```
python3 -m venv venv
```
Activar el entorno virtual usando:
```
source venv/bin/activate
```
Instalar los paquetes (necesario para manejar dependencias):
```
pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv pydantic[email]
```

## Cómo levantar el servidor usando Docker:

Ir al directorio del proyecto (en donde está el archivo Dockerfile) para hacer build de la imagen de nuestro proyecto:

```
docker-compose build
```

Luego ejecutar el comando:
```
docker-compose up
```

Esto levanta en localhost en el puerto 8000 --> http://0.0.0.0:8000

## Cómo correr las migraciones usando Alembic:
Para generar las migraciones ejecutamos este comando

```
docker-compose run app alembic revision --autogenerate -m "New Migration"
```

Con el flag -m se crea un comentario para la nueva migración.

Luego, una vez hecho esto, hacemos que las migraciones persistan en la base de datos con el siguiente comando:

```
docker-compose run app alembic upgrade head
```
