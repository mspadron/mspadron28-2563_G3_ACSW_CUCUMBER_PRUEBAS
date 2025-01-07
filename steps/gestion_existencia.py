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

@then('Verificando ingreso correcto del sistema y selección dashboardExistencia')
def verificacion_y_seleccion_existencia(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Existencias en el navbar
        existencia_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Existencias'))
        )
        existencia_link.click()


        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5174/dashExistencia")
        )
        assert context.driver.current_url == "http://localhost:5174/dashExistencia", \
            "La URL no coincide con la página de 'Existencias'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboardExistencias')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de existencias")
        print("Redirigido correctamente a la página de 'Existencias'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Existencias':", str(e))
        raise


@when('Se selecciona el botón para crear una nueva existencia')
def seleccionar_boton_nueva_existencia(context):
    ensure_pdf_initialized(context)
    # Hacer clic en el botón para crear una nueva existencia
    nueva_existencia_button = context.driver.find_element(By.NAME, 'nueva_existencia')
    nueva_existencia_button.click()
    screenshot_path = take_screenshot(context, 'clic_boton_nueva_existencia')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Nueva Existencia'")


@when('Se completa el formulario para nueva existencia')
def completar_formulario_existencia(context):
    ensure_pdf_initialized(context)

    # Esperar a que el formulario de existencia esté presente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'category-label'))
    )

    # Seleccionar categoría
    categoria_label = context.driver.find_element(By.ID, 'category-label')
    categoria_label.click()
    time.sleep(1)
    categoria_opcion = context.driver.find_element(By.XPATH, "//li[text()='Material Universitario']")
    categoria_opcion.click()
    time.sleep(1)

    # Seleccionar producto
    producto_label = context.driver.find_element(By.ID, 'producto-label')
    producto_label.click()
    time.sleep(1)
    producto_opcion = context.driver.find_element(By.XPATH, "//li[text()='papel ministro']")
    producto_opcion.click()
    time.sleep(1)

    # Seleccionar proveedor
    proveedor_label = context.driver.find_element(By.ID, 'proveedor-label')
    proveedor_label.click()
    time.sleep(1)
    proveedor_opcion = context.driver.find_element(By.XPATH, "//li[text()='Novicom']")
    proveedor_opcion.click()
    time.sleep(1)

    # Ingresar stock inicial
    stock_inicial_field = context.driver.find_element(By.NAME, 'stockinicial_existencia')
    stock_inicial_field.send_keys('50')
    time.sleep(1)

    # Ingresar precio de compra
    precio_compra_field = context.driver.find_element(By.NAME, 'preciocompra_existencia')
    precio_compra_field.send_keys('0.28')
    time.sleep(1)

    # Ingresar precio de venta
    precio_venta_field = context.driver.find_element(By.NAME, 'precioventa_existencia')
    precio_venta_field.send_keys('0.50')
    time.sleep(1)

    # Capturar pantalla del formulario completado
    screenshot_path = take_screenshot(context, 'formulario_existencia_completado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario de creación de existencia completado")


@when('Se guarda nueva existencia')
def guardar_nueva_existencia(context):
    ensure_pdf_initialized(context)

    # Hacer clic en el botón "Guardar"
    guardar_button = context.driver.find_element(By.NAME, 'guardar_existencia')
    guardar_button.click()

    # Esperar a que el botón desaparezca (indicando que la acción de guardar se completó)
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_existencia'))
    )

    # Capturar pantalla después de guardar
    screenshot_path = take_screenshot(context, 'existencia_guardada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Nueva existencia guardada")


@then('Se verifica que nueva existencia fue creada correctamente')
def verificar_existencia_creada(context):
    ensure_pdf_initialized(context)

    # Esperar a que la tabla o lista de existencias esté presente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    time.sleep(1)

    # Verificar que la existencia creada está en la tabla
    existencia_fila = context.driver.find_element(By.XPATH, "//th[text()='Material Universitario']/ancestor::tr")
    assert existencia_fila is not None, "La existencia 'Material Universitario' no fue encontrada en la tabla de existencias"

    # Capturar pantalla para documentación
    screenshot_path = take_screenshot(context, 'verificacion_existencia_creada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de creación de nueva existencia")

# -----------------------------------SEGUNDO escenario-------------------------------------------------
@when('Se selecciona el botón para agregar entrada')
def seleccionar_boton_agregar_entrada(context):
    ensure_pdf_initialized(context)
    # Localizar y hacer clic en el botón para agregar entrada
    entrada_button = context.driver.find_element(By.NAME, 'entrada')
    entrada_button.click()

    screenshot_path = take_screenshot(context, 'clic_boton_agregar_entrada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Agregar Entrada'")


@when('Se agrega la cantidad')
def agregar_cantidad_entrada(context):
    ensure_pdf_initialized(context)

    # Esperar a que el campo de cantidad esté presente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'cantidad'))
    )

    # Ingresar la cantidad en el campo correspondiente
    cantidad_field = context.driver.find_element(By.NAME, 'cantidad')
    cantidad_field.send_keys('10')
    time.sleep(1)

    screenshot_path = take_screenshot(context, 'cantidad_agregada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Cantidad agregada a la entrada")


@when('Se registra la entrada')
def registrar_entrada(context):
    ensure_pdf_initialized(context)

    # Localizar y hacer clic en el botón para registrar la entrada
    registrar_button = context.driver.find_element(By.NAME, 'registrar')
    registrar_button.click()

    # Esperar a que el proceso de registro se complete
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'registrar'))
    )

    screenshot_path = take_screenshot(context, 'entrada_registrada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Entrada registrada exitosamente")


# -----------------------------------Tercer escenario-------------------------------------------------
@when('Se selecciona el botón para agregar salida')
def seleccionar_boton_agregar_salida(context):
    ensure_pdf_initialized(context)
    # Localizar y hacer clic en el botón para agregar salida
    salida_button = context.driver.find_element(By.NAME, 'salida')
    salida_button.click()

    screenshot_path = take_screenshot(context, 'clic_boton_agregar_salida')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Agregar Salida'")


@when('Se agrega la cantidad salida')
def agregar_cantidad_salida(context):
    ensure_pdf_initialized(context)

    # Esperar a que el campo de cantidad esté presente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'cantidad'))
    )

    # Ingresar la cantidad en el campo correspondiente
    cantidad_field = context.driver.find_element(By.NAME, 'cantidad')
    cantidad_field.send_keys('5')  # Cantidad a salir (ajustar según el caso)
    time.sleep(1)

    screenshot_path = take_screenshot(context, 'cantidad_salida_agregada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Cantidad de salida agregada")


@when('Se registra la salida')
def registrar_salida(context):
    ensure_pdf_initialized(context)

    # Localizar y hacer clic en el botón para registrar la salida
    registrar_button = context.driver.find_element(By.NAME, 'registrar')
    registrar_button.click()

    # Esperar a que el proceso de registro se complete
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'registrar'))
    )

    screenshot_path = take_screenshot(context, 'salida_registrada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Salida registrada exitosamente")
