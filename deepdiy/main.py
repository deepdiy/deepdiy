from core.plugin_mgr import PluginManager
from core.widget_mgr import WidgetManager
from core.display_mgr import DisplayManager
from core.data_mgr import Data
from kivy.app import App
from kivy.properties import ObjectProperty,DictProperty
from threading import Thread
from test.debug import *

class MainWindow(App):
    title='DeepDIY'
    data=ObjectProperty(lambda: None,force_dispatch=True)
    plugins=DictProperty()

    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def load_plugins(self):
        self.plugin_manager=PluginManager()
        self.plugin_manager.load_plugins()
        self.display_manager=DisplayManager()
        self.data=Data()
        debug()

    def build(self):
        self.widget_manager=WidgetManager()
        Thread(target=self.load_plugins).start()
        return self.widget_manager

if __name__ == '__main__':
    MainWindow().run()
