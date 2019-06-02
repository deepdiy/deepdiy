import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,StringProperty,BooleanProperty
from kivy.uix.boxlayout import BoxLayout
import pkgutil,importlib,inspect,string,shutil,time,logging

class PluginWrapper(BoxLayout):
	"""A wrapper of plugin to manage the life-time of a plugin

	PluginManager manage plugins by instances of this class
	Attributs:
		data: ObjectProperty, sync with App' data attribute.
			used to sync with plugin instance's data attribute.
		id: id of plugin, e.g. 'model_zoo'
		type: string, e.g. 'processing'
		title: string, e.g. 'Model Zoo'
		is_valid: boolean, validity of the plugin,
			if False, plugin will not be instantiated.
			PlugnManager() will not load invalid Plugin, if loaded, will removed
		is_disabled: boolean,
			if False, WidgetManager() will remove the widgets of this plugin
		instance:object, instance of plugin Plugin
	"""
	data=ObjectProperty()
	id=StringProperty()
	type=StringProperty()
	title=StringProperty()
	is_valid=BooleanProperty(False)
	is_disabled=BooleanProperty(False)
	instance=ObjectProperty(allownone=True)
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'plugin_wrapper.kv')

	def __init__(self,package_name):
		super(PluginWrapper, self).__init__()
		self.package_name=package_name
		self.type=package_name.split('.')[1]
		self.id=package_name.split('.')[2]
		self.title=string.capwords(self.id.replace('_',' '))
		self.import_package()
		self.instantiate()

	def import_package(self):
		try:
			package=importlib.import_module(self.package_name)
		except Exception as e:
			logging.warning('Error when load {}:{}'.format(self.package_name,e))
			return
		for attr_id in dir(package):
			attr = getattr(package, attr_id)
			if inspect.isclass(attr) and attr_id==self.title.replace(' ',''):
				self._class=attr
				self.is_valid=True

	def instantiate(self):
		if self.is_valid == False:
			return
		self.instance=self._class()
		app=App.get_running_app()
		if hasattr(self.instance,'data') and self.type=='processing':
			'''use and sync app's data property'''
			self.instance.data=app.data
			app.bind(data=self.instance.setter('data'))
			self.instance.bind(data=app.setter('data'))

	def reload(self):
		self.is_valid=False # to tell plugin_mgr to remove this plugin
		self.remove_pycache() # to prevent use pycache when re-import plugin
		self.import_package()
		self.instantiate()

	def remove_pycache(self):
		pycache_dir=os.sep.join([self.bundle_dir]+self.package_name.split('.')[:-1]+['__pycache__'])
		if os.path.exists(pycache_dir):
			try:shutil.rmtree(pycache_dir)
			except Exception as e:
				print(e)

	def unload_kv_file(self,id):
		kv_path=os.sep.join([self.bundle_dir,'ui',self.id+'.kv'])
		print(kv_path)
		try: Builder.unload_file(kv_path)
		except Exception as e:
			print(e)


class Test(App):
	"""docstring for Test."""
	data=ObjectProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=PluginWrapper('plugins.processing.train.train')
		return demo

if __name__ == '__main__':
	Test().run()
