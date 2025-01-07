from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service

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


# ------------------------------------------------------------------------------------

@given('Abrir navegador')
def abrir_navegador(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost:5173/')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('Ingreso de credenciales y direccionamiento al dashboard correcto')
def ingreso_valido_dashboard(context):
    ensure_pdf_initialized(context)

    # Ingresar credenciales
    username_field = context.driver.find_element(By.NAME, 'nombre_usuario')
    password_field = context.driver.find_element(By.NAME, 'clave_usuario')
    username_field.send_keys('Matias')
    password_field.send_keys('mspadron')
    # Tomar captura antes de enviar
    screenshot_path = take_screenshot(context, 'validUserNameAndPassword')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales válidas")
    context.driver.find_element(By.NAME, 'submit').click()
    time.sleep(3)
    context.driver.get('http://localhost:5173/dashboard')
    # Esperar redirección al dashboard
    WebDriverWait(context.driver, 10).until(
        EC.url_to_be("http://localhost:5173/dashboard")
    )
    time.sleep(3)
    print("Redirigido correctamente al dashboard.")



@then('Verificando dashboard')
def verificacion_dashboard(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente en un <h1>
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")
        # Validar la URL actual
        assert context.driver.current_url == "http://localhost:5173/dashboard", "La URL no coincide con la del dashboard."
        # Tomar captura de pantalla para evidencia
        screenshot_path = take_screenshot(context, 'verificacion_dashboard')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard")
    except Exception as e:
        # Capturar cualquier error y mostrar detalles
        print("Error durante la verificación del dashboard:", str(e))
        raise