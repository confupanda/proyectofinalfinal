# modelo_sir.py

class ModeloSIR:
    def __init__(self, poblacion, infectados_iniciales, recuperados_iniciales, beta, gamma):
        self.poblacion = poblacion
        self.susceptibles = poblacion - infectados_iniciales - recuperados_iniciales
        self.infectados = infectados_iniciales
        self.recuperados = recuperados_iniciales
        self.beta = beta
        self.gamma = gamma
        self.resultados = []

    def paso(self):
        nuevos_infectados = (self.beta * self.susceptibles * self.infectados) / self.poblacion
        nuevos_recuperados = self.gamma * self.infectados

        self.susceptibles -= nuevos_infectados
        self.infectados += nuevos_infectados - nuevos_recuperados
        self.recuperados += nuevos_recuperados

        self.resultados.append((self.susceptibles, self.infectados, self.recuperados))

    def obtener_resultados(self):
        return self.resultados
