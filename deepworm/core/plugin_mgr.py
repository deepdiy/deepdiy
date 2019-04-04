import sys,os
sys.path.append(os.path.dirname(sys.path[0]))

import inspect
import plugins as plugins
import pkgutil,importlib

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import DictProperty
import threading


class PluginManager(EventDispatcher):
	"""docstring for PluginManager."""
	plugins=DictProperty({})
	data=DictProperty()
	def __init__(self,**kwargs):
		super(PluginManager, self).__init__(**kwargs)
		app=App.get_running_app()
		if app!=None:
			app.bind(data=self.setter('data'))
			self.bind(data=app.setter('data'))
			app.bind(plugins=self.setter('plugins'))
			self.bind(plugins=app.setter('plugins'))

	def load(self):
		self.find_plugin_packages()
		self.collect_plugins()
		self.load_plugins()

	def find_plugin_packages(self):
		self.plugin_package_names=[]
		for importer, modname, ispkg in pkgutil.walk_packages(path=plugins.__path__,prefix=plugins.__name__+'.',onerror=lambda x: None):
			if len(modname.split('.'))>2:
				self.plugin_package_names.append(modname)

	def collect_plugins(self):
		classes=[]
		for name in self.plugin_package_names:
			type,id=name.split('.')[1:3]
			package=importlib.import_module(name)
			for atrribute in dir(package):
				obj = getattr(package, atrribute)
				if inspect.isclass(obj) and atrribute.lower()==id.replace('_',''):
					classes.append({'id':id,'type':type,'class':obj})
		self.plugins['classes']=classes

	def load_plugins(self):
		instances=[]
		app=App.get_running_app()
		for plugin in self.plugins['classes']:
			obj=plugin['class']()
			if app!=None and plugin['type']=='processing':
				app.bind(data=obj.setter('data'))
				obj.bind(data=app.setter('data'))
			instances.append({'id':plugin['id'],'type':plugin['type'],'obj':obj})
		self.plugins['instances']=instances


class Test(object):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		class_manager=PluginManager()
		class_manager.load()
		print(class_manager.plugins.classes)
		print(class_manager.plugins.instances)

if __name__ == '__main__':
	test=Test()
