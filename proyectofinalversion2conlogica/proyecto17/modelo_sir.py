from interfaz import Interfaz

import numpy as np

class ModeloSIR:
    def __init__(self, poblacion, beta, gamma):
        self.poblacion = poblacion
        self.susceptibles = poblacion - 1
        self.infectados = 1
        self.recuperados = 0
        self.beta = beta
        self.gamma = gamma

    def simular_paso(self):
        nuevos_infectados = (self.beta * self.susceptibles * self.infectados) / self.poblacion
        nuevos_recuperados = self.gamma * self.infectados

        self.susceptibles -= nuevos_infectados
        self.infectados += nuevos_infectados - nuevos_recuperados
        self.recuperados += nuevos_recuperados

        print(f"S: {self.susceptibles}, I: {self.infectados}, R: {self.recuperados}")

if __name__ == "__main__":
    app = Interfaz()
    app.run(None)
