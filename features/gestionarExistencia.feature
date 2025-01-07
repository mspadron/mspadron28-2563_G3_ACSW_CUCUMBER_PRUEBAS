# Created by MATIAS at 6/1/2025
Feature: Gestion Existencia

  Scenario: Crear existencia
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboardExistencia
    When Se selecciona el botón para crear una nueva existencia
    And Se completa el formulario para nueva existencia
    And Se guarda nueva existencia
    Then Se verifica que nueva existencia fue creada correctamente

  Scenario: Agregar entrada existencia
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboardExistencia
    When Se selecciona el botón para agregar entrada
    And Se agrega la cantidad
    And Se registra la entrada

  Scenario: Agregar salida existencia
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboardExistencia
    When Se selecciona el botón para agregar salida
    And Se agrega la cantidad salida
    And Se registra la salida