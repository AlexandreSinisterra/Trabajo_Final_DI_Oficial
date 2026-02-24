import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ventanas.ventana_principal import VentanaPrincipal


def main():
    """
        clase main para ejecutar el programa
    """
    app = VentanaPrincipal()
    app.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()