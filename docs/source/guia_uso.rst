Guía de Uso
===========

Bienvenido a la Biblioteca Personal. Esta aplicación te permite gestionar tus libros de forma sencilla mediante una interfaz gráfica intuitiva.

Sistemas Operativos Compatibles
-------------------------------
Este proyecto está optimizado y probado principalmente para entornos **Linux** (como Ubuntu, Debian, etc.), ya que se integra de forma nativa con el entorno de escritorio.

También es compatible con **Windows y macOS**, siempre y cuando el usuario configure previamente el entorno de librerías gráficas de GTK3 (mediante MSYS2 en Windows o Homebrew en macOS).

Requisitos y Dependencias
-------------------------
Para que la aplicación funcione correctamente, tu sistema debe cumplir con los siguientes requisitos:

* **Python 3.x**
* El gestor de paquetes **pip**.
* **Librerías gráficas GTK3 (PyGObject):** Si estás en un sistema basado en Debian/Ubuntu, puedes asegurarte de tener las dependencias del sistema ejecutando:

  ``sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0``

Cómo instalar y arrancar la aplicación
--------------------------------------
1. Abre tu terminal.
2. Instala la aplicación mediante pip:

   ``pip install biblioteca-personal``

3. Una vez finalizada la instalación, lanza la interfaz gráfica escribiendo este único comando en la terminal:

   ``abrir-biblioteca``

Funcionalidades principales
---------------------------
* **Añadir un libro:** Rellena los campos del formulario en la interfaz y pulsa el botón correspondiente para guardarlo.
* **Ver libros:** En la pantalla principal verás una tabla con todos los registros guardados de forma persistente en la base de datos local.