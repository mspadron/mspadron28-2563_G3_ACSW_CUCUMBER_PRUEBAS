from behave import *
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

from PIL import Image
from fpdf import FPDF
import os
import time

# Ruta para guardar capturas de pantalla
SCREENSHOTS_DIR = 'screenshots'


def ensure_pdf_initialized(context):
    if not hasattr(context, 'pdf'):
        context.pdf = FPDF()
        context.pdf.set_auto_page_break(auto=True, margin=15)


def setup_browser(context):
    # Uso de GeckoDriverManager para automatizar el manejo del driver de Firefox
    service = EdgeService(EdgeChromiumDriverManager().install())
    # Inicializar el navegador
    context.driver = webdriver.Edge(service=service)
    context.driver.maximize_window()
    # Crea el directorio de capturas si no existe
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def take_screenshot(context, name):
    """Captura una pantalla y la guarda con el nombre proporcionado."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f'{name}_{timestamp}.png')
    context.driver.save_screenshot(screenshot_path)
    return screenshot_path


def add_screenshot_to_pdf(pdf, image_path, step_description):
    """Agrega una captura de pantalla al PDF."""
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, step_description, 0, 1, 'C')
    pdf.ln(10)  # Agrega un salto de línea
    pdf.image(image_path, x=10, y=pdf.get_y(), w=190)

    # -----------------------------------Primer escenario-------------------------------------------------

@then('Verificando ingreso correcto del sistema y selección dashProveedor')
def verificacion_y_seleccion_proveedor(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Proveedores' en el navbar
        proveedores_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Proveedores'))
        )
        proveedores_link.click()

        # Esperar redirección a la URL de 'Proveedores'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5173/dashProveedor")
        )
        assert context.driver.current_url == "http://localhost:5173/dashProveedor", \
            "La URL no coincide con la página de 'Proveedores'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboardProveedor')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de proveedores")
        print("Redirigido correctamente a la página de 'Proveedores'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Proveedores':", str(e))
        raise

@when('Se selecciona el botón para crear un nuevo proveedor')
def seleccionar_boton_nuevo_proveedor(context):
    ensure_pdf_initialized(context)
    # Hacer clic en el botón para crear un nuevo proveedor
    nuevo_proveedor_button = context.driver.find_element(By.NAME, 'nuevo_proveedor')
    nuevo_proveedor_button.click()
    screenshot_path = take_screenshot(context, 'clic_boton_nuevo_proveedor')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Nuevo Proveedor'")


@when('Se completa el formulario para el nuevo proveedor')
def completar_formulario_nuevo_proveedor(context):
    ensure_pdf_initialized(context)
    # Llenar el campo "Nombre Proveedor"
    nombre_proveedor_field = context.driver.find_element(By.NAME, 'nombre_proveedor')
    nombre_proveedor_field.send_keys('Proveedor Test Selenium')
    time.sleep(1)

    # Llenar el campo "Correo Proveedor"
    correo_proveedor_field = context.driver.find_element(By.NAME, 'correo_proveedor')
    correo_proveedor_field.send_keys('proveedor@testselenium.com')
    time.sleep(1)

    # Llenar el campo "Teléfono"
    telefono_field = context.driver.find_element(By.NAME, 'telefono')
    telefono_field.send_keys('1234567890')
    time.sleep(1)

    screenshot_path = take_screenshot(context, 'formulario_proveedor_completado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario completado con datos válidos para el proveedor")


@when('Se guarda el nuevo proveedor')
def guardar_nuevo_proveedor(context):
    ensure_pdf_initialized(context)
    guardar_button = context.driver.find_element(By.NAME, 'guardar_proveedor')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_proveedor'))
    )
    screenshot_path = take_screenshot(context, 'proveedor_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Nuevo proveedor guardado")


@then('Se verifica que el proveedor fue creado correctamente')
def verificar_proveedor_creado(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    time.sleep(1)
    # Verificar que el proveedor "Proveedor Test Selenium" está presente en la tabla
    proveedor_nombre = context.driver.find_element(By.XPATH, "//th[text()='Proveedor Test Selenium']")
    assert proveedor_nombre is not None, "El proveedor 'Proveedor Test Selenium' no fue encontrado en la tabla de proveedores"

    screenshot_path = take_screenshot(context, 'verificacion_proveedor_creado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de creación de proveedor")


# -----------------------------------Segundo escenario-------------------------------------------------
@when('Se selecciona el botón para editar un proveedor')
def seleccionar_boton_editar_proveedor(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el proveedor "Proveedor Test Selenium"
    proveedor_fila = context.driver.find_element(By.XPATH, "//th[text()='Proveedor Test Selenium']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Editar"
    editar_proveedor_button = proveedor_fila.find_element(By.XPATH, ".//button[@name='editar_proveedor']")
    editar_proveedor_button.click()

    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_editar_proveedor')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Editar Proveedor'")


@when('Se edita el nombre del proveedor')
def editar_nombre_proveedor(context):
    ensure_pdf_initialized(context)
    # Localizar el campo del nombre del proveedor y cambiar el valor
    nombre_proveedor_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'nombre_proveedor'))
    )
    time.sleep(1)
    nombre_proveedor_field.send_keys(Keys.CONTROL + 'a')  # Seleccionar todo el texto existente
    time.sleep(1)
    nombre_proveedor_field.send_keys(Keys.DELETE)  # Eliminar el texto existente
    time.sleep(1)
    nombre_proveedor_field.send_keys('Proveedor Updated Selenium')  # Ingresar el nuevo nombre
    time.sleep(2)
    screenshot_path = take_screenshot(context, 'formulario_edicion_proveedor')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario editado con el nuevo nombre de proveedor")


@when('Se guarda el proveedor editado')
def guardar_proveedor_editado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    guardar_button = context.driver.find_element(By.NAME, 'guardar_proveedor')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_proveedor'))
    )
    screenshot_path = take_screenshot(context, 'proveedor_editado_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proveedor editado guardado")


@then('Se verifica que el proveedor fue editado correctamente')
def verificar_proveedor_editado(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    # Verificar que el proveedor "Proveedor Updated Selenium" está presente en la tabla
    proveedor_editado = context.driver.find_element(By.XPATH, "//th[text()='Proveedor Updated Selenium']")
    assert proveedor_editado is not None, "El proveedor 'Proveedor Updated Selenium' no fue encontrado en la tabla de proveedores"
    screenshot_path = take_screenshot(context, 'verificacion_proveedor_editado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de edición de proveedor")





# -----------------------------------Tercer escenario-------------------------------------------------

@when('Se selecciona el botón para eliminar un proveedor')
def seleccionar_boton_eliminar_proveedor(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el proveedor a eliminar
    proveedor_fila = context.driver.find_element(By.XPATH, "//th[text()='Proveedor Updated Selenium']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Eliminar"
    eliminar_proveedor_button = proveedor_fila.find_element(By.XPATH, ".//button[@name='eliminar_proveedor']")
    eliminar_proveedor_button.click()

    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_eliminar_proveedor')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Eliminar Proveedor'")


@when('Se confirma la eliminación del proveedor')
def confirmar_eliminacion_proveedor(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Interactuar con el cuadro de Alertify y confirmar la eliminación
    alertify_ok_button = context.driver.find_element(By.CSS_SELECTOR, "button.ajs-button.ajs-ok")
    alertify_ok_button.click()

    # Capturar pantalla después de confirmar
    screenshot_path = take_screenshot(context, 'confirmar_eliminacion_proveedor')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Confirmar eliminación del proveedor")


@then('Se verifica que el proveedor fue eliminado correctamente')
def verificar_proveedor_eliminado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Verificar que el proveedor eliminado ya no está en la tabla
    proveedor_tabla = context.driver.find_elements(By.XPATH, "//th[text()='Proveedor Updated Selenium']")
    assert len(proveedor_tabla) == 0, "El proveedor 'Proveedor Updated Selenium' aún aparece en la tabla"

    # Capturar pantalla de la tabla después de verificar
    screenshot_path = take_screenshot(context, 'verificacion_proveedor_eliminado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de eliminación de proveedor")


