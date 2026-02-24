import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import conexionBD
from ventanas.ventana_formulario import VentanaFormulario
from ventanas.ventana_notas import VentanaNotas


class VentanaPrincipal(Gtk.Window):
    """
        clase de la ventana principal que contiene el treeview de los datos de los libros
    """

    def __init__(self):
        """
            funcion para construir la estructura de la pagina
        """
        super().__init__(title="Gestión de Biblioteca")
        self.set_default_size(700, 400)
        self.connect("destroy", Gtk.main_quit)

        caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(caja_principal)

        # modelo de datos (ID, Título, Autor, Género, Formato, Leído, notas)
        self.modelo = Gtk.ListStore(int, str, str, str, str, bool, bool)
        self.treeview = Gtk.TreeView(model=self.modelo)

        # columnas de texto
        titulos = ["ID", "Título", "Autor", "Género", "Formato"]
        for i, titulo in enumerate(titulos):
            renderer = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(titulo, renderer, text=i)
            self.treeview.append_column(columna)

        # columna de Checkbox para leido
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_leido_toggled)
        columna_leido = Gtk.TreeViewColumn("Leído", renderer_toggle, active=5)
        self.treeview.append_column(columna_leido)

        renderer_toggle2 = Gtk.CellRendererToggle()
        renderer_toggle2.set_property('activatable', False)
        columna_notas = Gtk.TreeViewColumn("Notas", renderer_toggle2, active=6)
        self.treeview.append_column(columna_notas)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.treeview)
        caja_principal.pack_start(scroll, True, True, 0)

        # botones
        caja_botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_agregar = Gtk.Button(label="Agregar")
        btn_editar = Gtk.Button(label="Editar")
        btn_eliminar = Gtk.Button(label="Eliminar")
        btn_notas = Gtk.Button(label="Ver Notas")

        btn_agregar.connect("clicked", self.on_agregar_clicked)
        btn_editar.connect("clicked", self.on_editar_clicked)
        btn_eliminar.connect("clicked", self.on_eliminar_clicked)
        btn_notas.connect("clicked", self.on_ver_notas_clicked)

        caja_botones.pack_start(btn_agregar, True, True, 0)
        caja_botones.pack_start(btn_editar, True, True, 0)
        caja_botones.pack_start(btn_eliminar, True, True, 0)
        caja_botones.pack_start(btn_notas, True, True, 0)
        caja_principal.pack_start(caja_botones, False, False, 0)

        self.cargar_datos()


    def cargar_datos(self):
        """
            funcion para cargar los datos de los libros en el treeview
        """
        self.modelo.clear()
        libros = conexionBD.obtener_libros()
        for libro in libros:
            notas = bool(libro[6] and libro[6].strip())

            self.modelo.append([libro[0], libro[1], libro[2], libro[3], libro[4], bool(libro[5]), notas])


    def on_leido_toggled(self, widget, path):
        """
            funcion para cambiar el leido clickando en la checkbox
        """
        estado_actual = self.modelo[path][5]
        nuevo_estado = not estado_actual

        self.modelo[path][5] = nuevo_estado

        id_libro = self.modelo[path][0]
        estado_bd = 1 if nuevo_estado else 0
        conexionBD.actualizar_estado_leido(id_libro, estado_bd)


    def on_agregar_clicked(self, widget):
        """
            funcion para abrir la ventana de formulario para agregar un libro
        """
        dialogo = VentanaFormulario(self)
        dialogo.show_all()


    def on_editar_clicked(self, widget):
        """
            funcion para abrir la ventana de formulario para editar un libro
        """
        seleccion = self.treeview.get_selection()
        modelo, iterador = seleccion.get_selected()
        if iterador:
            id_libro = modelo[iterador][0]
            libros = conexionBD.obtener_libros()
            libro_editar = next(l for l in libros if l[0] == id_libro)
            dialogo = VentanaFormulario(self, libro_editar)
            dialogo.show_all()
        else:
            self.mostrar_alerta_seleccion()


    def on_eliminar_clicked(self, widget):
        """
            funcion para eliminar un libro
        """
        seleccion = self.treeview.get_selection()
        modelo, iterador = seleccion.get_selected()
        if iterador:
            id_libro = modelo[iterador][0]
            dialogo = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                        Gtk.ButtonsType.YES_NO, "Confirmar eliminación")
            dialogo.format_secondary_text(f"¿Estás seguro de que quieres eliminar el libro con el ID {id_libro}?")
            respuesta = dialogo.run()
            if respuesta == Gtk.ResponseType.YES:
                conexionBD.borrar_libro(id_libro)
                self.cargar_datos()
            dialogo.destroy()
        else:
            self.mostrar_alerta_seleccion()


    def on_ver_notas_clicked(self, widget):
        """
            funcion para abrir la ventana de notaas de un libro
        """
        seleccion = self.treeview.get_selection()
        modelo, iterador = seleccion.get_selected()
        if iterador:
            id_libro = modelo[iterador][0]
            libros = conexionBD.obtener_libros()
            # Buscamos el libro en la base de datos
            libro_seleccionado = next((l for l in libros if l[0] == id_libro), None)

            if libro_seleccionado:
                titulo = libro_seleccionado[1]  # El índice 1 es el título
                notas = libro_seleccionado[6]  # El índice 6 son las notas
                dialogo = VentanaNotas(self, titulo, notas)
                dialogo.show_all()
        else:
            self.mostrar_alerta_seleccion()


    def mostrar_alerta_seleccion(self):
        """
            funcion para mostrar un aviso por si no esta seleccionado ningun libro e intentas hacer algo que no puedes
        """
        dialogo = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Atención")
        dialogo.format_secondary_text("Por favor, selecciona primero un libro de la lista.")
        dialogo.run()
        dialogo.destroy()