import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')
from kivy.lang import Builder

import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from utils.select_path_dialog import select_file,select_folder
from utils.path2tree import *

class SelectPathPanel(BoxLayout):
    file_path=StringProperty('')
    folder_path=StringProperty('')
    tree=DictProperty()
    id='select_path_panel'

    # def __init__(self):
    #     super(SelectPathPanel, self).__init__()
        # self.register_event_type('on_select_file')
        # self.register_event_type('on_select_folder')

    def open_file(self):
        self.file_path=select_file()
        self.tree=path2tree(self.file_path)
        # self.dispatch('on_select_file', 'test message')
        print(self.file_path)

    def open_folder(self):
        self.folder_path=select_folder()
        self.tree=path2tree(self.folder_path)
        # self.dispatch('on_select_folder', 'test message')
        print(self.folder_path)

    # def on_open_file(self, *args):
    #     pass
    #
    # def on_open_folder(self, *args):
    #     pass


class OpenPanelApp(App):
    def build(self):
        return SelectPathPanel()

if __name__ == '__main__':
    Builder.load_file('../views/select_path_panel.kv')
    OpenPanelApp().run()
