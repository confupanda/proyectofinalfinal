import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GLib

class MyApplication(Gtk.Application):

    def _init_(self):
        super()._init_(application_id="com.example.MyApp")

    def do_activate(self):
        window = self.props.active_window
        if not window:
            window = Gtk.ApplicationWindow(application=self)
            window.set_default_size(400, 300)
            window.set_title("My Gtk4 Application")
            window.show()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(None)
exit(exit_status)