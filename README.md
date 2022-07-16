# Microservicio Usuarios

# Cómo comenzar:

### Requerimientos:
Python 3.6+

## Cómo instalar FastAPI:
Instalar el entorno virtual venv:
```
python3 -m venv <nombre-del-venv>
```
Activar el entorno virtual usando:
```
source <nombre-del-venv>/bin/activate
```
Instalar las dependencias necesarias:
```
poetry install
```

<u>Consejo</u>: agregar en el archivo .gitignore nombre del venv elegido, para evitar subirlo por error.

## Cómo levantar el servidor usando Docker:

<u> Primero: agregar el archivo .env en el directorio root. </u>

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
