import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from controllers.config_panel import ConfigPanel
from controllers.resource_tree import ResourceTree
from controllers.menu import Menu

from kivy.event import EventDispatcher


class Frame(BoxLayout):
    pass



Builder.load_file('../views/frame.kv')
Builder.load_file('../views/menu.kv')



class MainWindow(App):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resource_tree=ResourceTree({'node_id': 'img','children': []})

    def build(self):
        frame=Frame()
        frame.ids.source_tree.add_widget(self.resource_tree)
        frame.ids.menu.bind(current_state=frame.ids.config_panel.setter('page'))
        frame.ids.config_panel.ids.select_path_panel.bind(tree=self.resource_tree.setter('data'))
        return frame


if __name__ == '__main__':
    MainWindow().run()
