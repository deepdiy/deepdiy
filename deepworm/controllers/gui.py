import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from controllers.select_path_panel import SelectPathPanel
from controllers.resource_tree import ResourceTree
from utils.path2tree import *
from kivy.event import EventDispatcher


class Frame(BoxLayout):
    pass

class Menu(BoxLayout):
    pass

Builder.load_file('../views/frame.kv')
Builder.load_file('../views/menu.kv')
Builder.load_file('../views/select_path_panel.kv')


class MainWindow(App):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resource_tree=ResourceTree({'node_id': 'img','children': []})

    def update_resource_tree(self,state,value):
        self.resource_tree.data=path2tree(value)

    def update_option_panel(self):
        pass


    def build(self):
        frame=Frame()
        frame.ids.source_tree.add_widget(self.resource_tree)

        select_path_panel=SelectPathPanel()
        frame.ids.options.add_widget(select_path_panel)
        select_path_panel.bind(file_path=self.update_resource_tree)
        select_path_panel.bind(folder_path=self.update_resource_tree)
        return frame


if __name__ == '__main__':
    MainWindow().run()
