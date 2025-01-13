# Created by MATIAS at 13/1/2025
Feature: Iniciar Sesión Sistema

  Scenario: Inicio de sesion mediante credenciales invalidas
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales invalidas y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboarduser

  Scenario: Inicio sesión mediante campos vacios en credenciales
    Given Abrir Navegador para inicio sesión
    When Campos vacios de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboarduser

  Scenario: Inicio de sesión mediante credenciales validas
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales validos y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashboarduser
