class Simulador:
    def __init__(self, comunidad, modelo_sir, dias):
        self.comunidad = comunidad
        self.modelo_sir = modelo_sir
        self.dias = dias

    def simular(self):
        for _ in range(self.dias):
            self.comunidad.paso()
            self.modelo_sir.simular_paso()

    def simular_paso(self):
        self.comunidad.paso()
        self.modelo_sir.simular_paso()


#define la clase Simulador que controla la simulación
#configura la comunidad, el número de dias
#y ejecuta la simulación guardando los resultados en un archivo CSV.
