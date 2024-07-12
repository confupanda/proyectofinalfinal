import pandas as pd

class Simulador:
    def __init__(self):
        self.comunidad = None
        self.num_pasos = 0

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def set_num_pasos(self, num_pasos):
        self.num_pasos = num_pasos

    def iniciar_simulacion(self):
        resultados = pd.DataFrame(columns=['Día', 'Total Contagios', 'Casos Activos'])

        for paso in range(self.num_pasos):
            self.comunidad.paso()
            resultados = pd.concat([resultados, pd.DataFrame([{
                'Día': self.comunidad.dia_actual,
                'Total Contagios': self.comunidad.num_contagios,
                'Casos Activos': self.comunidad.num_infectados
            }])], ignore_index=True)
        
        resultados.to_csv('resultados.csv', index=False)


#define la clase Simulador que controla la simulación
#configura la comunidad, el número de pasos
#y ejecuta la simulación guardando los resultados en un archivo CSV.