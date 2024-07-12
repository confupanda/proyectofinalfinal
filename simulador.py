import csv
import random
import matplotlib.pyplot as plt

class Simulador:
    def __init__(self):
        self.comunidad = None
        self.num_pasos = 0

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def set_num_pasos(self, num_pasos):
        self.num_pasos = num_pasos

    def iniciar_simulacion(self):
        infectados_por_paso = []
        for paso in range(self.num_pasos):
            nuevos_infectados = 0
            for ciudadano in self.comunidad.ciudadanos:
                if not ciudadano.estado:  # Si está infectado
                    contactos = self.obtener_contactos(ciudadano)
                    for contacto in contactos:
                        if contacto.estado and random.random() < self.comunidad.enfermedad.infeccion_probable:
                            contacto.infectar(self.comunidad.enfermedad)
                            nuevos_infectados += 1

            infectados = sum(1 for c in self.comunidad.ciudadanos if not c.estado)
            infectados_por_paso.append(infectados)
            self.guardar_estado(paso)

        self.graficar(infectados_por_paso)

    def obtener_contactos(self, ciudadano):
        contactos = []
        for _ in range(self.comunidad.promedio_conexion_fisica):
            if random.random() < self.comunidad.probabilidad_conexion_fisica:
                contacto = random.choice(self.comunidad.ciudadanos)
                if contacto.id != ciudadano.id:
                    contactos.append(contacto)
        return contactos

    def guardar_estado(self, paso):
        with open(f'estado_paso_{paso}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nombre', 'Apellido', 'Familia', 'Estado'])
            for ciudadano in self.comunidad.ciudadanos:
                writer.writerow([ciudadano.id, ciudadano.nombre, ciudadano.apellido, ciudadano.familia, 'Sano' if ciudadano.estado else 'Infectado'])

    def graficar(self, infectados_por_paso):
        plt.figure()
        plt.plot(infectados_por_paso, label='Infectados')
        plt.xlabel('Pasos')
        plt.ylabel('Número de Infectados')
        plt.title('Simulación SIR')
        plt.legend()
        plt.show()
