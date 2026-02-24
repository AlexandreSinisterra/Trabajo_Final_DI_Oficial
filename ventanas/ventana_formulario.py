import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import conexionBD


class VentanaFormulario(Gtk.Window):
    """
        clase de la ventana formulario para editar o agregar libros
    """
    def __init__(self, padre, libro_editar=None):
        """
            funcion para construir la estructura de la pagina
        """
        super().__init__(title="Formulario de Libro")
        self.padre = padre
        self.libro_editar = libro_editar
        self.set_modal(True)
        self.set_transient_for(padre)
        self.set_default_size(400, 400)
        self.set_border_width(10)

        caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(caja_principal)

        # titulo y autor
        self.entrada_titulo = Gtk.Entry(placeholder_text="Título del libro")
        self.entrada_autor = Gtk.Entry(placeholder_text="Autor")

        # ComboBox para género
        self.combo_genero = Gtk.ComboBoxText()
        for x in ["Ficción", "Fantasía", "Ciencia", "Historia", "MMO RPG no lineal", "Pablo"]:
            self.combo_genero.append_text(x)
        self.combo_genero.set_active(0)

        # RadioButtons para formato
        caja_radio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.radio_fisico = Gtk.RadioButton.new_with_label_from_widget(None, "Físico")
        self.radio_digital = Gtk.RadioButton.new_with_label_from_widget(self.radio_fisico, "Digital")
        caja_radio.pack_start(self.radio_fisico, False, False, 0)
        caja_radio.pack_start(self.radio_digital, False, False, 0)

        # CheckButton para estado
        self.check_leido = Gtk.CheckButton(label="Libro ya leído")

        # TextView para notas
        self.buffer_notas = Gtk.TextBuffer()
        self.vista_notas = Gtk.TextView(buffer=self.buffer_notas)
        self.vista_notas.set_wrap_mode(Gtk.WrapMode.WORD)
        scroll_notas = Gtk.ScrolledWindow()
        scroll_notas.add(self.vista_notas)

        # Añadir a la caja principal (añadimos lo que vendrian ser los widgets a la plantilla)
        caja_principal.pack_start(Gtk.Label(label="Título:"), False, False, 0)
        caja_principal.pack_start(self.entrada_titulo, False, False, 0)
        caja_principal.pack_start(Gtk.Label(label="Autor:"), False, False, 0)
        caja_principal.pack_start(self.entrada_autor, False, False, 0)
        caja_principal.pack_start(Gtk.Label(label="Género:"), False, False, 0)
        caja_principal.pack_start(self.combo_genero, False, False, 0)
        caja_principal.pack_start(Gtk.Label(label="Formato:"), False, False, 0)
        caja_principal.pack_start(caja_radio, False, False, 0)
        caja_principal.pack_start(self.check_leido, False, False, 0)
        caja_principal.pack_start(Gtk.Label(label="Notas:"), False, False, 0)
        caja_principal.pack_start(scroll_notas, True, True, 0)

        # Botón de Guardar
        btn_guardar = Gtk.Button(label="Guardar")
        btn_guardar.connect("clicked", self.on_guardar_clicked)
        caja_principal.pack_start(btn_guardar, False, False, 0)

        # Cargar datos si queremos editarlo
        if self.libro_editar:
            self.entrada_titulo.set_text(self.libro_editar[1])
            self.entrada_autor.set_text(self.libro_editar[2])
            self.buffer_notas.set_text(self.libro_editar[6])
            generos = ["Ficción", "No Ficción", "Ciencia", "Historia"]
            self.combo_genero.set_active(generos.index(self.libro_editar[3]))
            self.radio_fisico.set_active(self.libro_editar[4] == "Físico")
            self.radio_digital.set_active(self.libro_editar[4] == "Digital")
            self.check_leido.set_active(bool(self.libro_editar[5]))


    def on_guardar_clicked(self, widget):
        """
            funcion para guardar los libros
        """
        titulo = self.entrada_titulo.get_text().strip()
        autor = self.entrada_autor.get_text().strip()

        if not titulo or not autor:
            dialogo = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error de Validación")
            dialogo.format_secondary_text("El título y el autor son obligatorios.")
            dialogo.run()
            dialogo.destroy()
            return

        genero = self.combo_genero.get_active_text()
        formato = "Físico" if self.radio_fisico.get_active() else "Digital"
        leido = 1 if self.check_leido.get_active() else 0
        notas = self.buffer_notas.get_text(self.buffer_notas.get_start_iter(), self.buffer_notas.get_end_iter(), True)

        if self.libro_editar:
            conexionBD.actualizar_libro(self.libro_editar[0], titulo, autor, genero, formato, leido, notas)
        else:
            conexionBD.insertar_libro(titulo, autor, genero, formato, leido, notas)

        self.padre.cargar_datos()
        self.destroy()