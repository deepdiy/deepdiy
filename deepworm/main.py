from core.plugin_mgr import PluginManager
from core.widget_mgr import WidgetManager
from core.display_mgr import DisplayManager

from test.auto_run import *

from kivy.app import App
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty

class MainWindow(App):
    title='Deep Lab'
    data=DictProperty()
    plugins=DictProperty()

    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.plugin_manager=PluginManager()
        self.widget_manager=WidgetManager()
        self.display_manager=DisplayManager()

    def build(self):
        self.plugin_manager.load()
        load_demo()
        return self.widget_manager

if __name__ == '__main__':
    MainWindow().run()
