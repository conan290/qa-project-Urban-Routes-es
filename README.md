# Pruebas Automatizadas para Urban Routes

## Descripción del Proyecto

Este proyecto contiene una suite de pruebas automatizadas para la página web de Urban Routes, una aplicación de rutas urbanas que permite solicitar taxis. Las pruebas verifican diversas funcionalidades como la selección de rutas, tarifas de taxi, la adición de una tarjeta de crédito, y el envío de mensajes al conductor. Además, incluyen interacciones avanzadas como el manejo de contadores para seleccionar helados y activar opciones especiales como pedir manta y pañuelos.

## Tecnologías y Técnicas Utilizadas

- **Lenguaje**: Python
- **Automatización de pruebas**: Selenium WebDriver
- **Patrón de diseño**: Page Object Model (POM)
- **Manejo de esperas**: WebDriverWait para sincronizar las interacciones con elementos de la página.
- **Interacción avanzada con el DOM**: Uso de JavaScript para hacer scroll hacia elementos no visibles y ejecutar comandos en segundo plano.
- **Aserciones**: Validación de resultados utilizando `assert` en Python.

## Requisitos Previos

Antes de ejecutar las pruebas, asegúrate de tener instaladas las siguientes herramientas:

1. **Python 3.x**
2. **Google Chrome** (Última versión)
3. **ChromeDriver** compatible con la versión de Chrome instalada.

Instala las dependencias necesarias utilizando el siguiente comando:

pip install selenium

## Estructura del Proyecto

- **main.py**: Contiene las clases `UrbanRoutesPage` y `TestUrbanRoutes` que implementan las pruebas.
- **data.py**: Contiene los datos utilizados en las pruebas como URLs, direcciones, números de teléfono y más.
- **README.md**: Documentación del proyecto (este archivo).

## Instrucciones para Ejecutar las Pruebas

### Paso 1: Configuración de ChromeDriver

1. Descarga [ChromeDriver](https://sites.google.com/chromium.org/driver) y colócalo en una carpeta accesible.
2. Asegúrate de agregar el directorio de ChromeDriver a tu variable de entorno `PATH`, o bien asegúrate de que esté en la misma carpeta del proyecto.

### Paso 2: Ejecución de las Pruebas

1. Clona el repositorio o descarga los archivos del proyecto.
2. Desde una terminal, navega hasta la carpeta que contiene el proyecto.
3. Ejecuta el siguiente comando para ejecutar las pruebas:

    ```bash
    pytest main.py
    ```

    Esto ejecutará la suite completa de pruebas automatizadas. Asegúrate de que Google Chrome esté cerrado antes de iniciar las pruebas, ya que el WebDriver abrirá una nueva instancia del navegador para cada prueba.

### Paso 3: Verificación de los Resultados

Al final de la ejecución de las pruebas, recibirás un reporte en la terminal que indicará si las pruebas han pasado o si alguna ha fallado. Puedes analizar los errores detallados para solucionar posibles problemas en las pruebas o en la página.
