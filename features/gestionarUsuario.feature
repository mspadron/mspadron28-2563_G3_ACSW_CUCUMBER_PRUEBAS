# Created by MATIAS at 2/1/2025
Feature: Gestionar Usuario

  Scenario: Crear un usuario en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboarduser
    When Se selecciona el botón para crear un nuevo usuario
    And Se completa el formulario de creación con datos válidos
    And Se guarda el nuevo usuario
    Then Se verifica que el usuario "Test_Selenium" fue creado correctamente

  Scenario: Editar un usuario en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboarduser
    When Se selecciona el botón para editar un usuario
    And Se edita el nombre de usuario de Nuria a Test_Edit_Selenium
    And Se guarda el usuario editado
    Then Se verifica que el usuario fue editado correctamente

  Scenario: Eliminar un usuario en el sistema
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboarduser
    When Se selecciona el botón para eliminar un usuario
    And Se confirma la eliminación del usuario
    Then Se verifica que el usuario fue eliminado correctamente
