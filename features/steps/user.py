import requests
from behave import *
import json

empty = b'[]'


# Cuando haya que hacer estos tests, habrá que modificar estos bodys.
body2 = """{"nombre": "Catalina", "lider_de_equipo": {"resourceID": 0, "name": "Romina","surname": "Gomez"},"personas_asignadas": [{"resourceID": 0,"name": "Tomas","surname": "Gomez"}],"fecha_inicio": "21/06/2021", "fecha_limite_inicio": "21/07/2021", "fecha_estimada_fin": "21/06/2021"}"""
body3 = """{"nombre": "Franco", "lider_de_equipo": {"resourceID": 10, "name": "Romina","surname": "Gomez"},"personas_asignadas": [{"resourceID": 0,"name": "Tomas","surname": "Gomez"}],"fecha_inicio": "21/06/2021", "fecha_limite_inicio": "21/07/2021", "fecha_estimada_fin": "21/06/2021"}"""
body4 = """{"nombre": "Tomas", "lider_de_equipo": {"resourceID": 10, "name": "Romina","surname": "Gomez"},"personas_asignadas": [{"resourceID": 0,"name": "Tomas","surname": "Gomez"}],"fecha_inicio": "21/06/2021", "fecha_limite_inicio": "21/07/2021", "fecha_estimada_fin": "21/06/2021"}"""
body4Edited = """{"nombre": "Lautaro", "lider_de_equipo": {"resourceID": 10, "name": "Romina","surname": "Gomez"},"personas_asignadas": [{"resourceID": 0,"name": "Tomas","surname": "Gomez"}],"fecha_inicio": "21/06/2021", "fecha_limite_inicio": "21/07/2021", "fecha_estimada_fin": "21/06/2021"}"""
body5 = """{"nombre": "Julieta", "lider_de_equipo": {"resourceID": 10, "name": "Romina","surname": "Gomez"},"personas_asignadas": [{"resourceID": 0,"name": "Tomas","surname": "Gomez"}],"fecha_inicio": "21/06/2021", "fecha_limite_inicio": "21/07/2021", "fecha_estimada_fin": "21/06/2021"}"""
completeApi = 'http://127.0.0.1:8000/users/'


@given('que no hay users existentes')
def no_users(context):
    global apiUrl
    apiUrl = 'http://127.0.0.1:8000/'

@given('que necesito crear users al sistema')
def create_users(context):
    global completeApi
    completeApi = 'http://127.0.0.1:8000/users/'

@given('soy un usuario y quiero visualizar la información de un user')
def view_information(context):
    global id

    bodyJson = json.loads(body3)
    id = requests.post(completeApi, json=bodyJson).content.decode()


@given('que necesito actualizar la información de un user existente')
def update_information(context):
    global id

    bodyJson = json.loads(body4)
    id = requests.post(completeApi, json=bodyJson).content.decode()

@given('que quiero tener actualizados los users')
def update_users(context):
    global id

    bodyJson = json.loads(body5)
    id = requests.post(completeApi, json=bodyJson).content.decode()


@when('consulto los users')
def get_all_users(context):
    global result
    completeApi = apiUrl+"users/"
    result = requests.get(completeApi)

@when('agrego un user')
def add_user(context):
    global result, bodyJson
    bodyJson = json.loads(body2)
    requests.post(completeApi, json = bodyJson)


@when('solicito la información con el identificador')
def user_by_id(context):
    global result
    api = completeApi + id
    result = requests.get(api)

@when('modifico el user')
def modify_user(context):
    global result, url
    url = completeApi + id
    bodyJson = json.loads(body4Edited)
    result = requests.put(url, json = bodyJson)

@when('un user está en desuso y lo elimino')
def delete_user(context):
    global result, url
    url = completeApi + id
    result = requests.delete(url)

@then('no me muestra ningún user')
def not_found_users(context):
    assert result.content == empty

@then('el sistema carga el user con el nombre y otros datos')
def all_information(context):
    result = requests.get(completeApi)
    assert compareJsons(result.content, body2)

@then( 'el sistema muestra el user con todos sus datos')
def all_information(context):
    assert compareJsons(result.content, body3)

@then( 'el sistema guarda el user con los campos que le modifiqué')
def save_user(context):
    result = requests.get(url)
    assert compareJsons(result.content, body4Edited)
    assert not compareJsons(result.content, body4)

@then( 'el sistema lo borra y no muestra más su información')
def delete_user(context):
    result = requests.get(url)
    assert not compareJsons(result.content, body5)

def compareJsons(result, body):
    resultToCompare = result.decode()
    bodyToCompare = body.replace(": ", ":").replace(", ", ",")[0:-1]
    return bodyToCompare in resultToCompare

