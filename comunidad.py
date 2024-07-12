import json
import random
from ciudadano import Ciudadano

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.num_infectados = num_infectados
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.ciudadanos = self.generar_ciudadanos()

    def generar_ciudadanos(self):
        try:
            with open('nombres_apellidos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                nombres = data['nombres']
                apellidos = data['apellidos']
        except FileNotFoundError:
            print("El archivo 'nombres_apellidos.json' no se encuentra en el directorio.")
            return []

        ciudadanos = []
        for i in range(self.num_ciudadanos):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            familia = apellido
            ciudadano = Ciudadano(id=i, nombre=nombre, apellido=apellido, familia=familia)
            ciudadanos.append(ciudadano)

        infectados = random.sample(ciudadanos, self.num_infectados)
        for infectado in infectados:
            infectado.infectar(self.enfermedad)

        return ciudadanos

    def __str__(self):
        return f"Comunidad({len(self.ciudadanos)} ciudadanos, {self.num_infectados} infectados inicialmente)"
