import kivy
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import DictProperty
from kivy.core.window import Window


class ResourceTree(TreeView):
    data = DictProperty()
    def __init__(self, **kwargs):
        super(ResourceTree, self).__init__(**kwargs)
        self.bind(data=self.update_tree_view)
        self.size_hint = 1, None
        self.bind(minimum_height = self.setter('height'))


    def populate_tree_view(self, parent, node):
        for key in list(node.keys()):
            tree_node = self.add_node(TreeViewLabel(text=key,is_open=True), parent)
            print(key)
        for child_node in node[key]:
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

        self.resource_tree=ResourceTree()
        self.resource_tree.data={'1': [
                    {'1.1': [
                        {'1.1.1': [
                            {'1.1.1.1': []}]},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.2': []},
                        {'1.1.3': []}]},
                      {'1.2': []}]}

    def build(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        root=BoxLayout()
        window=ScrollView()
        root.add_widget(window)
        window.add_widget(self.resource_tree)
        root.add_widget(Button(text='Clear',on_press=self.resource_tree.depopulate))
        root.add_widget(Button(text='Update',on_press=self.resource_tree.update_tree_view))
        return root


if __name__ == '__main__':
    TestApp().run()
