import pandas as pd

class Simulador:
    def __init__(self, beta, gamma, N):
        self.comunidad = None
        self.num_pasos = 0
        self.beta = beta
        self.gamma = gamma
        self.N = N
        self.susceptibles = N
        self.infectados = 0
        self.recuperados = 0

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad
        self.infectados = comunidad.num_infectados
        self.susceptibles = self.N - self.infectados

    def set_num_pasos(self, num_pasos):
        self.num_pasos = num_pasos

    def iniciar_simulacion(self):
        resultados = pd.DataFrame(columns=['Día', 'Susceptibles', 'Infectados', 'Recuperados'])

        for paso in range(self.num_pasos):
            self.comunidad.paso()
            nuevos_susceptibles = self.susceptibles - (self.beta * self.susceptibles * self.infectados) / self.N
            nuevos_infectados = self.infectados + (self.beta * self.susceptibles * self.infectados) / self.N - self.gamma * self.infectados
            nuevos_recuperados = self.recuperados + self.gamma * self.infectados

            self.susceptibles = max(nuevos_susceptibles, 0)
            self.infectados = max(nuevos_infectados, 0)
            self.recuperados = max(nuevos_recuperados, 0)

            resultados = pd.concat([resultados, pd.DataFrame([{
                'Día': paso,
                'Susceptibles': self.susceptibles,
                'Infectados': self.infectados,
                'Recuperados': self.recuperados
            }])], ignore_index=True)

        resultados.to_csv('resultados_sir.csv', index=False)
