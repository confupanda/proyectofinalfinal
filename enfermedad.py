class Enfermedad:
    def __init__(self, infeccion_probable, promedio_pasos):
        self.infeccion_probable = infeccion_probable
        self.promedio_pasos = promedio_pasos

    def __str__(self):
        return f"Enfermedad(infeccion_probable={self.infeccion_probable}, promedio_pasos={self.promedio_pasos})"
