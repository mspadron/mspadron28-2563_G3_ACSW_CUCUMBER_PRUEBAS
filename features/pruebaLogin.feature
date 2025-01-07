# Created by Matias Padrón at 1/1/2024
Feature: Prueba para inicio de sesión básico

  Scenario: Inicio de sesión dashboard
    Given Abrir navegador
    When Ingreso de credenciales y direccionamiento al dashboard correcto
    Then Verificando dashboard