import csv

class Simulador:
    def __init__(self):
        self.comunidad = None
        self.num_pasos = 0

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def set_num_pasos(self, num_pasos):
        self.num_pasos = num_pasos

    def iniciar_simulacion(self):
        with open('resultados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Pasos', 'Infectados'])

        for _ in range(self.num_pasos):
            self.comunidad.paso()
