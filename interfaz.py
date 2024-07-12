import gi
import threading
import csv
import pandas as pd
import matplotlib.pyplot as plt
from gi.repository import Gtk, Gio, GLib
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas

gi.require_version('Gtk', '4.0')

from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador

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

        self.label_pasos = Gtk.Label(label="Número de dias:")
        vbox.append(self.label_pasos)

        self.entrada_pasos = Gtk.Entry()
        self.entrada_pasos.set_placeholder_text("Número de dias")
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
            self.resultado.set_text("Por favor ingrese valores válidos.")
            return

        num_ciudadanos = int(num_ciudadanos)
        num_infectados = int(num_infectados)
        num_pasos = int(num_pasos)

        if num_ciudadanos < 1 or num_infectados < 1 or num_pasos < 1:
            self.resultado.set_text("Todos los valores deben ser mayores que 0.")
            return

        enfermedad = Enfermedad(infeccion_probable=0.3, duracion_infeccion=7)
        comunidad = Comunidad(num_ciudadanos, 10, enfermedad, num_infectados, 0.05)
        simulador = Simulador()
        simulador.set_comunidad(comunidad)
        simulador.set_num_pasos(num_pasos)

        self.resultado.set_text("Simulación en curso...")

        thread = threading.Thread(target=self.run_simulation, args=(simulador,))
        thread.start()

    def run_simulation(self, simulador):
        simulador.iniciar_simulacion()
        GLib.idle_add(self.update_results)

    def update_results(self):
        self.resultado.set_text("Simulación completada.")
        self.show_graph()

    def show_graph(self):
        df = pd.read_csv('resultados.csv')

        # Contar las personas que jamás se infectaron
        ciudadanos = pd.read_csv('ciudadanos.csv')
        nunca_infectados = ciudadanos[ciudadanos['dia_infectado'] == -1].shape[0]
        
        # Contar las personas recuperadas
        recuperados = ciudadanos[(ciudadanos['dia_infectado'] != -1) & (ciudadanos['dias_infectado'] == -1)].shape[0]

        figure = Figure(figsize=(8, 6))
        ax = figure.add_subplot(111)

        ax.plot(df['Día'], df['Casos Activos'], label="Casos Activos", color='blue')
        ax.plot(df['Día'], df['Total Contagios'], label="Total Contagios", color='red')

        # Añadir la línea para las personas que jamás se infectaron
        ax.axhline(y=nunca_infectados, color='green', linestyle='--', label="Jamás Infectados")

        # Añadir la línea para las personas recuperadas
        ax.axhline(y=recuperados, color='purple', linestyle='-.', label="Recuperados")

        ax.set_title("Simulación de Infectados")
        ax.set_xlabel("Días")
        ax.set_ylabel("Número de Casos")
        ax.legend()

        figure.savefig("grafico_simulacion.png")

        canvas = FigureCanvas(figure)
        canvas.set_size_request(800, 600)

        window = Gtk.Window()
        window.set_title("Gráfico de la Simulación")
        window.set_default_size(800, 600)
        window.set_child(canvas)
        window.present()

