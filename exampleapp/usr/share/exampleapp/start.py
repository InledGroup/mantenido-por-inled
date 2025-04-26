#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Example App")
        self.set_default_size(300, 150)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Crear una etiqueta con el texto deseado
        self.label = Gtk.Label()
        self.label.set_markup("<span size='large'><b>Installed correctly</b></span>")
        
        # Crear un contenedor para centrar la etiqueta
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_homogeneous(False)
        self.box.pack_start(self.label, True, True, 0)
        
        self.add(self.box)
        self.connect("destroy", Gtk.main_quit)

# Iniciar la aplicación
ventana = VentanaPrincipal()
ventana.show_all()
Gtk.main()