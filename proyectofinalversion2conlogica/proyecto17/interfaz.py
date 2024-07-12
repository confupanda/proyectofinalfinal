import random

class Enfermedad:
    def __init__(self, infeccion_probable, duracion_infeccion):
        self.infeccion_probable = infeccion_probable
        self.duracion_infeccion = duracion_infeccion

    def es_infeccioso(self):
        return random.random() < self.infeccion_probable

# interfaz.py

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
from modelo_sir import ModeloSIR  

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
        num_ciudadanos = int(self.entrada_ciudadanos.get_text())
        num_infectados = int(self.entrada_infectados.get_text())
        dias = int(self.entrada_pasos.get_text())
        
        # Definimos la enfermedad
        enfermedad = Enfermedad(infeccion_probable=0.2, duracion_infeccion=14)

        # Crear comunidad
        self.comunidad = Comunidad(num_ciudadanos, promedio_conexion_fisica=5, enfermedad=enfermedad, num_infectados=num_infectados, probabilidad_conexion_fisica=0.3)

        # Crear modelo SIR
        self.modelo_sir = ModeloSIR(num_ciudadanos, 0.1, 0.05)

        self.simulador = Simulador(self.comunidad, self.modelo_sir, dias)

        self.simulacion_thread = threading.Thread(target=self.simulador.simular)
        self.simulacion_thread.start()