import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QListWidget, QMessageBox, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
import sqlite3
from Libro import Libro
from Autor import Autor
from Categoria import Categoria
from Usuario import Usuario
from Biblioteca import Biblioteca
from predeterminados import LibrosPredeterminados

class BibliotecaApp(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biblioteca App")
        
        # Inicializa la interfaz de usuario
        self.setup_ui()
        # Inicializa la base de datos
        self.initialize_db()

        # Inicializa la biblioteca con libros predefinidos
        self.initialize_library()

        # Usuario actualmente logueado
        self.current_user = None

    def setup_ui(self):
            """Configura la interfaz de usuario inicial."""
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            # Layout principal para centrar el contenido
            self.main_layout = QVBoxLayout(self.central_widget)
            self.main_layout.setAlignment(Qt.AlignCenter)
            self.main_layout.setContentsMargins(20, 20, 20, 20)  # Márgenes
            self.main_layout.setSpacing(15)  # Espaciado

            # Título de bienvenida
            self.label_title = QLabel("Bienvenido a la Biblioteca")
            self.label_title.setStyleSheet("font-size: 18px; font-weight: bold;")
            self.main_layout.addWidget(self.label_title, alignment=Qt.AlignCenter)

            # Botón para iniciar sesión
            self.btn_login = QPushButton("Iniciar Sesión", self)
            self.btn_login.setMinimumHeight(40)
            self.btn_login.setStyleSheet("font-size: 14px;")
            self.btn_login.clicked.connect(self.open_login_window)
            self.main_layout.addWidget(self.btn_login)

            # Botón para registrarse
            self.btn_register = QPushButton("Registrarse", self)
            self.btn_register.setMinimumHeight(40)
            self.btn_register.setStyleSheet("font-size: 14px;")
            self.btn_register.clicked.connect(self.open_register_window)
            self.main_layout.addWidget(self.btn_register)

            # Botón para salir
            self.btn_exit = QPushButton("Salir", self)
            self.btn_exit.setMinimumHeight(40)
            self.btn_exit.setStyleSheet("font-size: 14px;")
            self.btn_exit.clicked.connect(QApplication.quit)
            self.main_layout.addWidget(self.btn_exit)

    def initialize_db(self):
        """Inicializa la base de datos y crea la tabla de usuarios si no existe."""
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            username TEXT,
            password TEXT,
            es_admin INTEGER
        )
    ''')
    conn.commit()
    conn.close()

    def initialize_library(self):
            """Crea la biblioteca y agrega libros predefinidos."""
            self.biblioteca = Biblioteca()
            libros_predefinidos = LibrosPredeterminados.obtener_libros()
            for libro in libros_predefinidos:
                self.biblioteca.registrar_libro(libro)

    def open_login_window(self):
            """Abre la ventana de inicio de sesión."""
            self.login_window = QWidget()
            self.login_window.setWindowTitle("Inicio de Sesión")
            self.login_window.setGeometry(500, 200, 300, 200)

            # Layout para el formulario de inicio de sesión
            self.layout_login = QVBoxLayout(self.login_window)
            self.layout_login.setAlignment(Qt.AlignCenter)
            self.layout_login.setContentsMargins(20, 20, 20, 20)
            self.layout_login.setSpacing(15)

            # Campo de texto para el nombre de usuario
            self.label_username = QLabel("Nombre de Usuario:")
            self.layout_login.addWidget(self.label_username)
            self.entry_username = QLineEdit()
            self.layout_login.addWidget(self.entry_username)

            # Botón para inicio de sesión administrativo (si es necesario)
            self.admin_button = QPushButton()
            self.admin_button.setFixedSize(30, 30)  # Tamaño del botón cuadrado
            self.admin_button.setStyleSheet("background-color: #ccc; border: 1px solid #666;")
            self.layout_login.addWidget(self.admin_button)
            self.admin_button.clicked.connect(self.open_admin_login)

            # Campo de texto para la contraseña
            self.label_password = QLabel("Contraseña:")
            self.layout_login.addWidget(self.label_password)
            self.entry_password = QLineEdit()
            self.entry_password.setEchoMode(QLineEdit.Password)
            self.layout_login.addWidget(self.entry_password)

            # Botón para iniciar sesión
            self.btn_login_user = QPushButton("Iniciar Sesión", self.login_window)
            self.btn_login_user.setMinimumHeight(40)
            self.btn_login_user.setStyleSheet("font-size: 14px;")
            self.btn_login_user.clicked.connect(self.login_user)
            self.layout_login.addWidget(self.btn_login_user)

            # Botón para volver
            self.btn_back = QPushButton("Volver", self.login_window)
            self.btn_back.setMinimumHeight(40)
            self.btn_back.setStyleSheet("font-size: 14px;")
            self.btn_back.clicked.connect(self.login_window.close)
            self.layout_login.addWidget(self.btn_back)

            self.login_window.show()

    def login_user(self):
        """Verifica las credenciales del usuario y lo autentica."""
        username = self.entry_username.text()
        password = self.entry_password.text()
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nombre, apellido FROM usuarios WHERE username=? AND password=?
        ''', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.current_user = Usuario(user[1], user[2], user[0], password)
            QMessageBox.information(self.login_window, "Inicio de Sesión", f"Bienvenido, {self.current_user.nombre}!")
            self.login_window.close()
            self.central_widget.hide()  # Oculta la ventana de inicio después del login
            self.open_menu_window()
        else:
            QMessageBox.critical(self.login_window, "Error", "Usuario o contraseña incorrectos.")


    def open_register_window(self):
                    """Abre la ventana de registro de usuario."""
                    self.register_window = QWidget()
                    self.register_window.setWindowTitle("Registro de Usuario")
                    self.register_window.setGeometry(500, 200, 300, 300)

                    # Configuración del layout de registro
                    self.layout_register = QVBoxLayout(self.register_window)
                    self.layout_register.setAlignment(Qt.AlignCenter)
                    self.layout_register.setContentsMargins(20, 20, 20, 20)
                    self.layout_register.setSpacing(15)

                    # Título del formulario de registro
                    self.label_register_title = QLabel("Registro de Usuario")
                    self.label_register_title.setStyleSheet("font-size: 18px; font-weight: bold;")
                    self.layout_register.addWidget(self.label_register_title, alignment=Qt.AlignCenter)

                    # Campo de texto para el nombre
                    self.label_register_name = QLabel("Nombre:")
                    self.layout_register.addWidget(self.label_register_name)
                    self.entry_register_name = QLineEdit()
                    self.layout_register.addWidget(self.entry_register_name)

                    # Campo de texto para el apellido
                    self.label_register_last_name = QLabel("Apellido:")
                    self.layout_register.addWidget(self.label_register_last_name)
                    self.entry_register_last_name = QLineEdit()
                    self.layout_register.addWidget(self.entry_register_last_name)

                    # Campo de texto para el nombre de usuario
                    self.label_register_username = QLabel("Nombre de Usuario:")
                    self.layout_register.addWidget(self.label_register_username)
                    self.entry_register_username = QLineEdit()
                    self.layout_register.addWidget(self.entry_register_username)

                    # Campo de texto para la contraseña
                    self.label_register_password = QLabel("Contraseña:")
                    self.layout_register.addWidget(self.label_register_password)
                    self.entry_register_password = QLineEdit()
                    self.entry_register_password.setEchoMode(QLineEdit.Password)
                    self.layout_register.addWidget(self.entry_register_password)

                    # Botón para registrar al usuario
                    self.btn_register_user = QPushButton("Registrar", self.register_window)
                    self.btn_register_user.setMinimumHeight(40)
                    self.btn_register_user.setStyleSheet("font-size: 14px;")
                    self.btn_register_user.clicked.connect(self.register_user)
                    self.layout_register.addWidget(self.btn_register_user)

                    # Botón para volver a la ventana anterior
                    self.btn_back = QPushButton("Volver", self.register_window)
                    self.btn_back.setMinimumHeight(40)
                    self.btn_back.setStyleSheet("font-size: 14px;")
                    self.btn_back.clicked.connect(self.register_window.close)
                    self.layout_register.addWidget(self.btn_back)

                    self.register_window.show()

    def register_user(self):
                """Registra un nuevo usuario en la base de datos."""
                nombre = self.entry_register_name.text()
                apellido = self.entry_register_last_name.text()
                username = self.entry_register_username.text()
                password = self.entry_register_password.text()

                if nombre and apellido and username and password:
                    try:
                        # Conectar a la base de datos
                        conn = sqlite3.connect('biblioteca.db')
                        cursor = conn.cursor()
                        
                        # Insertar el nuevo usuario en la base de datos
                        cursor.execute('''
                            INSERT INTO usuarios (nombre, apellido, username, password)
                            VALUES (?, ?, ?, ?)
                        ''', (nombre, apellido, username, password))
                        conn.commit()
                        conn.close()
                        
                        # Mostrar mensaje de éxito
                        QMessageBox.information(self.register_window, "Registro", f"Usuario '{username}' registrado con éxito.")
                        self.register_window.close()
                    except sqlite3.IntegrityError:
                        # Mostrar mensaje de error si el nombre de usuario ya está en uso
                        QMessageBox.critical(self.register_window, "Error", f"El nombre de usuario '{username}' ya está en uso.")
                else:
                    # Mostrar mensaje de error si algún campo está vacío
                    QMessageBox.critical(self.register_window, "Error", "Por favor completa todos los campos.")

            
    def open_menu_window(self):
                    """Abre la ventana del menú principal."""
                # Configuración de la ventana del menú principal
                    self.menu_window = QWidget()
                    self.menu_window.setWindowTitle("Menú Principal")
                    self.menu_window.setGeometry(500, 200, 300, 200)

                    # Configuración del layout del menú principal
                    self.layout_menu = QVBoxLayout(self.menu_window)
                    self.layout_menu.setAlignment(Qt.AlignCenter)
                    self.layout_menu.setContentsMargins(20, 20, 20, 20)
                    self.layout_menu.setSpacing(15)

                    # Título del menú principal
                    self.label_menu_title = QLabel("Menú Principal")
                    self.label_menu_title.setStyleSheet("font-size: 18px; font-weight: bold;")
                    self.layout_menu.addWidget(self.label_menu_title, alignment=Qt.AlignCenter)

                    # Botón para buscar un libro
                    self.btn_search = QPushButton("Buscar Libro", self.menu_window)
                    self.btn_search.setMinimumHeight(40)
                    self.btn_search.setStyleSheet("font-size: 14px;")
                    self.btn_search.clicked.connect(self.open_search_window)
                    self.layout_menu.addWidget(self.btn_search)

                    # Botón para prestar un libro
                    self.btn_loan = QPushButton("Prestar Libro", self.menu_window)
                    self.btn_loan.setMinimumHeight(40)
                    self.btn_loan.setStyleSheet("font-size: 14px;")
                    self.btn_loan.clicked.connect(self.open_loan_window)
                    self.layout_menu.addWidget(self.btn_loan)

                    # Botón para cerrar sesión
                    self.btn_logout = QPushButton("Cerrar Sesión", self.menu_window)
                    self.btn_logout.setMinimumHeight(40)
                    self.btn_logout.setStyleSheet("font-size: 14px;")
                    self.btn_logout.clicked.connect(self.logout_user)
                    self.layout_menu.addWidget(self.btn_logout)

                    self.menu_window.show()

    def open_search_window(self):
                """Abre la ventana de búsqueda de libros."""
                # Configuración de la ventana de búsqueda de libros
                self.search_window = QWidget()
                self.search_window.setWindowTitle("Buscar Libro")
                self.search_window.setGeometry(500, 200, 400, 400)

                # Configuración del layout de búsqueda de libros
                self.layout_search = QVBoxLayout(self.search_window)
                self.layout_search.setAlignment(Qt.AlignCenter)
                self.layout_search.setContentsMargins(20, 20, 20, 20)
                self.layout_search.setSpacing(15)

                # Título de la búsqueda de libros
                self.label_search_title = QLabel("Buscar Libro")
                self.label_search_title.setStyleSheet("font-size: 18px; font-weight: bold;")
                self.layout_search.addWidget(self.label_search_title, alignment=Qt.AlignCenter)

                # Campo de texto para el título del libro a buscar
                self.label_book_title = QLabel("Título del Libro:")
                self.layout_search.addWidget(self.label_book_title)
                self.entry_book_title = QLineEdit()
                self.layout_search.addWidget(self.entry_book_title)

                # Botón para realizar la búsqueda
                self.btn_search_book = QPushButton("Buscar", self.search_window)
                self.btn_search_book.setMinimumHeight(40)
                self.btn_search_book.setStyleSheet("font-size: 14px;")
                self.btn_search_book.clicked.connect(self.search_book)
                self.layout_search.addWidget(self.btn_search_book)

                # Lista para mostrar los resultados de búsqueda de libros
                self.listbox_books = QListWidget(self.search_window)
                self.layout_search.addWidget(self.listbox_books)

                # Limpiar la lista antes de insertar los libros predefinidos
                self.listbox_books.clear()

                # Insertar los libros predefinidos en el Listbox
                for libro in LibrosPredeterminados.obtener_libros():
                    self.listbox_books.addItem(libro.titulo)

                # Botón para ver los detalles del libro seleccionado
                self.btn_show_details = QPushButton("Ver Detalles", self.search_window)
                self.btn_show_details.setMinimumHeight(40)
                self.btn_show_details.setStyleSheet("font-size: 14px;")
                self.btn_show_details.clicked.connect(self.show_selected_book)
                self.layout_search.addWidget(self.btn_show_details)

                # Botón para volver a la ventana anterior
                self.btn_back = QPushButton("Volver", self.search_window)
                self.btn_back.setMinimumHeight(40)
                self.btn_back.setStyleSheet("font-size: 14px;")
                self.btn_back.clicked.connect(self.search_window.close)
                self.layout_search.addWidget(self.btn_back)

                self.search_window.show()

    def search_book(self):
                """Busca un libro por título en la biblioteca y muestra la información si se encuentra."""
                titulo = self.entry_book_title.text()
                libro = self.biblioteca.buscar_libro(titulo)
                if libro:
                    self.show_book_info(libro)
                else:
                    QMessageBox.critical(self.search_window, "Error", "Libro no encontrado.")

    def show_selected_book(self):
                """Muestra los detalles del libro seleccionado en la lista."""
                selected_items = self.listbox_books.selectedItems()
                if selected_items:
                    selected_book_title = selected_items[0].text()
                    libro = self.biblioteca.buscar_libro(selected_book_title)
                    if libro:
                        self.show_book_info(libro)
                    else:
                        QMessageBox.critical(self.search_window, "Error", "Libro no encontrado.")
                else:
                    QMessageBox.critical(self.search_window, "Error", "Por favor selecciona un libro de la lista.")

    def show_book_info(self, libro):
                """Muestra la información del libro en una nueva ventana."""
                # Configuración de la ventana de información del libro
                self.book_info_window = QWidget()
                self.book_info_window.setWindowTitle("Información del Libro")
                self.book_info_window.setGeometry(500, 200, 300, 200)

                # Configuración del layout de información del libro
                self.layout_book_info = QVBoxLayout(self.book_info_window)
                self.layout_book_info.setAlignment(Qt.AlignCenter)
                self.layout_book_info.setContentsMargins(20, 20, 20, 20)
                self.layout_book_info.setSpacing(15)

                # Mostrar el título del libro
                self.label_book_title_info = QLabel(f"Título: {libro.titulo}")
                self.layout_book_info.addWidget(self.label_book_title_info)

                # Mostrar el autor del libro
                self.label_book_author_info = QLabel(f"Autor: {libro.autor.nombre} {libro.autor.apellido}")
                self.layout_book_info.addWidget(self.label_book_author_info)

                # Mostrar la categoría del libro
                self.label_book_category_info = QLabel(f"Categoría: {libro.categoria.nombre}")
                self.layout_book_info.addWidget(self.label_book_category_info)

                # Mostrar el estado del libro (prestado o disponible)
                status_text = "Estado: Prestado" if libro.esta_prestado() else "Estado: Disponible"
                self.label_book_status_info = QLabel(status_text)
                self.layout_book_info.addWidget(self.label_book_status_info)

                # Botón para volver a la ventana anterior
                self.btn_back = QPushButton("Volver", self.book_info_window)
                self.btn_back.setMinimumHeight(40)
                self.btn_back.setStyleSheet("font-size: 14px;")
                self.btn_back.clicked.connect(self.book_info_window.close)
                self.layout_book_info.addWidget(self.btn_back)

                self.book_info_window.show()

    def open_loan_window(self):
                """Abre la ventana para prestar libros."""
                # Configuración de la ventana de préstamo de libros
                self.loan_window = QWidget()
                self.loan_window.setWindowTitle("Préstamo de Libro")
                self.loan_window.setGeometry(500, 200, 300, 200)

                # Configuración del layout de préstamo de libros
                self.layout_loan = QVBoxLayout(self.loan_window)
                self.layout_loan.setAlignment(Qt.AlignCenter)
                self.layout_loan.setContentsMargins(20, 20, 20, 20)
                self.layout_loan.setSpacing(15)

                # Título de la ventana de préstamo de libros
                self.label_loan_title = QLabel("Préstamo de Libro")
                self.label_loan_title.setStyleSheet("font-size: 18px; font-weight: bold;")
                self.layout_loan.addWidget(self.label_loan_title, alignment=Qt.AlignCenter)

                # Campo de texto para el título del libro a prestar
                self.label_book_title = QLabel("Título del Libro:")
                self.layout_loan.addWidget(self.label_book_title)
                self.entry_book_title = QLineEdit()
                self.layout_loan.addWidget(self.entry_book_title)

                # Botón para solicitar el préstamo del libro
                self.btn_loan_book = QPushButton("Pedir Prestado", self.loan_window)
                self.btn_loan_book.setMinimumHeight(40)
                self.btn_loan_book.setStyleSheet("font-size: 14px;")
                self.btn_loan_book.clicked.connect(self.loan_book)
                self.layout_loan.addWidget(self.btn_loan_book)

                # Botón para volver a la ventana anterior
                self.btn_back = QPushButton("Volver", self.loan_window)
                self.btn_back.setMinimumHeight(40)
                self.btn_back.setStyleSheet("font-size: 14px;")
                self.btn_back.clicked.connect(self.loan_window.close)
                self.layout_loan.addWidget(self.btn_back)

                self.loan_window.show()


    def open_admin_menu(self):
                """Abre la ventana del menú de administrador."""
                # Configuración de la ventana del menú de administrador
                self.admin_menu_window = QWidget()
                self.admin_menu_window.setWindowTitle("Menú de Administrador")
                self.admin_menu_window.setGeometry(500, 200, 300, 200)

                # Configuración del layout del menú de administrador
                self.layout_admin_menu = QVBoxLayout(self.admin_menu_window)
                self.layout_admin_menu.setAlignment(Qt.AlignCenter)
                self.layout_admin_menu.setContentsMargins(20, 20, 20, 20)
                self.layout_admin_menu.setSpacing(15)

                # Título del menú de administrador
                self.label_admin_menu_title = QLabel("Menú de Administrador")
                self.label_admin_menu_title.setStyleSheet("font-size: 18px; font-weight: bold;")
                self.layout_admin_menu.addWidget(self.label_admin_menu_title, alignment=Qt.AlignCenter)

                # Botón para agregar un nuevo libro
                self.btn_add_book = QPushButton("Agregar Libro", self.admin_menu_window)
                self.btn_add_book.setMinimumHeight(40)
                self.btn_add_book.setStyleSheet("font-size: 14px;")
                self.btn_add_book.clicked.connect(self.open_add_book_window)
                self.layout_admin_menu.addWidget(self.btn_add_book)

                # Botón para ver los detalles de un libro
                self.btn_view_book_details = QPushButton("Ver Detalles de Libro", self.admin_menu_window)
                self.btn_view_book_details.setMinimumHeight(40)
                self.btn_view_book_details.setStyleSheet("font-size: 14px;")
                self.btn_view_book_details.clicked.connect(self.open_view_book_details_window)
                self.layout_admin_menu.addWidget(self.btn_view_book_details)

                # Botón para cerrar sesión
                self.btn_logout = QPushButton("Cerrar Sesión", self.admin_menu_window)
                self.btn_logout.setMinimumHeight(40)
                self.btn_logout.setStyleSheet("font-size: 14px;")
                self.btn_logout.clicked.connect(self.logout_admin_user)
                self.layout_admin_menu.addWidget(self.btn_logout)

                self.admin_menu_window.show()

    def open_view_book_details_window(self):
                """Abre la ventana para ver los detalles de un libro."""
                # Configuración de la ventana para ver los detalles del libro
                self.view_book_details_window = QWidget()
                self.view_book_details_window.setWindowTitle("Ver Detalles de Libro")
                self.view_book_details_window.setGeometry(500, 200, 300, 200)

                # Configuración del layout para los detalles del libro
                self.layout_view_book_details = QVBoxLayout(self.view_book_details_window)
                self.layout_view_book_details.setAlignment(Qt.AlignCenter)
                self.layout_view_book_details.setContentsMargins(20, 20, 20, 20)
                self.layout_view_book_details.setSpacing(15)

                # Etiqueta y campo de texto para mostrar los detalles del libro
                self.label_book_title = QLabel("Título del Libro:")
                self.layout_view_book_details.addWidget(self.label_book_title)
                self.text_edit_book_details = QTextEdit()
                self.layout_view_book_details.addWidget(self.text_edit_book_details)

                # Botón para cerrar la ventana
                self.btn_close = QPushButton("Cerrar")
                self.btn_close.clicked.connect(self.view_book_details_window.close)
                self.layout_view_book_details.addWidget(self.btn_close)

                self.view_book_details_window.show()

    def open_admin_login(self):
                """Abre la ventana de inicio de sesión del administrador."""
                # Configuración de la ventana de inicio de sesión del administrador
                self.admin_login_window = QWidget()
                self.admin_login_window.setWindowTitle("Inicio de Sesión de Administrador")
                self.admin_login_window.setGeometry(500, 200, 200, 100)

                # Configuración del layout de inicio de sesión
                self.layout_admin_login = QVBoxLayout(self.admin_login_window)
                self.layout_admin_login.setAlignment(Qt.AlignCenter)
                self.layout_admin_login.setContentsMargins(20, 20, 20, 20)
                self.layout_admin_login.setSpacing(15)

                # Campo de texto para el nombre de usuario del administrador
                self.label_admin_username = QLabel("Nombre de Usuario:")
                self.layout_admin_login.addWidget(self.label_admin_username)
                self.entry_admin_username = QLineEdit()
                self.layout_admin_login.addWidget(self.entry_admin_username)

                # Campo de texto para la contraseña del administrador
                self.label_admin_password = QLabel("Contraseña:")
                self.layout_admin_login.addWidget(self.label_admin_password)
                self.entry_admin_password = QLineEdit()
                self.entry_admin_password.setEchoMode(QLineEdit.Password)
                self.layout_admin_login.addWidget(self.entry_admin_password)

                # Botón para iniciar sesión
                self.btn_admin_login = QPushButton("Iniciar Sesión")
                self.btn_admin_login.clicked.connect(self.admin_login)
                self.layout_admin_login.addWidget(self.btn_admin_login)

                self.admin_login_window.show()

    def admin_login(self):
                """Verifica las credenciales del administrador y abre el menú de administrador si son correctas."""
                username = self.entry_admin_username.text()
                password = self.entry_admin_password.text()

                if username == "admin" and password == "admin1":
                    try:
                        self.open_admin_menu()
                        self.admin_login_window.close()
                    except Exception as e:
                        print(f"Error: {e}")

    def open_add_book_window(self):
                """Abre la ventana para agregar un nuevo libro."""
                # Configuración de la ventana para agregar un nuevo libro
                self.add_book_window = QWidget()
                self.add_book_window.setWindowTitle("Agregar Nuevo Libro")
                self.add_book_window.setGeometry(500, 200, 400, 300)

                # Configuración del layout para agregar un nuevo libro
                self.layout_add_book = QVBoxLayout(self.add_book_window)
                self.layout_add_book.setAlignment(Qt.AlignCenter)
                self.layout_add_book.setContentsMargins(20, 20, 20, 20)
                self.layout_add_book.setSpacing(15)

                # Título de la ventana para agregar un nuevo libro
                self.label_add_book_title = QLabel("Agregar Nuevo Libro")
                self.label_add_book_title.setStyleSheet("font-size: 18px; font-weight: bold;")
                self.layout_add_book.addWidget(self.label_add_book_title, alignment=Qt.AlignCenter)

                # Campo de texto para el título del nuevo libro
                self.label_add_book_title = QLabel("Título del Libro:")
                self.layout_add_book.addWidget(self.label_add_book_title)
                self.entry_add_book_title = QLineEdit()
                self.layout_add_book.addWidget(self.entry_add_book_title)

                # Campo de texto para el autor del nuevo libro
                self.label_add_book_author = QLabel("Autor del Libro:")
                self.layout_add_book.addWidget(self.label_add_book_author)
                self.entry_add_book_author = QLineEdit()
                self.layout_add_book.addWidget(self.entry_add_book_author)

                # Cambiar de QComboBox a QLineEdit para la categoría del libro
                self.label_add_book_category = QLabel("Categoría del Libro:")
                self.layout_add_book.addWidget(self.label_add_book_category)
                self.entry_add_book_category = QLineEdit()  # Usamos QLineEdit para entrada de texto
                self.layout_add_book.addWidget(self.entry_add_book_category)

                # Botón para agregar el nuevo libro
                self.btn_add_book = QPushButton("Agregar Libro", self.add_book_window)
                self.btn_add_book.setMinimumHeight(40)
                self.btn_add_book.setStyleSheet("font-size: 14px;")
                self.btn_add_book.clicked.connect(self.add_new_book)
                self.layout_add_book.addWidget(self.btn_add_book)

                # Botón para volver a la ventana anterior
                self.btn_back = QPushButton("Volver", self.add_book_window)
                self.btn_back.setMinimumHeight(40)
                self.btn_back.setStyleSheet("font-size: 14px;")
                self.btn_back.clicked.connect(self.add_book_window.close)
                self.layout_add_book.addWidget(self.btn_back)

                self.add_book_window.show()


    def refresh_list(self):
                    """Refresca la lista de libros en la interfaz de usuario."""
                    self.listbox_books.clear()
                    for libro in self.biblioteca.libros:
                        estado = "Disponible" if not libro.esta_prestado() else "Prestado"
                        self.listbox_books.addItem(f"{libro.titulo} - Estado: {estado}")

    def add_new_book(self):
        """Agregar un nuevo libro a la biblioteca."""
        titulo = self.entry_add_book_title.text()
        autor_nombre = self.entry_add_book_author.text()
        categoria_nombre = self.entry_add_book_category.text()  # Obtener texto de QLineEdit

        if titulo and autor_nombre and categoria_nombre:
            # Buscar o crear el autor
            autor_existente = next((autor for autor in self.biblioteca.autores if autor.nombre == autor_nombre), None)
            if not autor_existente:
                autor_existente = Autor(autor_nombre, "")
                self.biblioteca.registrar_autor(autor_existente)

            # Crear una instancia de Categoria usando el nombre ingresado
            categoria = Categoria(categoria_nombre)

            # Crear el nuevo libro con la instancia de categoria
            nuevo_libro = Libro(titulo, autor_existente, categoria)

            # Registrar el libro en la biblioteca
            self.biblioteca.registrar_libro(nuevo_libro)

            # Actualizar la lista de libros en la interfaz si es necesario
            self.lista_libros_window.add_book_to_db(nuevo_libro)
            self.lista_libros_window.update_list_from_db()

            # Mostrar un mensaje de confirmación
            QMessageBox.information(self.add_book_window, "Agregar Libro", f"Libro '{titulo}' agregado con éxito.")

            # Limpiar los campos de entrada
            self.entry_add_book_title.clear()
            self.entry_add_book_author.clear()
            self.entry_add_book_category.clear()
        else:
            QMessageBox.critical(self.add_book_window, "Error", "Por favor completa todos los campos.")

    def logout_admin(self):
                """Cierra la sesión del administrador y muestra la interfaz de inicio."""
                self.admin_menu_window.close()
                self.show_start_window()
                

    def loan_book(self):
                """Intenta prestar un libro si está disponible."""
                titulo = self.entry_book_title.text()
                libro = self.biblioteca.buscar_libro(titulo)

                if libro:
                    if libro.esta_prestado():
                        # Mostrar mensaje de error si el libro ya está prestado
                        QMessageBox.critical(self.loan_window, "Error", "Este libro ya está prestado.")
                    else:
                        # Proceder con el préstamo del libro
                        self.borrow_book(libro)
                else:
                    # Mostrar mensaje de error si el libro no se encuentra
                    QMessageBox.critical(self.loan_window, "Error", "Libro no encontrado.")

    def borrow_book(self, libro):
                """Registra el préstamo de un libro a un usuario autenticado."""
                if self.current_user:
                    self.biblioteca.realizar_prestamo(libro, self.current_user)
                    QMessageBox.information(self.loan_window, "Préstamo", f"¡Libro '{libro.titulo}' prestado con éxito a {self.current_user.nombre}!")
                    self.loan_window.close()
                else:
                    # Mostrar mensaje de error si no hay usuario autenticado
                    QMessageBox.critical(self.loan_window, "Error", "Debes iniciar sesión para realizar préstamos.")

    def show_start_window(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set up the layout and UI elements for the login/registration window
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Add UI elements for login/registration
        self.label_title = QLabel("Bienvenido a la Biblioteca")
        self.layout.addWidget(self.label_title)

        self.btn_login = QPushButton("Iniciar Sesión")
        self.layout.addWidget(self.btn_login)

        self.btn_register = QPushButton("Registrarse")
        self.layout.addWidget(self.btn_register)

        # Connect buttons to their respective methods
        self.btn_login.clicked.connect(self.open_login_window)
        self.btn_register.clicked.connect(self.open_register_window)

        # Reset the UI to the initial state
        self.setup_ui()

    def logout_user(self):
                """Cierra la sesión del usuario actual y retorna a la interfaz de inicio."""
                self.current_user = None  # Deslogea al usuario actual
                self.menu_window.close()  # Cierra la ventana del menú principal
                self.show_start_window()  # Muestra la ventana inicial de login/registro
                self.admin_menu_window.close()

    def logout_admin_user(self):
                """Cierra la sesión del usuario actual y retorna a la interfaz de inicio."""
                self.current_user = None  # Deslogea al usuario actual
                self.admin_menu_window.close()  # Cierra la ventana del menú principal
                self.show_start_window()  # Muestra la ventana inicial de login/registro
                

    def close_all_windows(self):
                """Cierra todas las ventanas abiertas, excepto la ventana principal."""
                for widget in self.centralWidget().findChildren(QWidget):
                    if widget != self.central_widget:
                        widget.close()

    def exit_application(self):
            """Cierra la aplicación."""
            QApplication.quit()

            # Botones de la interfaz principal
            self.btn_admin_menu = QPushButton("Menú de Administrador", self)
            self.btn_admin_menu.setMinimumHeight(40)
            self.btn_admin_menu.setStyleSheet("font-size: 14px;")
            self.btn_admin_menu.clicked.connect(self.open_admin_menu_from_button)
            self.layout.addWidget(self.btn_admin_menu)
            self.btn_admin_menu.hide()  # Ocultar inicialmente el botón de administrador

            self.btn_register = QPushButton("Registrarse", self)
            self.btn_register.setMinimumHeight(40)
            self.btn_register.setStyleSheet("font-size: 14px;")
            self.btn_register.clicked.connect(self.open_register_window)
            self.layout.addWidget(self.btn_register)

            self.btn_exit = QPushButton("Salir", self)
            self.btn_exit.setMinimumHeight(40)
            self.btn_exit.setStyleSheet("font-size: 14px;")
            self.btn_exit.clicked.connect(QApplication.quit)
            self.layout.addWidget(self.btn_exit)

def main():
    app = QApplication(sys.argv)
    biblioteca_app = BibliotecaApp()
    biblioteca_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()