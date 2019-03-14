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
from kivy.event import EventDispatcher

data={'node_id': '1',
'children': [{'node_id': '1.1',
              'children': [{'node_id': '1.1.1',
                            'children': [{'node_id': '1.1.1.1',
                                          'children': []}]},
                           {'node_id': '1.1.2',
                            'children': []},
                           {'node_id': '1.1.3',
                            'children': []}]},
              {'node_id': '1.2',
               'children': []}]}

class Frame(BoxLayout):
    pass


class Menu(BoxLayout):
    pass


class MainWindow(App):
    Builder.load_file('../views/frame.kv')
    Builder.load_file('../views/menu.kv')
    Builder.load_file('../views/openpanel.kv')
    def alert(self,*args):
        print('hi')

    def build(self):
        frame=Frame()
        frame.ids.source_tree.add_widget(ResourceTree(data))

        select_path_panel=SelectPathPanel()
        frame.ids.options.add_widget(select_path_panel)
        open_panel.bind(file_path=self.alert)
        open_panel.bind(file_path=self.alert)
        print(open_panel.file_path)
        return frame


if __name__ == '__main__':
    MainWindow().run()
