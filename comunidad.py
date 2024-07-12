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
        
    def generar_ciudadanos(self):
        try:
            with open('nombres_apellidos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                nombres = data['nombres']
                apellidos = data['apellidos']
        except FileNotFoundError:
            print("El archivo 'nombres_apellidos.json' no se encuentra en el directorio.")
            return pd.DataFrame()
        
        # Crear ciudadanos con nombres y apellidos aleatorios
        ciudadanos = pd.DataFrame({
            'id': range(1, self.num_ciudadanos + 1),
            'nombre': [random.choice(nombres) + " " + random.choice(apellidos) for _ in range(self.num_ciudadanos)],
            'edad': np.random.randint(1, 101, self.num_ciudadanos),
            'infectado': [i < self.num_infectados for i in range(self.num_ciudadanos)],
            'dias_infectado': [self.enfermedad.duracion_infeccion if i < self.num_infectados else 0 for i in range(self.num_ciudadanos)],
            'dia_infectado': [0 if i < self.num_infectados else -1 for i in range(self.num_ciudadanos)],
            'dia_sano': [-1 for _ in range(self.num_ciudadanos)]
        })
        
        # Extraer apellidos y asignar ID familiar
        ciudadanos['apellido'] = ciudadanos['nombre'].apply(lambda x: x.split()[-1])
        ciudadanos['id_familiar'] = self.generar_id_familiar(ciudadanos['apellido'])
        
        return ciudadanos

    def generar_id_familiar(self, apellidos):
        id_familiar = []
        familias = apellidos.value_counts()
        id_actual = 1
        
        for apellido in familias.index:
            miembros_familia = apellidos[apellidos == apellido].index.tolist()
            for miembro in miembros_familia:
                id_familiar.append((miembro, id_actual))
            id_actual += 1
        
        id_familiar.sort()  # Ordenar para coincidir con el DataFrame original
        return [id for _, id in id_familiar]
        
    def guardar_ciudadanos_csv(self):
        self.ciudadanos.to_csv('ciudadanos.csv', index=False)
        
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
    
            contactos = self.ciudadanos.sample(self.promedio_conexion_fisica)
            for _, contacto in contactos.iterrows():
                if not contacto['infectado'] and not contacto['dias_infectado'] and random.random() < self.probabilidad_conexion_fisica:
                    self.ciudadanos.at[contacto.name, 'infectado'] = True
                    self.ciudadanos.at[contacto.name, 'dias_infectado'] = self.enfermedad.duracion_infeccion
                    self.ciudadanos.at[contacto.name, 'dia_infectado'] = self.dia_actual
                    nuevos_infectados += 1
      
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
