import os
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import pysnooper


class ResourceTree(TreeView):
    data=ObjectProperty(lambda: None)
    def __init__(self, **kwargs):
        super(ResourceTree, self).__init__()
        self.bind(data=self.update_tree_view)
        self.size_hint_y = None
        self.bind(minimum_height = self.setter('height'))
        self.bind(selected_node = self.update_selection)
        self.hide_root=True
        self.ignore_data_change=False

    def update_selection(self,instance,node):
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
        self.data.select_idx=index_chain

    def populate_tree_view(self, parent, node):
        if parent is None:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True))
        else:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True), parent)
        for child_node in node['children']:
            self.populate_tree_view(tree_node, child_node)

    def depopulate(self,*arg):
        self.deselect_node()
        for node in self.iterate_all_nodes():
            self.remove_node(node)

    # @pysnooper.snoop()
    def update_tree_view(self,*arg):
        if not hasattr(self.data,'tree'):
            return
        self.depopulate()
        self.populate_tree_view(None, self.data.tree)
        try:
            self.auto_select()
        except:
            pass

    def auto_select(self):
        node=self.root
        for i in self.data.select_idx:
            node=node.nodes[i]
        last_child=len(node.nodes)-1
        if last_child>-1:
            self.ignore_data_change=True
            self.select_node(node.nodes[last_child])
        else:
            self.ignore_data_change=True
            self.select_node(node)


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
        self.resource_tree.update_tree_view()

    def build(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        root=BoxLayout()
        window=ScrollView(scroll_type=["bars"],  bar_width=20)
        root.add_widget(window)
        window.add_widget(self.resource_tree)
        root.add_widget(Button(text='Clear',on_press=self.resource_tree.depopulate))
        root.add_widget(Button(text='Update',on_press=self.resource_tree.update_tree_view))
        return root


if __name__ == '__main__':
    TestApp().run()
