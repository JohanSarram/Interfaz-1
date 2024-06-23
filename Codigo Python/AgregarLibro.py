from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from Libro import Libro  # Asumiendo que Libro es una clase existente en tu proyecto
from Autor import Autor  # Asumiendo que Autor es una clase existente en tu proyecto
from Categoria import Categoria  # Asumiendo que Categoria es una clase existente en tu proyecto


class AgregarLibroWindow(QWidget):
    def __init__(self, biblioteca):
        super().__init__()
        self.setWindowTitle("Agregar Libro")
        self.setGeometry(500, 200, 300, 300)

        self.biblioteca = biblioteca

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.label_title = QLabel("Añadir Libro")
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label_title, alignment=Qt.AlignCenter)

        self.label_name = QLabel("Nombre:")
        layout.addWidget(self.label_name)
        self.entry_name = QLineEdit()
        layout.addWidget(self.entry_name)

        self.label_author = QLabel("Autor:")
        layout.addWidget(self.label_author)
        self.entry_author = QLineEdit()
        layout.addWidget(self.entry_author)

        self.label_category = QLabel("Categoría:")
        layout.addWidget(self.label_category)
        self.entry_category = QLineEdit()
        layout.addWidget(self.entry_category)

        self.btn_add = QPushButton("Añadir", self)
        self.btn_add.setMinimumHeight(40)
        self.btn_add.setStyleSheet("font-size: 14px;")
        self.btn_add.clicked.connect(self.add_book)
        layout.addWidget(self.btn_add)

        self.btn_back = QPushButton("Volver", self)
        self.btn_back.setMinimumHeight(40)
        self.btn_back.setStyleSheet("font-size: 14px;")
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

    def add_book(self):
        """Añade un nuevo libro a la biblioteca."""
        nombre = self.entry_name.text().strip()
        autor_nombre = self.entry_author.text().strip()
        categoria_nombre = self.entry_category.text().strip()

        if nombre and autor_nombre and categoria_nombre:
            autor = Autor(autor_nombre)  # Crear objeto Autor (debes definir la clase Autor)
            categoria = Categoria(categoria_nombre)  # Crear objeto Categoria (debes definir la clase Categoria)
            libro = Libro(nombre, autor, categoria)  # Crear objeto Libro (debes definir la clase Libro)
            self.biblioteca.registrar_libro(libro)
            QMessageBox.information(self, "Añadir Libro", f"Libro '{nombre}' añadido con éxito.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Por favor completa todos los campos.")
