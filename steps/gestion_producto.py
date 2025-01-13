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

@then('Verificando ingreso correcto del sistema y selección dashboardProducto')
def verificacion_y_seleccion_producto(context):
    ensure_pdf_initialized(context)

    try:
        # Verificar que el texto "Dashboard" esté presente
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
        )
        print("El texto 'Dashboard' se encontró correctamente en la página.")

        # Seleccionar la opción 'Productos' en el navbar
        productos_link = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Productos'))
        )
        productos_link.click()

        # Esperar redirección a la URL de 'Productos'
        WebDriverWait(context.driver, 10).until(
            EC.url_to_be("http://localhost:5173/dashProducto")
        )
        assert context.driver.current_url == "http://localhost:5173/dashProducto", \
            "La URL no coincide con la página de 'Productos'."

        # Tomar captura de pantalla
        screenshot_path = take_screenshot(context, 'verificacion_dashboardProductos')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del dashboard y selección de productos")
        print("Redirigido correctamente a la página de 'Productos'.")

    except Exception as e:
        print("Error durante la verificación y selección de 'Productos':", str(e))
        raise


@when('Se selecciona el botón para crear un nuevo producto')
def seleccionar_boton_nuevo_producto(context):
    ensure_pdf_initialized(context)
    # Hacer clic en el botón para crear un nuevo producto
    nuevo_producto_button = context.driver.find_element(By.NAME, 'nuevo_producto')
    nuevo_producto_button.click()
    screenshot_path = take_screenshot(context, 'clic_boton_nuevo_producto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Nuevo Producto'")


@when('Se completa el formulario para el nuevo producto')
def completar_formulario_creacion(context):
    # Esperar a que el formulario de producto esté presente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'id_categoria'))
    )
    cat_select = context.driver.find_element(By.ID, 'categoria-label')
    cat_select.click()
    time.sleep(1)
    categoria_opcion = context.driver.find_element(By.XPATH, "//li[text()='TestCategory']")
    categoria_opcion.click()
    time.sleep(1)

    # Rellenar el nombre del producto
    nombre_producto_field = context.driver.find_element(By.NAME, 'nombre_producto')
    nombre_producto_field.send_keys('Producto Test Selenium')
    time.sleep(1)

    # Rellenar el precio del producto
    precio_producto_field = context.driver.find_element(By.NAME, 'precio_producto')
    precio_producto_field.send_keys('99.99')
    time.sleep(1)

    # Rellenar la fecha de expiración del producto
    fecha_expiracion_field = context.driver.find_element(By.NAME, 'fecha_expiracion_producto')
    fecha_expiracion_field.send_keys('20253105')

    time.sleep(1)

    # Tomar captura del formulario completado
    screenshot_path = take_screenshot(context, 'formulario_producto_completado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario de creación de producto completado con datos válidos")


@when('Se guarda el nuevo producto')
def guardar_nuevo_producto(context):
    ensure_pdf_initialized(context)

    # Hacer clic en el botón "Guardar"
    guardar_button = context.driver.find_element(By.NAME, 'guardar_producto')
    guardar_button.click()

    # Esperar a que el botón desaparezca (indicando que la acción de guardar se completó)
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_producto'))
    )

    # Tomar una captura de pantalla del estado después de guardar
    screenshot_path = take_screenshot(context, 'producto_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Nuevo producto guardado")



@then('Se verifica que el producto fue creado correctamente')
def verificar_producto_creado(context):
    ensure_pdf_initialized(context)

    # Esperar a que la tabla o lista de productos esté presente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    time.sleep(1)
    # Verificar que el producto "Producto Test Selenium" se encuentra en la tabla
    producto_nombre = context.driver.find_element(By.XPATH, "//th[text()='Producto Test Selenium']")
    assert producto_nombre is not None, "El producto 'Producto Test Selenium' no fue encontrado en la tabla de productos"

    # Tomar captura de pantalla para documentación
    screenshot_path = take_screenshot(context, 'verificacion_producto_creado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de creación de producto")


# -----------------------------------Segundo escenario-------------------------------------------------
@when('Se selecciona el botón para editar un producto')
def seleccionar_boton_editar_producto(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el producto "Producto Test Selenium"
    producto_fila = context.driver.find_element(By.XPATH, "//th[text()='Producto Test Selenium']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Editar"
    editar_producto_button = producto_fila.find_element(By.XPATH, ".//button[@name='editar_producto']")
    editar_producto_button.click()

    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_editar_producto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Editar Producto'")


@when('Se edita el nombre de producto de Producto Test Selenium a Producto Updated')
def editar_nombre_producto(context):
    ensure_pdf_initialized(context)
    # Localizar el campo del nombre del producto y cambiar el valor
    nombre_producto_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'nombre_producto'))
    )
    time.sleep(1)
    nombre_producto_field.send_keys(Keys.CONTROL + 'a')  # Seleccionar todo el texto
    time.sleep(1)
    nombre_producto_field.send_keys(Keys.DELETE)  # Eliminar el texto actual
    time.sleep(1)
    nombre_producto_field.send_keys('Producto Updated')  # Ingresar el nuevo nombre
    time.sleep(2)
    screenshot_path = take_screenshot(context, 'formulario_edicion_producto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Formulario editado con el nuevo nombre de producto")


@when('Se guarda el producto editado')
def guardar_producto_editado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar y hacer clic en el botón para guardar el producto
    guardar_button = context.driver.find_element(By.NAME, 'guardar_producto')
    guardar_button.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.NAME, 'guardar_producto'))
    )
    screenshot_path = take_screenshot(context, 'producto_editado_guardado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Producto editado guardado")


@then('Se verifica que el producto fue editado correctamente')
def verificar_producto_editado(context):
    ensure_pdf_initialized(context)
    # Esperar la presencia de la tabla de productos
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )
    # Verificar que el producto editado esté presente en la tabla
    producto_editado = context.driver.find_element(By.XPATH, "//td[text()='Producto Updated']")
    assert producto_editado is not None, "El producto 'Producto Updated' no fue encontrado en la tabla de productos"
    screenshot_path = take_screenshot(context, 'verificacion_producto_editado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de edición de producto")

# -----------------------------------Tercer escenario-------------------------------------------------

@when('Se selecciona el botón para eliminar un producto')
def seleccionar_boton_eliminar_producto(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Localizar la fila que contiene el producto "Producto Test Selenium"
    producto_fila = context.driver.find_element(By.XPATH, "//th[text()='Producto Test Selenium']/ancestor::tr")
    time.sleep(2)
    # Dentro de la misma fila, localizar el botón "Eliminar"
    eliminar_producto_button = producto_fila.find_element(By.XPATH, ".//button[@name='eliminar_producto']")
    eliminar_producto_button.click()

    # Capturar pantalla y agregar al PDF
    screenshot_path = take_screenshot(context, 'clic_boton_eliminar_producto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar botón 'Eliminar Producto'")


@when('Se confirma la eliminación del producto')
def confirmar_eliminacion_producto(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Interactuar con el cuadro de confirmación (ejemplo: Alertify.js)
    alertify_ok_button = context.driver.find_element(By.CSS_SELECTOR, "button.ajs-button.ajs-ok")
    alertify_ok_button.click()

    # Capturar pantalla después de confirmar
    screenshot_path = take_screenshot(context, 'confirmar_eliminacion_producto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Confirmar eliminación del producto")


@then('Se verifica que el producto fue eliminado correctamente')
def verificar_producto_eliminado(context):
    ensure_pdf_initialized(context)
    time.sleep(2)
    # Verificar que el producto "Producto Test Selenium" ya no esté en la tabla
    productos_tabla = context.driver.find_elements(By.XPATH, "//th[text()='Producto Test Selenium']")
    assert len(productos_tabla) == 0, "El producto 'Producto Test Selenium' aún aparece en la tabla"

    # Capturar pantalla de la tabla después de verificar
    screenshot_path = take_screenshot(context, 'verificacion_producto_eliminado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de eliminación de producto")
