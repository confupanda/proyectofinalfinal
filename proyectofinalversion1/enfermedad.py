import random

class Enfermedad:
    def __init__(self, infeccion_probable, duracion_infeccion):
        self.infeccion_probable = infeccion_probable
        self.duracion_infeccion = duracion_infeccion

    def es_infeccioso(self):
        return random.random() < self.infeccion_probable

#define la clase Enfermedad que contiene la probabilidad de infección y la duración de la infección
#el metodo es_infeccioso determina si la infección ocurre basado en la probabilidad.