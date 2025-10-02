#!/usr/bin/env python3
import gi
import os
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, Gio

class InledApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='es.inled.app')
        
    def do_activate(self):
        win = InledWindow(application=self)
        win.present()

class InledWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de ventana
        self.set_default_size(700, 450)
        self.set_title("Inled Group")
        
        # Variable para el toast
        self.toast_revealer = None
        
        # CSS con múltiples animaciones ligeras
        css = b"""
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(-10px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .hero-box {
            background: #ffffff;
            border: 2px solid #e5e7eb;
            border-radius: 20px;
            padding: 48px;
            margin: 32px;
            transition: all 250ms ease-out;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .hero-box:hover {
            transform: translateY(-6px) scale(1.01);
            border-color: #39b6ff;
            box-shadow: 0 20px 40px rgba(57, 182, 255, 0.15);
        }
        
        .hero-title {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 16px;
            animation: fadeInUp 600ms ease-out;
            transition: color 200ms ease;
        }
        
        .hero-box:hover .hero-title {
            color: #39b6ff;
        }
        
        .hero-subtitle {
            font-size: 16px;
            color: #6b7280;
            font-weight: 400;
            animation: fadeInUp 600ms ease-out 200ms backwards;
        }
        
        .logo-container {
            padding: 24px;
            background: #ffffff;
            border-bottom: 1px solid #f3f4f6;
            animation: slideIn 400ms ease-out;
            transition: background 200ms ease;
        }
        
        .logo-container:hover {
            background: #f9fafb;
        }
        
        .logo-image {
            transition: all 300ms ease-out;
            opacity: 0.95;
        }
        
        .logo-image:hover {
            transform: scale(1.05) rotate(1deg);
            opacity: 1;
        }
        
        .email-link {
            color: #39b6ff;
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: all 200ms ease;
            padding: 4px 8px;
            border-radius: 6px;
            background: transparent;
        }
        
        .email-link:hover {
            background: #e6f7ff;
            border-bottom-color: #39b6ff;
            transform: translateY(-1px);
        }
        
        .email-link:active {
            transform: scale(0.98);
        }
        
        .icon-box {
            transition: transform 300ms ease-out;
        }
        
        .icon-box:hover {
            transform: rotate(360deg);
        }
        
        .support-badge {
            background: #f0fdf4;
            border: 1px solid #86efac;
            color: #16a34a;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-top: 16px;
            transition: all 200ms ease;
            animation: fadeInUp 600ms ease-out 400ms backwards;
        }
        
        .support-badge:hover {
            background: #dcfce7;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
        }
        
        .toast-notification {
            background: #39b6ff;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(57, 182, 255, 0.3);
            animation: slideInDown 300ms ease-out;
            margin: 16px;
        }
        
        @keyframes slideInDown {
            from {
                transform: translateY(-20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        window {
            background: #f9fafb;
        }
        """
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Contenedor principal con overlay para notificaciones
        overlay = Gtk.Overlay()
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Revealer para el toast (notificación)
        self.toast_revealer = Gtk.Revealer()
        self.toast_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.toast_revealer.set_transition_duration(300)
        self.toast_revealer.set_valign(Gtk.Align.START)
        self.toast_revealer.set_halign(Gtk.Align.CENTER)
        
        self.toast_label = Gtk.Label(label="")
        self.toast_label.add_css_class('toast-notification')
        self.toast_revealer.set_child(self.toast_label)
        
        # Header con logo
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_halign(Gtk.Align.CENTER)
        header_box.add_css_class('logo-container')
        
        # Cargar logo usando GFile (método moderno)
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inled.png')
        
        if os.path.exists(logo_path):
            try:
                logo_file = Gio.File.new_for_path(logo_path)
                logo = Gtk.Picture.new_for_file(logo_file)
                logo.set_can_shrink(True)
                logo.set_content_fit(Gtk.ContentFit.CONTAIN)
                logo.set_size_request(200, 80)
                logo.add_css_class('logo-image')
                
                # Añadir hover effect al logo
                logo_motion = Gtk.EventControllerMotion.new()
                logo.add_controller(logo_motion)
                
                header_box.append(logo)
            except Exception as e:
                print(f"Error cargando logo: {e}")
                fallback = Gtk.Label(label="🚀 INLED")
                fallback.add_css_class('hero-title')
                header_box.append(fallback)
        else:
            fallback = Gtk.Label(label="🚀 INLED")
            fallback.add_css_class('hero-title')
            header_box.append(fallback)
        
        main_box.append(header_box)
        
        # Hero section
        hero_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        hero_box.set_valign(Gtk.Align.CENTER)
        hero_box.set_halign(Gtk.Align.FILL)
        hero_box.add_css_class('hero-box')
        
        # Icono decorativo con animación
        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        icon_box.set_halign(Gtk.Align.CENTER)
        icon_box.add_css_class('icon-box')
        icon_label = Gtk.Label(label="⚡")
        icon_label.set_css_classes(['hero-title'])
        icon_box.append(icon_label)
        hero_box.append(icon_box)
        
        # Título
        title = Gtk.Label(label="Mantenido por Inled Group")
        title.add_css_class('hero-title')
        title.set_wrap(True)
        title.set_justify(Gtk.Justification.CENTER)
        hero_box.append(title)
        
        # Subtítulo con email
        subtitle_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        subtitle_box.set_halign(Gtk.Align.CENTER)
        
        help_label = Gtk.Label(label="Ayuda: ")
        help_label.add_css_class('hero-subtitle')
        subtitle_box.append(help_label)
        
        email_label = Gtk.Label(label="contacto@inled.es")
        email_label.add_css_class('hero-subtitle')
        email_label.add_css_class('email-link')
        
        # Email clickeable
        email_gesture = Gtk.GestureClick.new()
        email_gesture.connect('released', self.on_email_clicked)
        email_label.add_controller(email_gesture)
        
        # Cursor pointer
        email_motion = Gtk.EventControllerMotion.new()
        email_motion.connect('enter', self.on_email_enter)
        email_motion.connect('leave', self.on_email_leave)
        email_label.add_controller(email_motion)
        
        subtitle_box.append(email_label)
        hero_box.append(subtitle_box)
        
        # Badge de soporte
        badge = Gtk.Label(label="✓ Soporte activo")
        badge.add_css_class('support-badge')
        badge.set_halign(Gtk.Align.CENTER)
        hero_box.append(badge)
        
        # Badge hover effect
        badge_motion = Gtk.EventControllerMotion.new()
        badge.add_controller(badge_motion)
        
        # Contenedor para centrar el hero
        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        center_box.set_vexpand(True)
        center_box.set_valign(Gtk.Align.CENTER)
        center_box.append(hero_box)
        
        main_box.append(center_box)
        
        # Configurar overlay
        overlay.set_child(main_box)
        overlay.add_overlay(self.toast_revealer)
        
        self.set_content(overlay)
    
    def on_email_clicked(self, gesture, n_press, x, y):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set("contacto@inled.es")
        self.show_toast("✓ Email copiado al portapapeles")
    
    def show_toast(self, message):
        """Muestra una notificación temporal"""
        from gi.repository import GLib
        
        self.toast_label.set_label(message)
        self.toast_revealer.set_reveal_child(True)
        
        # Ocultar después de 2.5 segundos
        GLib.timeout_add(2500, self.hide_toast)
    
    def hide_toast(self):
        """Oculta la notificación"""
        self.toast_revealer.set_reveal_child(False)
        return False
    
    def on_email_enter(self, controller, x, y):
        self.set_cursor(Gdk.Cursor.new_from_name("pointer"))
    
    def on_email_leave(self, controller):
        self.set_cursor(None)

def main():
    app = InledApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    main()