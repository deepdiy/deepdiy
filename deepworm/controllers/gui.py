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

Builder.load_file('../views/frame.kv')
Builder.load_file('../views/menu.kv')
Builder.load_file('../views/select_path_panel.kv')



class MainWindow(App):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resource_tree=ResourceTree(data)

    def alert(self,*args):
        self.resource_tree.data={'node_id': '1',
        'children': []}
        self.resource_tree.update_tree_view()

    def build(self):
        frame=Frame()
        frame.ids.source_tree.add_widget(self.resource_tree)

        select_path_panel=SelectPathPanel()
        frame.ids.options.add_widget(select_path_panel)
        select_path_panel.bind(file_path=self.alert)
        select_path_panel.bind(file_path=self.alert)
        return frame


if __name__ == '__main__':
    MainWindow().run()
