from Libro import Libro
from Autor import Autor
from Categoria import Categoria

class LibrosPredeterminados:
    @staticmethod
    def obtener_libros():
        autor1 = Autor("Gabriel", "García Márquez")
        categoria1 = Categoria("Literatura Latinoamericana")
        libro1 = Libro("Cien años de soledad", "978-84-376-0494-7", autor1, categoria1)

        autor2 = Autor("J.K.", "Rowling")
        categoria2 = Categoria("Fantasía")
        libro2 = Libro("Harry Potter y la piedra filosofal", "978-84-9838-293-4", autor2, categoria2)

        autor3 = Autor("J.R.R.", "Tolkien")
        categoria3 = Categoria("Fantasía")
        libro3 = Libro("El Señor de los Anillos: La Comunidad del Anillo", "978-84-450-7675-0", autor3, categoria3)

        autor4 = Autor("Stephen", "King")
        categoria4 = Categoria("Ficción de terror")
        libro4 = Libro("It", "978-84-670-3830-2", autor4, categoria4)

        autor5 = Autor("Agatha", "Christie")
        categoria5 = Categoria("Novela policíaca")
        libro5 = Libro("Asesinato en el Orient Express", "978-84-9759-887-1", autor5, categoria5)

        return [libro1, libro2, libro3, libro4, libro5]
