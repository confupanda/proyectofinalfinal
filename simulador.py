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
            fieldnames = ['Paso', 'Total Infectados']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            infectados_totales = []

            for paso in range(self.num_pasos):
                self.comunidad.paso()
                total_infectados = self.comunidad.obtener_total_infectados()
                infectados_totales.append(total_infectados)
                
                writer.writerow({'Paso': paso+1, 'Total Infectados': total_infectados})
                print(f"Paso {paso+1}: Total de infectados = {total_infectados}")
                
                if total_infectados >= len(self.comunidad.personas):
                    break
            
            self.guardar_grafico(infectados_totales)

    def guardar_grafico(self, infectados_totales):
        plt.plot(range(1, len(infectados_totales) + 1), infectados_totales, label='Total Infectados')
        plt.xlabel('Pasos')
        plt.ylabel('Número de Infectados')
        plt.legend()
        plt.savefig('grafico.png')
        plt.show()