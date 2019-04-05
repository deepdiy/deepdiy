from core.plugin_mgr import PluginManager
from core.widget_mgr import WidgetManager
from core.display_mgr import DisplayManager

from test.debug import *

from kivy.app import App
from kivy.properties import DictProperty
from threading import Thread

class MainWindow(App):
    title='Deep Lab'
    data=DictProperty()
    plugins=DictProperty()

    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def loading(self):
        self.plugin_manager=PluginManager()
        self.plugin_manager.load()
        self.display_manager=DisplayManager()
        debug()

    def build(self):
        self.widget_manager=WidgetManager()
        Thread(target=self.loading).start()
        return self.widget_manager

if __name__ == '__main__':
    MainWindow().run()
