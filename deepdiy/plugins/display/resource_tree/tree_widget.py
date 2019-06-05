import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import pysnooper
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import ObjectProperty,DictProperty,ListProperty
from kivy.core.window import Window
from kivy.clock import Clock


class TreeWidget(TreeView):

    data = DictProperty()
    select_idx = ListProperty()

    def __init__(self,data):
        super(TreeWidget, self).__init__()

        self.data = data
        self.size_hint_y = None
        self.hide_root=True
        self.bind(minimum_height = self.setter('height'))
        self.bind(selected_node = self.on_selected_node)
        self.populate_tree_view(None, self.data)

    def populate_tree_view(self, parent, node):
        if parent is None:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True))
        else:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True), parent)
        for child_node in node['children']:
            self.populate_tree_view(tree_node, child_node)

    def on_selected_node(self,instance,node):
        if node ==None:
            return
        index_chain=[]
        current=node
        for i in range(100):
            if current.text!='Root':
                index_chain.insert(0,current.parent_node.nodes.index(current))
                current=current.parent_node
            else:
                break
        self.select_idx = index_chain

    def on_select_idx(self,*args):
        node=self.root
        for i in self.select_idx:
            node=node.nodes[i]
        self.select_node(node)


class TestApp(App):
    def __init__(self):
        super(TestApp, self).__init__()

    def build(self):
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
        resource_tree=TreeWidget(data)
        resource_tree.select_idx= [0,0,1]
        return resource_tree


if __name__ == '__main__':
    TestApp().run()
