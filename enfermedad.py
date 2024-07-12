import random

class Enfermedad:
    def __init__(self, infeccion_probable, duracion_infeccion):
        self.infeccion_probable = infeccion_probable
        self.duracion_infeccion = duracion_infeccion

    def es_infeccioso(self):
        return random.random() < self.infeccion_probable

