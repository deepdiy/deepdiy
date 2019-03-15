import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.app import App
from kivy.lang import Builder

from controllers.frame import Frame
from controllers.menu import Menu
from controllers.resource_tree import ResourceTree
from controllers.config_panel import ConfigPanel


Builder.load_file('../views/frame.kv')
Builder.load_file('../views/menu.kv')


class MainWindow(App):
    def build(self):
        frame=Frame()
        frame.ids.menu.bind(current_state=frame.ids.config_panel.setter('page'))
        frame.ids.config_panel.ids.select_path_panel.bind(tree=frame.ids.resource_tree.setter('data'))
        return frame


if __name__ == '__main__':
    MainWindow().run()
