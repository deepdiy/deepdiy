from core.plugin_mgr import PluginManager
from core.widget_mgr import WidgetManager

from kivy.app import App
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty

class MainWindow(App):
    title='Deep Worm'
    data=DictProperty()
    plugins=DictProperty()

    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.plugin_manager=PluginManager()
        self.widget_manager=WidgetManager()

    def build(self):
        self.plugin_manager.load()
        return self.widget_manager


if __name__ == '__main__':
    MainWindow().run()
