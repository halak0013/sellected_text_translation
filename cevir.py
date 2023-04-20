import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import sys
from googletrans import Translator

class MainWindow(Gtk.Window):
    def __init__(self,x,y):
        Gtk.Window.__init__(self, title="Translated Text")

        self.set_border_width(7)
        self.set_decorated(False)
        self.label = Gtk.Label()

        self.connect("key-press-event", self.on_key_press_event)

        self.add(self.label)
        self.move(x,y)

    def set_text(self, text):
        self.label.set_text(text)

    def on_key_press_event(self, widget, event):
    # when type "esc" it will close
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

lang="tr"
if len(sys.argv) > 1:
    translator = Translator()
    x=int(sys.argv[2])
    y=int(sys.argv[3])
    window = MainWindow(x,y)
    window.connect("delete-event", Gtk.main_quit)
    selected_text = sys.argv[1]
    translation = translator.translate(selected_text, dest=lang).text
    window.set_text(translation)

    window.show_all()
    Gtk.main()