class Ciudadano:
    def __init__(self, id, nombre, apellido, familia, enfermedad=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = familia
        self.enfermedad = enfermedad
        self.estado = True  # True indica que el ciudadano está sano o recuperado

    def infectar(self, enfermedad):
        if self.estado:
            self.enfermedad = enfermedad
            self.estado = False  # False indica que el ciudadano está infectado

    def recuperar(self):
        if not self.estado and self.enfermedad is not None:
            self.enfermedad = None
            self.estado = True

    def __str__(self):
        estado = "Sano" if self.estado else "Infectado"
        return f"Ciudadano({self.id}, {self.nombre} {self.apellido}, {self.familia}, {estado})"
