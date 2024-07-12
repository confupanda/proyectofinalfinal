import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador

class Interfaz(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.SIRSimulator")
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = Gtk.ApplicationWindow(application=self)
            self.window.set_title("Simulador de Enfermedades Infecciosas")
            self.window.set_default_size(400, 400)
            self.build_ui()
        self.window.present()

    def build_ui(self):
        # Creación de la barra de menú
        self.menu_button = Gtk.MenuButton()
        self.menu_model = Gio.Menu()
        self.menu_model.append("Acerca de", "app.about")
        self.menu_button.set_menu_model(self.menu_model)
        self.window.set_titlebar(self.menu_button)

        self.add_about_action()

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

    def add_about_action(self):
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
        sim.iniciar_simulacion()

        self.resultado.set_text("Simulación completada. Revisa los archivos CSV y el gráfico.")

app = Interfaz()
app.run(None)
