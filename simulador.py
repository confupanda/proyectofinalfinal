import csv
import matplotlib.pyplot as plt
from comunidad import Comunidad

class Simulador:
    def __init__(self):
        self.comunidad = None
        self.num_pasos = 0

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def set_num_pasos(self, num_pasos):
        self.num_pasos = num_pasos

    def iniciar_simulacion(self):
        with open('resultados.csv', 'w', newline='') as csvfile:
            fieldnames = ['Dias', 'Nombre', 'Edad', 'Infectado']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for paso in range(self.num_pasos):
                self.comunidad.paso()

                for persona in self.comunidad.personas:
                    writer.writerow({
                        'Dias': paso+1,
                        'Nombre': f"{persona.nombre}",
                        'Edad': persona.edad,
                        'Infectado': persona.infectado
                    })

                total_infectados = self.comunidad.obtener_total_infectados()
                print(f"Dias {paso+1}: Total de infectados = {total_infectados}")

                if total_infectados >= len(self.comunidad.personas):
                    break