import matplotlib.pyplot as plt
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
        infectados_totales = []
        for paso in range(self.num_pasos):
            self.comunidad.paso()
            infectados_totales.append(self.comunidad.num_infectados)
            print(f"El total de contagios de la comunidad: {self.comunidad.num_contagios}; casos activos: {self.comunidad.num_infectados}.")
            
        # Guardar los datos de la simulación en un archivo CSV
        with open('resultados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Paso', 'Infectados'])
            for i, infectados in enumerate(infectados_totales):
                writer.writerow([i, infectados])
        
        # Guardar la figura en lugar de mostrarla
        plt.figure()
        plt.plot(infectados_totales)
        plt.xlabel('Pasos')
        plt.ylabel('Infectados')
        plt.title('Simulación de Enfermedad Infecciosa')
        plt.savefig('grafico.png')
