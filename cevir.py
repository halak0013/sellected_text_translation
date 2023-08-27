import json
import gi
import requests
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import sys
from urllib.parse import quote
class MainWindow(Gtk.Window):
    def __init__(self,x,y,selected_text):
        Gtk.Window.__init__(self)

        self.set_border_width(7)
        self.set_decorated(False)
        self.set_keep_above(True)
        
        self.label = Gtk.Label()
        self.input_text=Gtk.Entry()
        self.cmb_lang_o=Gtk.ComboBoxText()
        self.cmb_lang_i=Gtk.ComboBoxText()
        self.btn_copy=Gtk.Button(label="🗒")
        self.selected_text=selected_text
        self.connect("key-press-event", self.on_key_press_event)
        
        self.widget_pro()
        self.translate()
        
    def combo_process(self):
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
            self.cmb_lang_o.append_text(l)
        self.cmb_lang_o.set_active(0)
        
        lang_lst.insert(0,"Autodetect 🤖")
        for l in lang_lst:
            self.cmb_lang_i.append_text(l)
        self.cmb_lang_i.set_active(0)
        
        self.cmb_lang_i.connect("changed",self.lang_changed)
        self.cmb_lang_o.connect("changed",self.lang_changed)


    def widget_pro(self):
        input_box=Gtk.HBox()
        main_box=Gtk.VBox()
        self.combo_process()
        
        self.btn_copy.connect("clicked", self.copy_text)
        self.label.set_selectable(True)
        
        input_box.add(self.input_text)
        input_box.add(self.btn_copy)
        input_box.add(self.cmb_lang_i)
        input_box.add(self.cmb_lang_o)
        
        main_box.add(input_box)
        main_box.add(self.label)
        
        self.add(main_box)
        self.move(x,y)
        
    def lang_changed(self,cmb):
        self.translate()

    def translate(self):
        lang_o = self.cmb_lang_o.get_active_text().split()[0]
        lang_i = self.cmb_lang_i.get_active_text().split()[0]
        text = quote(self.input_text.get_text())
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={lang_i}&tl={lang_o}&dt=t&q={text}"
        result = ""
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open("/tmp/translate/t.txt", "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            with open("/tmp/translate/t.txt", "r") as f:
                tr = f.readline()
                print(tr)
                for d in json.loads(tr)[0]:
                    while not type(d) == str:
                        d = d[0]
                    result += d
            self.label.set_text(self.text_configure(result, 7))
        except requests.exceptions.RequestException as e:
            print(f"File download error: {e}")
            self.label.set_text("null")

    def text_configure(self,txt,k):
        txt=txt.split()
        result=""
        for i,t in enumerate(txt):
            if i%k==0 and i != 0:
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
    x=int(sys.argv[2])
    y=int(sys.argv[3])
    selected_text = sys.argv[1]
    
    window = MainWindow(x,y,selected_text)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()