from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from Libro import Libro  # Asumiendo que Libro es una clase existente en tu proyecto
import sqlite3

class ListaLibrosWindow(QWidget):
    def __init__(self, biblioteca):
        super().__init__()
        self.setWindowTitle("Lista de Libros")
        self.setGeometry(500, 200, 400, 400)

        self.biblioteca = biblioteca
        self.conn = sqlite3.connect('biblioteca.db')
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.listbox_books = QListWidget(self)
        layout.addWidget(self.listbox_books)

        self.btn_refresh = QPushButton("Actualizar Lista", self)
        self.btn_refresh.setMinimumHeight(40)
        self.btn_refresh.setStyleSheet("font-size: 14px;")
        self.btn_refresh.clicked.connect(self.refresh_list)
        layout.addWidget(self.btn_refresh)

        self.refresh_list()

    def refresh_list(self):
        """Refresca la lista de libros."""
        self.listbox_books.clear()
        self.cursor.execute("SELECT * FROM libros")
        rows = self.cursor.fetchall()
        for row in rows:
            titulo, autor_nombre, categoria_nombre = row
            libro = Libro(titulo, autor_nombre, categoria_nombre)
            estado = "Disponible" if not libro.esta_prestado() else "Prestado"
            self.listbox_books.addItem(f"{libro.titulo} - Estado: {estado}")

    def add_book_to_db(self, libro):
        """Agrega un libro a la base de datos."""
        self.cursor.execute("INSERT INTO libros (titulo, autor, categoria) VALUES (?, ?, ?)",
                            (libro.titulo, libro.autor.nombre, libro.categoria.nombre))
        self.conn.commit()

    def update_list_from_db(self):
        """Actualiza la lista de libros desde la base de datos."""
        self.listbox_books.clear()
        self.cursor.execute("SELECT * FROM libros")
        rows = self.cursor.fetchall()
        for row in rows:
            titulo, autor_nombre, categoria_nombre = row
            libro = Libro(titulo, autor_nombre, categoria_nombre)
            estado = "Disponible" if not libro.esta_prestado() else "Prestado"
            self.listbox_books.addItem(f"{libro.titulo} - Estado: {estado}")