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
        self.guardar_familias_csv()
        
    def generar_ciudadanos(self):
        try:
            with open('nombres_apellidos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                nombres = data['nombres']
                apellidos = data['apellidos']
        except FileNotFoundError:
            print("El archivo 'nombres_apellidos.json' no se encuentra en el directorio.")
            return pd.DataFrame()
        
        #carga nombres y apellidos de un archivo JSON 
        #si el archivo no se encuentra, imprime un mensaje de error y devuelve un DataFrame vacio
        
        ciudadanos = pd.DataFrame({
            'id': range(1, self.num_ciudadanos + 1),
            'nombre': [random.choice(nombres) + " " + random.choice(apellidos) for _ in range(self.num_ciudadanos)],
            'edad': np.random.randint(1, 101, self.num_ciudadanos),
            'infectado': [i < self.num_infectados for i in range(self.num_ciudadanos)],
            'dias_infectado': [self.enfermedad.duracion_infeccion if i < self.num_infectados else 0 for i in range(self.num_ciudadanos)],
            'dia_infectado': [0 if i < self.num_infectados else -1 for i in range(self.num_ciudadanos)],
            'dia_sano': [-1 for _ in range(self.num_ciudadanos)]
        })
        
        #creo un DataFrame con columnas para el id, nombre, edad, 
        #y varios estados de infección (infectado, dias_infectado, dia_infectado, dia_sano). 
        
        ciudadanos['apellido'] = [nombre.split()[-1] for nombre in ciudadanos['nombre']]

        ciudadanos['id_familiar'] = self.generar_id_familiar(ciudadanos['apellido'])
        
        return ciudadanos
    #extrae los apellidos y se generan IDs familiares para cada ciudadano
    #se devuelve el DataFrame 
    
    def generar_id_familiar(self, apellidos):
        id_familiar = []
        familias = apellidos.value_counts()
        id_actual = 1
        
        for apellido in familias.index:
            miembros_familia = apellidos[apellidos == apellido].index.tolist()
            for i in range(0, len(miembros_familia), 3):
                grupo_familiar = miembros_familia[i:i+3]
                for miembro in grupo_familiar:
                    id_familiar.append((miembro, id_actual))
                id_actual += 1
        # se itera sobre los índices de los miembros de la familia en pasos de 3
        
        id_familiar.sort()  # Ordenar para coincidir con el DataFrame original
        return [id for _, id in id_familiar]
       # se ordena la lista id_familiar 
       # para mantener el orden original del DataFrame.
    def guardar_ciudadanos_csv(self):
        self.ciudadanos.to_csv('ciudadanos.csv', index=False)
        
    def guardar_familias_csv(self):
        familias = self.ciudadanos.sort_values(by=['id_familiar', 'id'])
        familias.to_csv('familias.csv', index=False)
        
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
    #simula el dia, se seleccionan los ciudadanos infectados y se decrece su contador de dias_infectado
    #Si llega a cero, el ciudadano se marca como sano.
    
            contactos = self.ciudadanos.sample(self.promedio_conexion_fisica)
            for _, contacto in contactos.iterrows():
                if not contacto['infectado'] and not contacto['dias_infectado'] and random.random() < self.probabilidad_conexion_fisica:
                    self.ciudadanos.at[contacto.name, 'infectado'] = True
                    self.ciudadanos.at[contacto.name, 'dias_infectado'] = self.enfermedad.duracion_infeccion
                    self.ciudadanos.at[contacto.name, 'dia_infectado'] = self.dia_actual
                    nuevos_infectados += 1
      
        self.num_infectados += nuevos_infectados
        self.num_contagios += nuevos_infectados

        # Calcular el número de personas no infectadas
        num_no_infectados = self.num_ciudadanos - self.num_contagios

        print(self.ciudadanos)
        print(f"El total de contagios de la comunidad: {self.num_contagios}; casos activos: {self.num_infectados}; personas no infectadas: {num_no_infectados}.")

        # Registrar los datos en el archivo CSV
        with open('resultados.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.dia_actual, self.num_contagios, self.num_infectados, num_no_infectados])

        self.dia_actual += 1
        self.guardar_ciudadanos_csv()
        self.guardar_familias_csv()

