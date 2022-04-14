Feature: User

  Scenario: 1- Consulto y no hay users existentes - get_all
    Given que no hay users existentes
    When consulto los users
    Then no me muestra ningún user

 Scenario: 2- Camino A: Como usuario, quiero poder agregar users para consultar y comunicar su situación. - create
    Given que necesito crear users al sistema
    When agrego un user
    Then el sistema carga el user con el nombre y otros datos

Scenario: 3- Camino : Como usuario, quiero poder obtener los datos de un user para consultar y comunicar su situación. - get_by_id
  Given  soy un usuario y quiero visualizar la información de un user
  When  solicito la información con el identificador
  Then el sistema muestra el proyecto con todos sus datos

Scenario: 4- Camino B: Como usuario, quiero poder modificar users para actualizar la información. - update
  Given que necesito actualizar la información de un user existente
  When modifico el user
  Then el sistema guarda el user con los campos que le modifiqué

Scenario: Como usuario, quiero poder borrar un user para evitar tener users en desuso.
    Given que quiero tener actualizados los users
    When un user está en desuso y lo elimino
    Then el sistema lo borra y no muestra más su información
