import unittest
import os
import conexionBD


class TestBaseDeDatos(unittest.TestCase):
    """clase para las pruebas unitarias de las funciones CRUD de la base de datos."""

    def setUp(self):
        """funcion para preparar todo, cambiamos el nombre de la BD para no estropear la nuestra"""
        conexionBD.NOMBRE_BD = "bd_pruebas.db"
        conexionBD.crear_tabla()

    def tearDown(self):
        """funcion que se ejecuta despues de cada prueba para que quede mas limpio"""
        if os.path.exists("bd_pruebas.db"):
            os.remove("bd_pruebas.db")

    def test_insertar_y_obtener_libro(self):
        """Prueba que un libro se inserta y se lee correctamente."""
        conexionBD.insertar_libro("El Quijote", "Cervantes", "Ficción", "Físico", 1, "Un clásico.")

        libros = conexionBD.obtener_libros()

        # Comprobamos que hay exactamente 1 libro en la base de datos
        self.assertEqual(len(libros), 1)
        # Comprobamos que el título guardado coincide
        self.assertEqual(libros[0][1], "El Quijote")

    def test_actualizar_libro(self):
        """Prueba que los datos de un libro se modifican correctamente."""
        # Insertamos un libro de prueba
        conexionBD.insertar_libro("Libro Antiguo", "Autor", "Ciencia", "Digital", 0, "")
        libros = conexionBD.obtener_libros()
        id_libro = libros[0][0]

        # Lo actualizamos
        conexionBD.actualizar_libro(id_libro, "Libro Nuevo", "Autor", "Ciencia", "Digital", 1, "Actualizado")

        # Lo recuperamos y comprobamos los cambios
        libros_actualizados = conexionBD.obtener_libros()
        self.assertEqual(libros_actualizados[0][1], "Libro Nuevo")  # El título cambió
        self.assertEqual(libros_actualizados[0][5], 1)  # El estado leído cambió a 1

    def test_borrar_libro(self):
        """Prueba que un libro se elimina de la base de datos."""
        # Insertamos un libro
        conexionBD.insertar_libro("Libro para borrar", "Autor", "Historia", "Físico", 0, "")
        libros_antes = conexionBD.obtener_libros()
        id_libro = libros_antes[0][0]

        # Nos aseguramos de que hay 1 libro
        self.assertEqual(len(libros_antes), 1)

        # Lo borramos
        conexionBD.borrar_libro(id_libro)

        # Comprobamos que la base de datos ahora está vacía
        libros_despues = conexionBD.obtener_libros()
        self.assertEqual(len(libros_despues), 0)


if __name__ == '__main__':
    unittest.main()