

import random

import json

class Persona:
    def __init__(self, nombre, edad, infectado=False):
        self.nombre = nombre
        self.edad = edad
        self.infectado = infectado
        self.dias_infectado = 0

class Comunidad:
    def _init_(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.personas = self.generar_personas(num_ciudadanos)
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.infectar_personas_iniciales(num_infectados)
    
    def generar_personas(self, num_personas):
        with open('nombres_apellidos.json', 'r') as file:
            data = json.load(file)
        
        nombres = data["nombres"]
        apellidos = data["apellidos"]
        
        personas = []
        for i in range(num_personas):
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
            edad = random.randint(1, 100)
            persona = Persona(nombre, edad)
            personas.append(persona)
        
        return personas

    def infectar_personas_iniciales(self, num_infectados):
        infectados_iniciales = random.sample(self.personas, num_infectados)
        for persona in infectados_iniciales:
            persona.infectado = True

    def paso(self):
        nuevos_infectados = []
        
        for persona in self.personas:
            if persona.infectado:
                persona.dias_infectado += 1
                if persona.dias_infectado >= self.enfermedad.promedio_pasos:
                    persona.infectado = False
                    persona.dias_infectado = 0
            else:
                if random.random() < self.enfermedad.infeccion_probable:
                    nuevos_infectados.append(persona)
        
        for persona in nuevos_infectados:
            persona.infectado = True
    
    def obtener_total_infectados(self):
        return sum(1 for persona in self.personas if persona.infectado)