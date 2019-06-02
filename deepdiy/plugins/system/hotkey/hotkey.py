import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,StringProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.clock import Clock
from middleware.plugin_handler import PluginHandler
from middleware.widget_handler import WidgetHandler

class Hotkey(BoxLayout):
    """ Add hotkeys for the App
    Attributes:
        keycode: list, e.g. ['lctrl']
        modifiers: list, e.g. ['s']
    """

    keycode=ListProperty()
    modifiers=ListProperty()

    def __init__(self, **kwargs):
        super(Hotkey, self).__init__(**kwargs)

        '''add keyboard binding with clock, otherwise will lead to
        System No Response'''
        Clock.schedule_once(self.add_binding) # if not use clock, will conflict

    def add_binding(self,*args):
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down,on_key_up=self._on_keyboard_up)
        self.bind(keycode=self.trigger_hotkey)
        self.bind(modifiers=self.trigger_hotkey)

    def _keyboard_closed(self):
        self.modifiers=[]

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode not in self.keycode:
            self.keycode.append(keycode[1])
        if 'lctrl' not in self.modifiers and keycode[1] in ["lctrl"]:
            self.modifiers.append(keycode[1])
            return True
        else:
            return True

    def _on_keyboard_up(self, window=None, keycode=None):
        self.keycode =[]
        self.modifiers = []

    def trigger_hotkey(self,*args):
        if 'f1' in self.keycode:
            app=App.get_running_app()
            app.plugin_manager.open()
        if 'f5' in self.keycode:
            widget_handler=WidgetHandler()
            plugin_handler=PluginHandler()
            plugins=[]

            '''reload current processing plugin'''
            p1=widget_handler.processing_screens.current
            plugin_handler.plugins[p1]['wrapper'].reload()
            widget_handler.processing_screens.current=p1

            '''reload current display plugin'''
            p2=widget_handler.display_screens.current
            plugin_handler.plugins[p2]['wrapper'].reload()
            widget_handler.display_screens.current=p2
        if 'f2' in  self.keycode:
            app=App.get_running_app()
            app.plugin_manager.reload_all_plugins()


class Test(App):
    """docstring for Test."""

    def __init__(self):
        super(Test, self).__init__()

    def build(self):
        from main import MainWindow
        from core.plugin_wrapper import PluginWrapper
        plugin_wrapper = PluginWrapper('plugins.processing.hotkey')
        hotkey=Hotkey()
        app = MainWindow()
        window = app.build()
        app.plugins['hotkey']={
        'type':'processing','disabled':False,'instance':hotkey,'wrapper':plugin_wrapper}
        return window

if __name__ == '__main__':
    Test().run()
