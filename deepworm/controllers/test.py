from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.uix.treeview import TreeViewLabel
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button

class TreeViewButton(Button, TreeViewNode):
    pass

modGroups = [u'Fruit', u'Fruit', u'Meat', u'Dairy', u'Dairy', u'Fruit']
modItems = [u'Apple', u'Pear', u'Spam', u'Egg', u'Milk', u'Banana']
modDict = dict()
modDictUnique = dict()

def populate_tree_view(tv):
    modDict = zip(modGroups, modItems)
    for k, v in modDict:
        if k not in modDictUnique:
            modDictUnique[k] = [v]
        else:
            modDictUnique[k].append(v)
    sortedGroups = modDictUnique.keys()
    #print modItems
    #print modDictUnique
    n = tv.add_node(TreeViewLabel(text='Food', is_open=True))
    for group in sortedGroups:
        g = tv.add_node(TreeViewLabel(text='%s' % group), n)
        for item in modDictUnique[group]:
            tv.add_node(TreeViewButton(text='%s' % item), g)

class POSFMApp(App):

    def build(self):
        #for i in range(30):
        #    btn = Button(text=str(i), size=(480, 40),
        #                 size_hint=(None, None))
        #    layout.add_widget(btn)
        tv = TreeView(root_options=dict(text='Tree One'), hide_root=True, indent_level=4)
        tv.size_hint = 1, None
        # tv.bind(minimum_height = tv.setter('height'))
        populate_tree_view(tv)
        root = ScrollView(pos = (0, 0))
        root.add_widget(tv)
        return root

if __name__ == '__main__':
    POSFMApp().run()
