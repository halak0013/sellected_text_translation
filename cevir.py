import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import sys
from googletrans import Translator
import json

class MainWindow(Gtk.Window):
    def __init__(self,x,y,selected_text):
        Gtk.Window.__init__(self)

        self.set_border_width(7)
        self.set_decorated(False)
        self.set_keep_above(True)
        
        self.label = Gtk.Label()
        self.input_text=Gtk.Entry()
        self.cmb_lang=Gtk.ComboBoxText()
        self.btn_copy=Gtk.Button(label="🗒")
        self.selected_text=selected_text
        self.connect("key-press-event", self.on_key_press_event)
        
        self.widget_pro()
        self.translate()
        

    def widget_pro(self):
        input_box=Gtk.HBox()
        main_box=Gtk.VBox()
        
        lang_lst=[
            "tr 🇹🇷",
            "en 🇬🇧",
            "ar 🇵🇸",
            "de 🇩🇪",
            "es 🇪🇸",
            "ru 🇷🇺"
        ]
        self.input_text.set_text(self.selected_text)
        for l in lang_lst:
            self.cmb_lang.append_text(l)
        self.cmb_lang.set_active(0)
        
        self.btn_copy.connect("clicked", self.copy_text)
        self.label.set_selectable(True)
        
        input_box.add(self.input_text)
        input_box.add(self.btn_copy)
        input_box.add(self.cmb_lang)
        
        main_box.add(input_box)
        main_box.add(self.label)
        
        self.add(main_box)
        self.move(x,y)
        
    def set_text(self, text):
        self.label.set_text(text)
        
    def translate(self):
        lang = self.cmb_lang.get_active_text().split()[0]
        s_text = self.input_text.get_text()
        if s_text is not None and s_text != "":
            try:
                translation = translator.translate(s_text, dest=lang).text
                if translation is not None:
                    self.label.set_text(self.text_configure(translation, 7))
                else:
                    self.label.set_text("Translation not available.")
            except Exception as e:
                print("Translation error:", e)
                self.label.set_text("Translation error occurred.")
        else:
            self.label.set_text("No text to translate.")

    def text_configure(self,txt,k):
        txt=txt.split()
        result=""
        for i,t in enumerate(txt):
            print(i%k)
            if i%k==0:
                result+="\n"
            result+=t+" "
        return result

    def copy_text(self,widegt):
        print("kopyla")
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.label.get_text(), -1)

    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
        if event.keyval == Gdk.KEY_Return or event.keyval == Gdk.KEY_KP_Enter:
            self.translate()
            print("çevir")

if len(sys.argv) > 1:
    translator = Translator()
    x=int(sys.argv[2])
    y=int(sys.argv[3])
    selected_text = sys.argv[1]
    
    window = MainWindow(x,y,selected_text)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()