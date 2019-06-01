#!/usr/bin/python3
import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout

class PluginHandler(BoxLayout):
	""" PluginHandler help plugins to manipulate plugins in the app.

	Plugins call functions in this class to interact with other plugins,
	which ensures every plugin can be tested independetly without error.
	"""

	plugins=DictProperty(force_dispatch=True)
	processing_screens=ObjectProperty(lambda:None)

	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py

	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'plugin_handler.kv')

	def __init__(self):
		super(PluginHandler, self).__init__()
		self.bind(plugins=self.show_plugins)
		self._catch_plugins()

	def _catch_plugins(self):
		'''Catch plugins loaded in the running app'''
		app=App.get_running_app()
		app.bind(plugins=self.setter('plugins'))

	def show_plugins(self,*args):
		print(self.plugins)

	def get_plugin_attr(self,plugin_id,attr):
		''' Get attributes of a plugin by plugin id and attribute name
		Args:
			plugin_id: string, e.g. 'files'
			attr: string, e.g. 'path'
		'''
		plugin=self.plugins[plugin_id]['instance']
		return plugin.property(attr)

	def set_plugin_attr(self,plugin_id,attr,value):
		'''
		Args:
			plugin_id: string, e.g. 'files'
			attr: string, e.g. 'path'
			value: any type, e.g. 'd:/'
		'''
		plugin=self.plugins[plugin_id]['instance']
		plugin.setter(attr)(self,value)



class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		'''Testing by take this middleware as a plugin of main program'''
		from main import MainWindow
		app=MainWindow()
		window=app.build()
		plugin_handler=PluginHandler()
		app.plugins['plugin_handler']={
		'type':'processing','disabled':False,'instance':plugin_handler}
		# plugin_handler.set_plugin_attr('files','path',plugin_handler.bundle_dir+'/img/face.jpg')
		# path=plugin_handler.get_plugin_attr('files','path')
		# print(path)
		return window

if __name__ == '__main__':
	Test().run()
