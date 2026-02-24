import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class VentanaNotas(Gtk.Window):
    """
        clase de la ventaan notas que permite ver las notas que contiene cada uno de los libros
    """
    def __init__(self, padre, titulo_libro, texto_notas):
        """
            funcion para construir la estructura de la pagina
        """
        # nombre pestaña
        super().__init__(title=f"Notas de: {titulo_libro}")
        self.set_transient_for(padre)
        self.set_default_size(350, 250)
        self.set_border_width(10)

        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(caja)

        # titulo
        etiqueta = Gtk.Label(label=f"<b>Notas guardadas para '{titulo_libro}':</b>")
        etiqueta.set_use_markup(True)
        caja.pack_start(etiqueta, False, False, 0)

        # la caja donde se guardan las notas
        vista_notas = Gtk.TextView()
        vista_notas.set_editable(False)
        vista_notas.set_wrap_mode(Gtk.WrapMode.WORD)

        # si no hay notas que ponga un mensaje
        if not texto_notas or texto_notas.strip() == "":
            vista_notas.get_buffer().set_text("No hay notas guardadas para este libro.")
        else:
            vista_notas.get_buffer().set_text(texto_notas)

        # si son muy largas añade una barra para hacer scroll
        scroll = Gtk.ScrolledWindow()
        scroll.add(vista_notas)
        caja.pack_start(scroll, True, True, 0)