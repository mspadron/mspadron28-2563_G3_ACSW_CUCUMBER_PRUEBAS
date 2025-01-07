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

@given('Abrir Navegador para inicio sesión')
def abrir_navegador(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost:5174/')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('Ingreso de credenciales y direccionamiento al sistema')
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
    time.sleep(1)
    context.driver.get('http://localhost:5174/dashboard')
    # Esperar redirección al dashboard
    WebDriverWait(context.driver, 10).until(
        EC.url_to_be("http://localhost:5174/dashboard")
    )
    time.sleep(3)
    print("Redirigido correctamente al dashboard.")


@then('Verificando ingreso correcto del sistema y selección dashboarduser')
def verificacion_y_seleccion_usuario(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Usuarios' en el navbar
        usuarios_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Usuarios'))
        )
        usuarios_link.click()

        # Esperar redirección a la URL de 'Usuarios'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5174/dashUser")
        )
        assert context.driver.current_url == "http://localhost:5174/dashUser", \
            "La URL no coincide con la página de 'Usuarios'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboarduser')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de Usuarios")
        print("Redirigido correctamente a la página de 'Usuarios'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Usuarios':", str(e))
        raise


@when('Se selecciona el botón para crear un nuevo usuario')
def seleccionar_boton_nuevo_usuario(context):
    ensure_pdf_initialized(context)
    # Hacer clic en el botón para crear un nuevo usuario
    nuevo_usuario_button = context.driver.find_element(By.NAME, 'nuevo_usuario')
    nuevo_usuario_button.click()
    screenshot_path = take_screenshot(context, 'clic_boton_nuevo_usuario')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Nuevo Usuario'")


@when('Se completa el formulario de creación con datos válidos')
def completar_formulario_creacion(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'id_rol'))
    )
    rol_select = context.driver.find_element(By.ID, 'rol-label')
    rol_select.click()
    time.sleep(1)
    rol_opcion = context.driver.find_element(By.XPATH, "//li[text()='Administrador']")
    rol_opcion.click()
    time.sleep(1)
    nombre_usuario_field = context.driver.find_element(By.NAME, 'nombre_usuario')
    nombre_usuario_field.send_keys('Test_Selenium')
    time.sleep(1)
    clave_usuario_field = context.driver.find_element(By.NAME, 'clave_usuario')
    clave_usuario_field.send_keys('Mspadron28')
    time.sleep(1)
    screenshot_path = take_screenshot(context, 'formulario_completado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario completado con datos válidos")


@when('Se guarda el nuevo usuario')
def guardar_nuevo_usuario(context):
    ensure_pdf_initialized(context)
    guardar_button = context.driver.find_element(By.NAME, 'crear_usuario')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'crear_usuario'))
    )
    screenshot_path = take_screenshot(context, 'usuario_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Nuevo usuario guardado")


@then('Se verifica que el usuario "Test_Selenium" fue creado correctamente')
def verificar_usuario_creado(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    usuario_nombre = context.driver.find_element(By.XPATH, "//th[text()='Test_Selenium']")
    assert usuario_nombre is not None, "El usuario 'Test_Selenium' no fue encontrado en la tabla de usuarios"
    screenshot_path = take_screenshot(context, 'verificacion_usuario_creado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de creación de usuario")

# -----------------------------------Segundo escenario-------------------------------------------------

@when('Se selecciona el botón para editar un usuario')
def seleccionar_boton_editar_usuario(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el usuario "Test_Selenium"
    usuario_fila = context.driver.find_element(By.XPATH, "//th[text()='Nuria']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Editar"
    editar_usuario_button = usuario_fila.find_element(By.XPATH, ".//button[@name='editar_usuario']")
    editar_usuario_button.click()


    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_editar_usuario')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Editar Usuario'")



@when('Se edita el nombre de usuario de Nuria a Test_Edit_Selenium')
def editar_nombre_usuario(context):
    ensure_pdf_initialized(context)
    # Localizar el campo del nombre de usuario y cambiar el valor
    nombre_usuario_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'nombre_usuario'))
    )
    time.sleep(1)
    nombre_usuario_field.send_keys(Keys.CONTROL + 'a')
    time.sleep(1)
    nombre_usuario_field.send_keys(Keys.DELETE)
    time.sleep(1)
    nombre_usuario_field.send_keys('Test_Edit_Selenium')
    time.sleep(2)
    screenshot_path = take_screenshot(context, 'formulario_edicion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario editado con el nuevo nombre de usuario")


@when('Se guarda el usuario editado')
def guardar_usuario_editado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    guardar_button = context.driver.find_element(By.NAME, 'crear_usuario')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'crear_usuario'))
    )
    screenshot_path = take_screenshot(context, 'usuario_editado_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Usuario editado guardado")


@then('Se verifica que el usuario fue editado correctamente')
def verificar_usuario_editado(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    usuario_editado = context.driver.find_element(By.XPATH, "//th[text()='Test_Edit_Selenium']")
    assert usuario_editado is not None, "El usuario 'Test_Edit_Selenium' no fue encontrado en la tabla de usuarios"
    screenshot_path = take_screenshot(context, 'verificacion_usuario_editado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de edición de usuario")

# -----------------------------------Tercer escenario-------------------------------------------------
@when('Se selecciona el botón para eliminar un usuario')
def seleccionar_boton_eliminar_usuario(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el usuario "Test_Selenium"
    usuario_fila = context.driver.find_element(By.XPATH, "//th[text()='Test_Selenium']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Eliminar"
    eliminar_usuario_button = usuario_fila.find_element(By.XPATH, ".//button[@name='eliminar_usuario']")
    eliminar_usuario_button.click()

    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_eliminar_usuario')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Eliminar Usuario'")

@when('Se confirma la eliminación del usuario')
def confirmar_eliminacion_usuario(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Interactuar con el cuadro de Alertify y confirmar la eliminación
    alertify_ok_button = context.driver.find_element(By.CSS_SELECTOR, "button.ajs-button.ajs-ok")
    alertify_ok_button.click()

    # Capturar pantalla después de confirmar
    screenshot_path = take_screenshot(context, 'confirmar_eliminacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Confirmar eliminación del usuario")

@then('Se verifica que el usuario fue eliminado correctamente')
def verificar_usuario_eliminado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Verificar que el usuario "Test_Selenium" ya no esté en la tabla
    usuarios_tabla = context.driver.find_elements(By.XPATH, "//th[text()='Test_Selenium']")
    assert len(usuarios_tabla) == 0, "El usuario 'Test_Selenium' aún aparece en la tabla"

    # Capturar pantalla de la tabla después de verificar
    screenshot_path = take_screenshot(context, 'verificacion_usuario_eliminado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de eliminación de usuario")


