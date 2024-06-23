class Biblioteca:
    def __init__(self):
        self.libros = []

    def registrar_libro(self, libro):
        self.libros.append(libro)

    def buscar_libro(self, titulo):
        for libro in self.libros:
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    def realizar_prestamo(self, libro, usuario):
        libro.prestado = True

    def __init__(self):
        self.autores = []
        self.categorias = []
        self.libros = []

    def registrar_autor(self, autor):
        self.autores.append(autor)

    def registrar_categoria(self, categoria):
        self.categorias.append(categoria)

    def registrar_libro(self, libro):
        self.libros.append(libro)