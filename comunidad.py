import random
import json
import pandas as pd
import numpy as np
import csv

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.num_infectados = num_infectados
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.num_contagios = num_infectados
        self.dia_actual = 0
        self.ciudadanos = self.generar_ciudadanos()
        self.guardar_ciudadanos_csv()
        
        #llama a los métodos para generar ciudadanos y guardar los datos en un archivo CSV.

    def generar_ciudadanos(self):
        try:
            with open('nombres_apellidos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                nombres = data['nombres']
                apellidos = data['apellidos']
        except FileNotFoundError:
            print("El archivo 'nombres_apellidos.json' no se encuentra en el directorio.")
            return pd.DataFrame()
        
        #este método lee un archivo JSON para obtener nombres y apellidos. 
        #si el archivo no se encuentra, muestra un mensaje de error y devuelve un DataFrame vacío.

        ciudadanos = pd.DataFrame({
            'id': range(1, self.num_ciudadanos + 1),
            'nombre': [random.choice(nombres) + " " + random.choice(apellidos) for _ in range(self.num_ciudadanos)],
            'edad': np.random.randint(1, 101, self.num_ciudadanos),
            'infectado': [i < self.num_infectados for i in range(self.num_ciudadanos)],
            'dias_infectado': [self.enfermedad.duracion_infeccion if i < self.num_infectados else 0 for i in range(self.num_ciudadanos)],
            'dia_infectado': [0 if i < self.num_infectados else -1 for i in range(self.num_ciudadanos)],
            'dia_sano': [-1 for _ in range(self.num_ciudadanos)]
        })
        return ciudadanos

#esta parte genera un DataFrame con la información de cada ciudadano:
#un ID, nombre completo, edad, si está infectado o no, días de infección, día de infección y día en que se curó.

    def guardar_ciudadanos_csv(self):
        self.ciudadanos.to_csv('ciudadanos.csv', index=False)
        
    
    #este metodo guarda el DataFrame de ciudadanos en un archivo CSV llamado ciudadanos.csv

    def paso(self):
        nuevos_infectados = 0
        infectados = self.ciudadanos[self.ciudadanos['infectado']]
        
        for idx, ciudadano in infectados.iterrows():
            self.ciudadanos.at[idx, 'dias_infectado'] -= 1
            if self.ciudadanos.at[idx, 'dias_infectado'] <= 0:
                self.ciudadanos.at[idx, 'infectado'] = False
                self.ciudadanos.at[idx, 'dias_infectado'] = -1
                self.ciudadanos.at[idx, 'dia_sano'] = self.dia_actual
                self.num_infectados -= 1
    
    #este método simula un día en la comunidad, primero decrementa el número de días infectados de cada ciudadano infectado
    #si los días infectados llegan a 0, el ciudadano se cura.

            contactos = self.ciudadanos.sample(self.promedio_conexion_fisica)
            for _, contacto in contactos.iterrows():
                if not contacto['infectado'] and not contacto['dias_infectado'] and random.random() < self.probabilidad_conexion_fisica:
                    self.ciudadanos.at[contacto.name, 'infectado'] = True
                    self.ciudadanos.at[contacto.name, 'dias_infectado'] = self.enfermedad.duracion_infeccion
                    self.ciudadanos.at[contacto.name, 'dia_infectado'] = self.dia_actual
                    nuevos_infectados += 1
        #para cada ciudadano infectado, selecciona una muestra de ciudadanos con los que tuvo contacto
        #si un contacto no está infectado y se cumple la probabilidad de infección, el contacto se infecta.            

        self.num_infectados += nuevos_infectados
        self.num_contagios += nuevos_infectados

        print(self.ciudadanos)
        print(f"El total de contagios de la comunidad: {self.num_contagios}; casos activos: {self.num_infectados}.")

        # Registrar los datos en el archivo CSV
        with open('resultados.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.dia_actual, self.num_contagios, self.num_infectados])

        self.dia_actual += 1
        self.guardar_ciudadanos_csv()
        
        #actualiza el número de infectados y el total de contagios, imprime el estado actual de la comunidad, 
        #guarda los resultados del día en un archivo CSV llamado resultados.csv
        #incrementa el día actual y guarda de nuevo los ciudadanos en el CSV.
        
