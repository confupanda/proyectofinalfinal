import csv
import matplotlib.pyplot as plt
import random

class Simulador:
    def __init__(self):
        self.comunidad = None
        self.num_pasos = 0

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def set_num_pasos(self, num_pasos):
        self.num_pasos = num_pasos

    def iniciar_simulacion(self):
        if not self.comunidad or self.num_pasos <= 0:
            return

        infectados_totales = []
        casos_activos = []

        for paso in range(self.num_pasos):
            nuevos_infectados = self.simular_paso()
            infectados_totales.append(len(nuevos_infectados))
            casos_activos.append(len(nuevos_infectados))

            # Imprimir estado en la terminal
            print(f"El total de contagios de la comunidad: {len(nuevos_infectados)}; casos activos: {len(nuevos_infectados)}.")

            # Detener la simulación si los casos activos son 0
            if len(nuevos_infectados) == 0:
                break

            self.guardar_estado(paso, nuevos_infectados)

        self.graficar_infectados(infectados_totales)

    def simular_paso(self):
        nuevos_infectados = []
        for ciudadano in self.comunidad.ciudadanos:
            if not ciudadano.estado and ciudadano.enfermedad and ciudadano.enfermedad.contador > 0:
                if random.random() < ciudadano.enfermedad.infeccion_probable:
                    nuevos_infectados.append(ciudadano)
                ciudadano.enfermedad.contador -= 1
                if ciudadano.enfermedad.contador <= 0:
                    ciudadano.estado = True
        return nuevos_infectados

    def guardar_estado(self, paso, nuevos_infectados):
        with open('estado_simulacion.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([paso, len(nuevos_infectados)])

    def graficar_infectados(self, infectados_totales):
        plt.plot(infectados_totales)
        plt.xlabel('Pasos')
        plt.ylabel('Número de Infectados')
        plt.title('Simulación de Enfermedades Infecciosas')
        plt.savefig('grafico_infectados.png')
        plt.show()
