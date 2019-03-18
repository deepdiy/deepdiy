import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty

import utils.file_dialog
from views.open_panel import OpenPanel

from kivy.uix.button import Button


class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        from kivy.lang import Builder
        Builder.load_file('openpanel.kv')
        self.ids.options_panel.add_widget(OpenPanel())
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'


class ControllerApp(App):

    def build(self):
        self.root=Controller(info='Hello world')
        return self.root
    def help(self):
        print(self.root.ids)

if __name__ == '__main__':
    ControllerApp().run()
