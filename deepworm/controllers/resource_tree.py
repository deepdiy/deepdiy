import kivy
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.app import App
from kivy.properties import DictProperty



class ResourceTree(TreeView):
    data = DictProperty()
    def __init__(self, tree_data):
        super(ResourceTree, self).__init__()
        self.data = tree_data
        self.populate_tree_view(None, self.data)
        data = self.data
        self.bind(data=self.update_tree_view)

    def populate_tree_view(self, parent, node):
        if parent is None:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True))
        else:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True), parent)
        for child_node in node['children']:
            self.populate_tree_view(tree_node, child_node)

    def depopulate(self,*arg):
        for node in self.root.nodes:
            self.remove_node(node)

    def update_tree_view(self,*arg):
        self.depopulate()
        self.populate_tree_view(None, self.data)



class TestApp(App):
    def __init__(self):
        super(TestApp, self).__init__()
        self.data={'node_id': '1',
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
        self.resource_tree=ResourceTree(self.data)

    def build(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        window=BoxLayout()
        window.add_widget(self.resource_tree)
        window.add_widget(Button(text='Clear',on_press=self.resource_tree.depopulate))
        window.add_widget(Button(text='Update',on_press=self.resource_tree.update_tree_view))
        return window


if __name__ == '__main__':
    TestApp().run()
