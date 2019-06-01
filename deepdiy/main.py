from core.data_mgr import Data
from core.widget_mgr import WidgetManager
from core.display_mgr import DisplayManager
from core.plugin_mgr import PluginManager
from kivy.app import App
from kivy.properties import ObjectProperty,DictProperty

# from test.debug import *

class MainWindow(App):
	title='DeepDIY'
	data=ObjectProperty(force_dispatch=True)
	plugins=DictProperty(force_dispatch=True)

	def __init__(self,**kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.data=Data() # assign data first to reduce dispatching observers
		self.widget_manager=WidgetManager()
		self.display_manager=DisplayManager()
		self.plugin_manager=PluginManager()
		self.plugin_manager.load_plugins()

	def build(self):
		return self.widget_manager

if __name__ == '__main__':
	MainWindow().run()
