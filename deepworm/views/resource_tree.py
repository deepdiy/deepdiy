import kivy
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.app import App


class ResourceTree(TreeView):
    def __init__(self, data):
        super(ResourceTree, self).__init__()
        self.data = data
        self.populate_tree_view(None, data)

    def populate_tree_view(self, parent, node):
        if parent is None:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True))
        else:
            tree_node = self.add_node(TreeViewLabel(text=node['node_id'],is_open=True), parent)
        for child_node in node['children']:
            self.populate_tree_view(tree_node, child_node)


class TestApp(App):
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
        return ResourceTree(data)


if __name__ == '__main__':
    TestApp().run()
