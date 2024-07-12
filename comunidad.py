import random
import json
import csv

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.num_infectados = num_infectados
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.num_contagios = num_infectados
        self.ciudadanos = self.generar_ciudadanos()
        self.dia_actual = 0

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
            nombre = random.choice(nombres) + " " + random.choice(apellidos)
            edad = random.randint(1, 100)
            infectado = i < self.num_infectados
            duracion_infeccion = self.enfermedad.duracion_infeccion if infectado else 0
            ciudadano = {"nombre": nombre, "edad": edad, "infectado": infectado, "dias_infectado": duracion_infeccion}
            ciudadanos.append(ciudadano)
        return ciudadanos

    def paso(self):
        nuevos_infectados = 0
        for ciudadano in self.ciudadanos:
            if ciudadano['infectado']:
                ciudadano['dias_infectado'] -= 1
                if ciudadano['dias_infectado'] <= 0:
                    ciudadano['infectado'] = False
                    self.num_infectados -= 1

                contactos = random.choices(self.ciudadanos, k=self.promedio_conexion_fisica)
                for contacto in contactos:
                    if not contacto['infectado'] and not contacto['dias_infectado'] and random.random() < self.probabilidad_conexion_fisica:
                        contacto['infectado'] = True
                        contacto['dias_infectado'] = self.enfermedad.duracion_infeccion
                        nuevos_infectados += 1
        self.num_infectados += nuevos_infectados
        self.num_contagios += nuevos_infectados

        # Imprimir detalles de cada ciudadano
        for ciudadano in self.ciudadanos:
            print(f"Nombre: {ciudadano['nombre']}, Edad: {ciudadano['edad']}, Infectado: {ciudadano['infectado']}")

        print(f"El total de contagios de la comunidad: {self.num_contagios}; casos activos: {self.num_infectados}.")

        # Registrar los datos en el archivo CSV
        with open('resultados.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.dia_actual, self.num_contagios, self.num_infectados])
        
        self.dia_actual += 1
