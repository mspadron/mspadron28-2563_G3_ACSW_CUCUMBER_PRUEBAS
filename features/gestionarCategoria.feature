# Created by MATIAS at 6/1/2025
Feature: Gestionar Categoria

  Scenario: Crear una categoria nueva
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashCategoria
    When Se selecciona el botón para crear una nueva categoria
    And Se completa el formulario para la nueva categoria
    And Se guarda la nueva categoria
    Then Se verifica que la categoria "TestCategory" fue creado correctamente

  Scenario: Editar una categoria en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashCategoria
    When Se selecciona el botón para editar una categoria
    And Se edita el nombre de la categoria de TestCategory a TestCategoryUpdated
    And Se guarda la categoria editada
    Then Se verifica que la categoria fue editada correctamente

  Scenario: Eliminar una categoria en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashCategoria
    When Se selecciona el botón para eliminar una categoria
    And Se confirma la eliminación de la categoria
    Then Se verifica que la categoria fue eliminada correctamente