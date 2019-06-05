import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import pysnooper
from plugins.display.resource_tree.tree_widget import TreeWidget


class ResourceTree(BoxLayout):

    data=ObjectProperty(lambda:None)

    def __init__(self, **kwargs):
        super(ResourceTree, self).__init__()
        self.bind(data=self.refresh)
        self.size_hint_y = None
        self.bind(minimum_height = self.setter('height'))
        # self.bind(selected_node = self.update_selection)
        self.hide_root=True


    # @pysnooper.snoop()
    def refresh(self,*arg):
        if not hasattr(self.data,'tree'):
            return
        self.tree=TreeWidget(self.data.tree)
        self.tree.bind(select_idx=self.data.setter('select_idx'))
        self.tree.select_idx = self.auto_select()
        self.clear_widgets()
        self.add_widget(self.tree)

    def auto_select(self):
        try:
            selected_data = self.data.get_selected_data()
            if len(selected_data['children'])>0:
                return self.data.select_idx + [len(selected_data['children'])-1]
            else:
                return self.data.select_idx
        except Exception as e:
            print (e)



class TestApp(App):
    def __init__(self):
        super(TestApp, self).__init__()
        self.resource_tree=ResourceTree()
        self.resource_tree.data.tree={'node_id': '1',
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
        self.resource_tree.refresh()

    def build(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        root=BoxLayout()
        window=ScrollView(scroll_type=["bars"],  bar_width=20)
        root.add_widget(window)
        window.add_widget(self.resource_tree)
        return root


if __name__ == '__main__':
    TestApp().run()
