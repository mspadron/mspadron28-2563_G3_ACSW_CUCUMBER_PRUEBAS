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

@then('Verificando ingreso correcto del sistema y selección dashEntrada')
def verificacion_y_seleccion_reportes(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Productos' en el navbar
        productos_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Entradas'))
        )
        productos_link.click()

        # Esperar redirección a la URL de 'Productos'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5173/dashEntrada")
        )
        assert context.driver.current_url == "http://localhost:5173/dashEntrada", \
            "La URL no coincide con la página de 'Entradas'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboardEntradas')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de entradas")
        print("Redirigido correctamente a la página de 'Entradas'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Entradas':", str(e))
        raise



@when('Se selecciona el botón para descargar el pdf de entradas')
def seleccionar_boton_descargar_pdf(context):
    ensure_pdf_initialized(context)

    try:
        # Localizar el botón de descarga del PDF y hacer clic en él
        descargar_pdf_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'descargar_pdf_entrada'))
        )
        descargar_pdf_button.click()

        # Tomar captura de pantalla después del clic
        screenshot_path = take_screenshot(context, 'clic_boton_descargar_pdf')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Clic en botón de descarga de PDF de entradas")

    except Exception as e:
        print(f"Error al seleccionar el botón para descargar el PDF: {e}")
        raise

@then('Se verifica que se haya descargado el pdf de entradas')
def verificar_descarga_pdf(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el archivo PDF haya sido descargado
        download_dir = "C:\\Users\\MATIAS\\Downloads"
        expected_file = os.path.join(download_dir, "entradas_reporte.pdf")

        # Esperar a que el archivo aparezca en el directorio de descargas
        timeout = 10
        start_time = time.time()
        while not os.path.exists(expected_file):
            time.sleep(1)
            if time.time() - start_time > timeout:
                raise FileNotFoundError(f"No se encontró el archivo {expected_file} después de {timeout} segundos")

        # Verificar que el archivo tiene contenido
        assert os.path.getsize(expected_file) > 0, "El archivo descargado está vacío."

        # Tomar captura de pantalla de la página para documentar el estado final
        screenshot_path = take_screenshot(context, 'pdf_descargado_exitosamente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "PDF descargado exitosamente")

        print(f"El archivo {expected_file} se descargó correctamente.")

    except Exception as e:
        print(f"Error al verificar la descarga del PDF: {e}")
        raise

# -----------------------------------Segundo escenario-------------------------------------------------
@then('Verificando ingreso correcto del sistema y selección dashSalida')
def verificacion_y_seleccion_dash_salida(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Salidas' en el navbar
        salidas_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Salidas'))
        )
        salidas_link.click()

        # Esperar redirección a la URL de 'Salidas'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5173/dashSalida")
        )
        assert context.driver.current_url == "http://localhost:5173/dashSalida", \
            "La URL no coincide con la página de 'Salidas'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboardSalidas')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de salidas")
        print("Redirigido correctamente a la página de 'Salidas'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Salidas':", str(e))
        raise

@when('Se selecciona el botón para descargar el pdf de salidas')
def seleccionar_boton_descargar_pdf_salida(context):
    try:
        # Localizar el botón por su atributo 'name'
        boton_pdf_salida = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "descargar_pdf_salida"))
        )
        boton_pdf_salida.click()
        print("Se hizo clic en el botón para descargar el PDF de salidas.")

        # Tomar captura de pantalla después de hacer clic en el botón
        screenshot_path = take_screenshot(context, 'click_descargar_pdf_salidas')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Clic en descargar PDF de salidas")

    except Exception as e:
        print("Error al intentar hacer clic en el botón de descargar PDF de salidas:", str(e))
        raise

@then('Se verifica que se haya descargado el pdf de salidas')
def verificar_descarga_pdf_salidas(context):
    import os
    import time

    ensure_pdf_initialized(context)

    try:
        # Define la ruta de descargas
        download_dir = "C:\\Users\\MATIAS\\Downloads"
        expected_file = os.path.join(download_dir, "salidas_reporte.pdf")

        # Esperar a que el archivo aparezca en el directorio de descargas
        timeout = 10
        start_time = time.time()
        while not os.path.exists(expected_file):
            time.sleep(1)
            if time.time() - start_time > timeout:
                raise FileNotFoundError(f"No se encontró el archivo {expected_file} después de {timeout} segundos")

        # Verificar que el archivo tiene contenido
        assert os.path.getsize(expected_file) > 0, "El archivo descargado está vacío."

        # Tomar captura de pantalla de la página para documentar el estado final
        screenshot_path = take_screenshot(context, 'pdf_salidas_descargado_exitosamente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "PDF de salidas descargado exitosamente")

        print(f"El archivo {expected_file} se descargó correctamente.")

    except Exception as e:
        print(f"Error al verificar la descarga del PDF de salidas: {e}")
        raise
# -----------------------------------Tercer escenario-------------------------------------------------
@then('Verificando ingreso correcto del sistema y selección dashMixEx')
def verificacion_y_seleccion_dash_mix_ex(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Existencias Mínimas' en el navbar
        mix_ex_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Existencias Mínimas'))
        )
        mix_ex_link.click()

        # Esperar redirección a la URL de 'Existencias Mínimas'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5173/reporteMinExis")
        )
        assert context.driver.current_url == "http://localhost:5173/reporteMinExis", \
            "La URL no coincide con la página de 'Existencias Mínimas'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboard_mix_ex')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de existencias mínimas")
        print("Redirigido correctamente a la página de 'Existencias Mínimas'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Existencias Mínimas':", str(e))
        raise


@when('Se selecciona el botón para descargar el pdf de existencias minimas')
def seleccionar_boton_descargar_pdf_existencia(context):
    try:
        # Localizar el botón por su atributo 'name'
        boton_pdf_existencia = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "descargar_pdf_existencia"))
        )
        boton_pdf_existencia.click()
        print("Se hizo clic en el botón para descargar el PDF de existencias mínimas.")

        # Tomar captura de pantalla después de hacer clic en el botón
        screenshot_path = take_screenshot(context, 'click_descargar_pdf_existencias_minimas')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Clic en descargar PDF de existencias mínimas")

    except Exception as e:
        print("Error al intentar hacer clic en el botón de descargar PDF de existencias mínimas:", str(e))
        raise


@then('Se verifica que se haya descargado el pdf de existencias minimas')
def verificar_descarga_pdf_existencias_minimas(context):
    import os
    import time

    ensure_pdf_initialized(context)

    try:
        # Define la ruta de descargas
        download_dir = "C:\\Users\\MATIAS\\Downloads"
        expected_file = os.path.join(download_dir, "existencia_minimas_reporte.pdf")

        # Esperar a que el archivo aparezca en el directorio de descargas
        timeout = 10
        start_time = time.time()
        while not os.path.exists(expected_file):
            time.sleep(1)
            if time.time() - start_time > timeout:
                raise FileNotFoundError(f"No se encontró el archivo {expected_file} después de {timeout} segundos")

        # Verificar que el archivo tiene contenido
        assert os.path.getsize(expected_file) > 0, "El archivo descargado está vacío."

        # Tomar captura de pantalla de la página para documentar el estado final
        screenshot_path = take_screenshot(context, 'pdf_existencias_minimas_descargado_exitosamente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "PDF de existencias mínimas descargado exitosamente")

        print(f"El archivo {expected_file} se descargó correctamente.")

    except Exception as e:
        print(f"Error al verificar la descarga del PDF de existencias mínimas: {e}")
        raise
