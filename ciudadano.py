class Ciudadano:
    def __init__(self, id, nombre, apellido, familia):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = familia
        self.enfermedad = None
        self.estado = True  # True para sano, False para infectado

    def infectar(self, enfermedad):
        self.enfermedad = enfermedad
        self.estado = False  # Ahora está infectado

    def __str__(self):
        return f"Ciudadano({self.id}, {self.nombre} {self.apellido}, {self.familia}, {self.enfermedad})"
