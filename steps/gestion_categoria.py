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
@then('Verificando ingreso correcto del sistema y selección dashCategoria')
def verificacion_y_seleccion_categoria(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Usuarios' en el navbar
        categorias_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Categorías'))
        )
        categorias_link.click()

        # Esperar redirección a la URL de 'Usuarios'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5173/dashCategoria")
        )
        assert context.driver.current_url == "http://localhost:5173/dashCategoria", \
            "La URL no coincide con la página de 'Usuarios'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboardCategoria')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de categorias")
        print("Redirigido correctamente a la página de 'Categorias'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Categorias':", str(e))
        raise


@when('Se selecciona el botón para crear una nueva categoria')
def seleccionar_boton_nueva_categoria(context):
    ensure_pdf_initialized(context)
    # Hacer clic en el botón para crear un nuevo usuario
    nueva_categoria_button = context.driver.find_element(By.NAME, 'nueva_categoria')
    nueva_categoria_button.click()
    screenshot_path = take_screenshot(context, 'clic_boton_nueva_categoria')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Nueva Categoria'")


@when('Se completa el formulario para la nueva categoria')
def completar_formulario_creacion(context):
    ensure_pdf_initialized(context)
    nombre_categoria_field = context.driver.find_element(By.NAME, 'nombre_categoria')
    nombre_categoria_field.send_keys('TestCategory')
    time.sleep(1)
    screenshot_path = take_screenshot(context, 'formulario_completado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario completado con datos válidos")


@when('Se guarda la nueva categoria')
def guardar_nuevo_usuario(context):
    ensure_pdf_initialized(context)
    guardar_button = context.driver.find_element(By.NAME, 'guardar_categoria')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_categoria'))
    )
    screenshot_path = take_screenshot(context, 'categoria_guardada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Nueva categoria guardada")


@then('Se verifica que la categoria "TestCategory" fue creado correctamente')
def verificar_categoria_creada(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    usuario_nombre = context.driver.find_element(By.XPATH, "//th[text()='TestCategory']")
    assert usuario_nombre is not None, "La categoria 'TestCategory' no fue encontrado en la tabla de categorias"
    screenshot_path = take_screenshot(context, 'verificacion_categoria_creada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de creación de categoria")


# -----------------------------------Segundo escenario-------------------------------------------------

@when('Se selecciona el botón para editar una categoria')
def seleccionar_boton_editar_categoria(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el usuario "Test_Selenium"
    usuario_fila = context.driver.find_element(By.XPATH, "//th[text()='TestCategory']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Editar"
    editar_categoria_button = usuario_fila.find_element(By.XPATH, ".//button[@name='editar_categoria']")
    editar_categoria_button.click()


    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_editar_categoria')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Editar Categoria'")


@when('Se edita el nombre de la categoria de TestCategory a TestCategoryUpdated')
def editar_nombre_categoria(context):
    ensure_pdf_initialized(context)
    # Localizar el campo del nombre de usuario y cambiar el valor
    nombre_categoria_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'nombre_categoria'))
    )
    time.sleep(1)
    nombre_categoria_field.send_keys(Keys.CONTROL + 'a')
    time.sleep(1)
    nombre_categoria_field.send_keys(Keys.DELETE)
    time.sleep(1)
    nombre_categoria_field.send_keys('TestCategoryUpdated')
    time.sleep(2)
    screenshot_path = take_screenshot(context, 'formulario_edicion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario editado con el nuevo nombre de categoria")


@when('Se guarda la categoria editada')
def guardar_categoria_editado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    guardar_button = context.driver.find_element(By.NAME, 'guardar_categoria')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_categoria'))
    )
    screenshot_path = take_screenshot(context, 'categoria_editada_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Categoria editada guardada")


@then('Se verifica que la categoria fue editada correctamente')
def verificar_categoria_editado(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    categoria_editado = context.driver.find_element(By.XPATH, "//th[text()='TestCategoryUpdated']")
    assert categoria_editado is not None, "La categoria 'TestCategoryUpdated' no fue encontrado en la tabla de categorias"
    screenshot_path = take_screenshot(context, 'verificacion_categoria_editado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de edición de categoria")

# -----------------------------------Tercer escenario-------------------------------------------------


@when('Se selecciona el botón para eliminar una categoria')
def seleccionar_boton_eliminar_categoria(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene la categoria a eliminar
    categoria_fila = context.driver.find_element(By.XPATH, "//th[text()='TestCategoryUpdated']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Eliminar"
    eliminar_categoria_button = categoria_fila.find_element(By.XPATH, ".//button[@name='eliminar_categoria']")
    eliminar_categoria_button.click()

    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_eliminar_categoria')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Eliminar Categoria'")

@when('Se confirma la eliminación de la categoria')
def confirmar_eliminacion_categoria(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Interactuar con el cuadro de Alertify y confirmar la eliminación
    alertify_ok_button = context.driver.find_element(By.CSS_SELECTOR, "button.ajs-button.ajs-ok")
    alertify_ok_button.click()

    # Capturar pantalla después de confirmar
    screenshot_path = take_screenshot(context, 'confirmar_eliminacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Confirmar eliminación de la categoria")

@then('Se verifica que la categoria fue eliminada correctamente')
def verificar_categoria_eliminado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Verificar que la categoria eliminada ya no esta en la tabla
    usuarios_tabla = context.driver.find_elements(By.XPATH, "//th[text()='TestCategoryUpdated']")
    assert len(usuarios_tabla) == 0, "La categoria 'TestCategoryUpdated' aún aparece en la tabla"

    # Capturar pantalla de la tabla después de verificar
    screenshot_path = take_screenshot(context, 'verificacion_categoria_eliminado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de eliminación de categoria")
