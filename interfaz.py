import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
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
            self.window.set_default_size(400, 300)
            self.build_ui()
        self.window.present()

    def build_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        self.window.set_child(vbox)

        self.entrada_ciudadanos = Gtk.Entry()
        self.entrada_ciudadanos.set_placeholder_text("Número de ciudadanos")
        vbox.append(self.entrada_ciudadanos)

        self.entrada_infectados = Gtk.Entry()
        self.entrada_infectados.set_placeholder_text("Número inicial de infectados")
        vbox.append(self.entrada_infectados)

        self.entrada_pasos = Gtk.Entry()
        self.entrada_pasos.set_placeholder_text("Número de pasos")
        vbox.append(self.entrada_pasos)

        self.boton_iniciar = Gtk.Button(label="Iniciar Simulación")
        self.boton_iniciar.connect("clicked", self.on_start_button_clicked)
        vbox.append(self.boton_iniciar)

    def on_start_button_clicked(self, button):
        num_ciudadanos = int(self.entrada_ciudadanos.get_text())
        num_infectados = int(self.entrada_infectados.get_text())
        num_pasos = int(self.entrada_pasos.get_text())

        covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)
        comunidad = Comunidad(num_ciudadanos=num_ciudadanos, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=num_infectados, probabilidad_conexion_fisica=0.8)
        simulador = Simulador()
        simulador.set_comunidad(comunidad)
        simulador.set_num_pasos(num_pasos)
        simulador.iniciar_simulacion()
