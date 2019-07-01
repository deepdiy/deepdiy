from core.data_mgr import Data
from core.widget_mgr import WidgetManager
from core.display_mgr import DisplayManager
from core.plugin_mgr import PluginManager
from kivy.app import App
from kivy.properties import ObjectProperty,DictProperty


class MainWindow(App):
	''' The entrance of App

	This class is a subclass of kivy App class, it has a built-in run()
		method to start the App.
	In this App, there are four core components:
		Data(): data object are shared and sync with all plugins
		WidgetManager(): Provide window and organize widgets in window
		DisplayManager(): Monitor data changes and update contents in widgets
		PluginManager(): Load and manage plugins

	Attributes:
		title: the title shown on the window
		data: object, the data object will be shared and sync with all plugins
		plugins: dict, the collection of loaded Plugins
	'''
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
