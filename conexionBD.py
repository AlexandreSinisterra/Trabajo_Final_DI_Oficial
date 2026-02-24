import sqlite3
"""
    clase para conexion y metodos CRUD para la ddbb
"""
NOMBRE_BD = "biblioteca.db"

def conectar():
    """
        funcion para conectar a la ddbb
    """
    return sqlite3.connect(NOMBRE_BD)



def crear_tabla():
    """
        funcion de creación de tablas
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT,
            formato TEXT,
            leido INTEGER,
            notas TEXT
        )
    ''')
    conexion.commit()
    conexion.close()



def insertar_libro(titulo, autor, genero, formato, leido, notas):
    """
        funcion de insercion de libros
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO libros (titulo, autor, genero, formato, leido, notas)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, autor, genero, formato, leido, notas))
    conexion.commit()
    conexion.close()



def obtener_libros():
    """
        funcion de obtencion de libros
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM libros')
    filas = cursor.fetchall()
    conexion.close()
    return filas



def actualizar_libro(id_libro, titulo, autor, genero, formato, leido, notas):
    """
        funcion de actualizacion de libros
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE libros SET titulo=?, autor=?, genero=?, formato=?, leido=?, notas=?
        WHERE id=?
    ''', (titulo, autor, genero, formato, leido, notas, id_libro))
    conexion.commit()
    conexion.close()



def borrar_libro(id_libro):
    """
        funcion de borrado de libros
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM libros WHERE id=?', (id_libro,))
    conexion.commit()
    conexion.close()



def actualizar_estado_leido(id_libro, leido):
    """
        funcion de actualizacion de leido de un libro (a traves de checkboxes en el treeview)
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('UPDATE libros SET leido=? WHERE id=?', (leido, id_libro))
    conexion.commit()
    conexion.close()

crear_tabla()