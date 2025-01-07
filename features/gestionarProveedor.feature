# Created by MATIAS at 6/1/2025
Feature: Gestionar Proveedor

  Scenario: Crear una proveedor
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashProveedor
    When Se selecciona el botón para crear un nuevo proveedor
    And Se completa el formulario para el nuevo proveedor
    And Se guarda el nuevo proveedor
    Then Se verifica que el proveedor fue creado correctamente

  Scenario: Editar un proveedor en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashProveedor
    When Se selecciona el botón para editar un proveedor
    And Se edita el nombre del proveedor
    And Se guarda el proveedor editado
    Then Se verifica que el proveedor fue editado correctamente

  Scenario: Eliminar una categoria en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashProveedor
    When Se selecciona el botón para eliminar un proveedor
    And Se confirma la eliminación del proveedor
    Then Se verifica que el proveedor fue eliminado correctamente