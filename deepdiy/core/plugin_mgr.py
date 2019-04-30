import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path

import inspect
import plugins as plugins
import pkgutil,importlib

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import DictProperty,StringProperty,ObjectProperty

import threading
import time
import string,shutil

class PluginCard(BoxLayout):
	title=StringProperty()
	id=StringProperty()
	type=StringProperty()
	operations=ObjectProperty()
	def __init__(self, **kwargs):
		super(PluginCard, self).__init__()
		self.title=kwargs['title']
		self.id=kwargs['id']
		self.type=kwargs['type']
		self.operations=kwargs['operations']


class PluginManager(ModalView):
	"""docstring for PluginManager."""
	plugins=DictProperty()
	data=ObjectProperty(lambda: None)
	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'plugin_mgr.kv')
	def __init__(self,**kwargs):
		super(PluginManager, self).__init__(**kwargs)
		app=App.get_running_app()
		if app!=None:
			app.bind(data=self.setter('data'))
			self.bind(data=app.setter('data'))
			app.bind(plugins=self.setter('plugins'))
			self.bind(plugins=app.setter('plugins'))
		self.bind(plugins=self.update_form)

	def load_plugins(self):
			self.find_plugin_packages()
			self.collect_plugins()

	def find_plugin_packages(self):
		self.plugin_package_names=[]
		for importer, modname, ispkg in pkgutil.walk_packages(path=plugins.__path__,prefix=plugins.__name__+'.',onerror=lambda x: None):
			if len(modname.split('.'))>2:
				self.plugin_package_names.append(modname)

	def collect_plugins(self):
		plugins={}
		for name in self.plugin_package_names:
			type,id=name.split('.')[1:3]
			package=importlib.import_module(name)
			plugin_class=self.import_plugin(id,name)
			if not plugin_class is None:
				plugin_instance=self.instantiate_plugin(id,type,plugin_class)
				plugins[id]={'type':type,'disabled':False,'class':plugin_class,'instance':plugin_instance}
		self.plugins=plugins

	def import_plugin(self,id,package_name):
		plugin_class=None
		package=importlib.import_module(package_name)
		for atrribute in dir(package):
			plugin_class = getattr(package, atrribute)
			if inspect.isclass(plugin_class) and atrribute.lower()==id.replace('_',''):
				return plugin_class

	def instantiate_plugin(self,id,type,plugin_class):
		app=App.get_running_app()
		plugin_obj=None
		plugin_obj=plugin_class()
		if app!=None and hasattr(plugin_obj,'data') and type=='processing':
			app.bind(data=plugin_obj.setter('data'))
			plugin_obj.bind(data=app.setter('data'))

		return plugin_obj

	def update_form(self,*ars):
		self.ids.plugin_album.clear_widgets()
		operations={'Disable':self.disable_plugin,'Remove':self.remove_plugin,'Reload':self.reload_plugin}
		for id in self.plugins:
			if id=='time':
				continue
			self.ids.plugin_album.add_widget(Factory.PluginCard(
				title=string.capwords(id.replace('_',' ')),id=id,type=string.capwords(self.plugins[id]['type']),operations=operations))

	def reload_all_plugins(self):
		plugins=[str(id) for id in self.plugins]
		for id in plugins:
			self.reload_plugin(id)

	def reload_plugin(self,id):
		self.remove_plugin(id)
		self.remove_pycache(id)
		self.unload_kv_file(id)
		package_names=[name for name in self.plugin_package_names if name.split('.')[-1]==id]
		for name in package_names:
			type=name.split('.')[1]
			package=importlib.import_module(name)
			importlib.reload(package)
			plugin_class=self.import_plugin(id,name)
			if not plugin_class is None:
				plugin_instance=self.instantiate_plugin(id,type,plugin_class)
				self.plugins[id]={'type':type,'class':plugin_class,'instance':plugin_instance,'disabled':False}

	def disable_plugin(self,id):
		self.plugins[id]['disabled']=True
		self.plugins['time']=time.time()

	def remove_plugin(self,id):
		self.disable_plugin(id)
		del self.plugins[id]

	def remove_pycache(self,id):
		package_names=[name for name in self.plugin_package_names if name.split('.')[-1]==id]
		for i in package_names:
			pycache_dir=os.sep.join([self.bundle_dir]+i.split('.')+['__pycache__'])
			if os.path.exists(pycache_dir):
				shutil.rmtree(pycache_dir)

	def unload_kv_file(self,id):
		try:
			Builder.unload_file(os.sep.join([self.bundle_dir,'ui',id+'.kv']))
		except:
			pass

class Test(App):
	data=DictProperty()
	plugins=DictProperty()
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		plugin_manager=PluginManager()
		plugin_manager.load_plugins()
		print(plugin_manager.plugins)
		return plugin_manager

if __name__ == '__main__':
	test=Test().run()
