import os
import gi
import threading
import csv
import json
import matplotlib.pyplot as plt
from gi.repository import Gtk, Gio, GLib

from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas

gi.require_version('Gtk', '4.0')

class Interfaz(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.SIRSimulator", flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.add_actions()

    def do_activate(self):
        if not self.window:
            self.window = Gtk.ApplicationWindow(application=self)
            self.window.set_default_size(400, 400)
            self.build_ui()
        self.window.present()

    def build_ui(self):
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_title_buttons(True)
        header_bar.set_title_widget(Gtk.Label(label="Simulador de Enfermedades Infecciosas"))
        self.window.set_titlebar(header_bar)

        self.menu_button = Gtk.MenuButton()
        self.menu_model = Gio.Menu()
        self.menu_model.append("Acerca de", "app.about")
        self.menu_button.set_menu_model(self.menu_model)
        header_bar.pack_end(self.menu_button)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        self.window.set_child(vbox)

        self.label_ciudadanos = Gtk.Label(label="Número de ciudadanos:")
        vbox.append(self.label_ciudadanos)

        self.entrada_ciudadanos = Gtk.Entry()
        self.entrada_ciudadanos.set_placeholder_text("Número de ciudadanos")
        vbox.append(self.entrada_ciudadanos)

        self.label_infectados = Gtk.Label(label="Número inicial de infectados:")
        vbox.append(self.label_infectados)

        self.entrada_infectados = Gtk.Entry()
        self.entrada_infectados.set_placeholder_text("Número inicial de infectados")
        vbox.append(self.entrada_infectados)

        self.label_pasos = Gtk.Label(label="Número de pasos:")
        vbox.append(self.label_pasos)

        self.entrada_pasos = Gtk.Entry()
        self.entrada_pasos.set_placeholder_text("Número de pasos")
        vbox.append(self.entrada_pasos)

        self.boton_iniciar = Gtk.Button(label="Iniciar Simulación")
        self.boton_iniciar.connect("clicked", self.on_start_button_clicked)
        vbox.append(self.boton_iniciar)

        self.resultado = Gtk.Label()
        vbox.append(self.resultado)

    def add_actions(self):
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.show_about_dialog)
        self.add_action(about_action)

    def show_about_dialog(self, action, param):
        about_dialog = Gtk.AboutDialog(
            transient_for=self.window,
            modal=True,
            program_name="Simulador de Enfermedades Infecciosas",
            version="1.0 BETA",
            authors=["Cristian Morales"]
        )
        about_dialog.present()

    def on_start_button_clicked(self, button):
        num_ciudadanos = self.entrada_ciudadanos.get_text()
        num_infectados = self.entrada_infectados.get_text()
        num_pasos = self.entrada_pasos.get_text()

        if not num_ciudadanos.isdigit() or not num_infectados.isdigit() or not num_pasos.isdigit():
            self.resultado.set_text("Por favor, ingrese valores válidos.")
            return

        num_ciudadanos = int(num_ciudadanos)
        num_infectados = int(num_infectados)
        num_pasos = int(num_pasos)

        if num_ciudadanos <= 0 or num_infectados < 0 or num_infectados > num_ciudadanos or num_pasos <= 0:
            self.resultado.set_text("Ingrese valores coherentes.")
            return

        covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)
        comunidad = Comunidad(num_ciudadanos=num_ciudadanos, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=num_infectados, probabilidad_conexion_fisica=0.8)
        sim = Simulador()
        sim.set_comunidad(comunidad)
        sim.set_num_pasos(num_pasos)

        # Ejecutar la simulación en un hilo separado
        thread = threading.Thread(target=self.run_simulation, args=(sim,))
        thread.start()

    def run_simulation(self, sim):
        sim.iniciar_simulacion()
        GLib.idle_add(self.on_simulation_complete)

    def on_simulation_complete(self):
        self.resultado.set_text("Simulación completada. Revisa los archivos CSV y el gráfico.")
        self.mostrar_grafico()
        return False  # Para detener la función en el bucle de eventos

    def mostrar_grafico(self):
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        with open('resultados.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            pasos = []
            infectados = []
            for row in reader:
                pasos.append(int(row[0]))
                infectados.append(int(row[1]))
        ax.plot(pasos, infectados)
        ax.set_xlabel('Pasos')
        ax.set_ylabel('Infectados')
        ax.set_title('Simulación de Enfermedad Infecciosa')

        canvas = FigureCanvas(figure)  # a Gtk.DrawingArea
        self.window.set_child(canvas)

if __name__ == "__main__":
    app = Interfaz()
    app.run(None)
