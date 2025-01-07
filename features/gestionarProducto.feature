# Created by MATIAS at 6/1/2025
Feature: Gestionar Producto

  Scenario: Crear producto
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboardProducto
    When Se selecciona el botón para crear un nuevo producto
    And Se completa el formulario para el nuevo producto
    And Se guarda el nuevo producto
    Then Se verifica que el producto fue creado correctamente

  Scenario: Editar un producto
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboardProducto
    When Se selecciona el botón para editar un producto
    And Se edita el nombre de producto de Producto Test Selenium a Producto Updated
    And Se guarda el producto editado
    Then Se verifica que el producto fue editado correctamente

  Scenario: Eliminar un usuario en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboardProducto
    When Se selecciona el botón para eliminar un producto
    And Se confirma la eliminación del producto
    Then Se verifica que el producto fue eliminado correctamente