import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty


class Menu(BoxLayout):
    Builder.load_file('../views/menu.kv')
    current_state=StringProperty('Open')
    
    def on_state(self, togglebutton):
        if togglebutton.state=='down':
            self.current_state=togglebutton.text
