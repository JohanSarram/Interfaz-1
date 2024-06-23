class Prestamo:
    def __init__(self, libro, usuario, fecha_prestamo, fecha_devolucion):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
    
    def mostrar_info(self):
        return f"Préstamo:\nLibro: {self.libro.mostrar_info()}\nUsuario: {self.usuario.mostrar_info()}\nFecha de préstamo: {self.fecha_prestamo}\nFecha de devolución: {self.fecha_devolucion}"
