# Created by MATIAS at 8/1/2025
Feature: Gestionar Reportes

  Scenario: Crear reporte de entradas de existencias
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashEntrada
    When Se selecciona el botón para descargar el pdf de entradas
    Then Se verifica que se haya descargado el pdf de entradas

  Scenario: Crear reporte de salidas de existencias
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashSalida
    When Se selecciona el botón para descargar el pdf de salidas
    Then Se verifica que se haya descargado el pdf de salidas

  Scenario: Crear reporte de existencias minimas
    Given Abrir Navegador para inicio sesión
    When Ingreso de credenciales y direccionamiento al sistema
    Then Verificando ingreso correcto del sistema y selección dashMixEx
    When Se selecciona el botón para descargar el pdf de existencias minimas
    Then Se verifica que se haya descargado el pdf de existencias minimas
