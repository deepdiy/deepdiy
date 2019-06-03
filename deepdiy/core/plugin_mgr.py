import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import pkgutil,importlib,inspect,string,shutil
from pebble.concurrent import thread
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import DictProperty,ObjectProperty
import plugins
from core.plugin_wrapper import PluginWrapper


class PluginManager(ModalView):
	"""Manage plugins

	Manage plugins by managing plugin wrappers. Each plugin wrapper will manage
	the whole lifetime of an individual plugin, and PluginManager manage
	plugins by interface provided by plugin wrappers.

	This module also provide GUI, which exhibit all valid plugins in a
	StackLayout, each plugin own a card display basic info of the plugin and
	button to disable of reload the plugin. The cards are provide by plugin
	wrappers.

	Attributes:
		plugins: a dictionary stores wrapper of each plugin.
			a typical item in this dictionary looks like this:
				<plugin id>:{
					'type':<type of plugin>,
					'disabled':<is_plugin_disabled>,
					'wrapper':<wrapper of plugin>,
					'instance':<instance of plugin>}
		bundle_dir: the dir of main.py
	"""
	plugins=DictProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'plugin_mgr.kv')

	def __init__(self,**kwargs):
		super(PluginManager, self).__init__(**kwargs)
		'''Sync plugins with App'''
		app=App.get_running_app()
		app.bind(plugins=self.setter('plugins'))
		self.bind(plugins=app.setter('plugins'))
		self.bind(plugins=self.update_gui)

	def load_plugins(self):
		self.find_plugin_packages()
		collect_plugin_task=self.collect_plugins()
		collect_plugin_task.add_done_callback(self.on_collect_plugins_finished)

	def find_plugin_packages(self):
		self.plugin_package_names=[]
		for importer, modname, ispkg in pkgutil.walk_packages(path=plugins.__path__,prefix=plugins.__name__+'.',onerror=lambda x: None):
			if len(modname.split('.'))>2:
				self.plugin_package_names.append(modname)

	@ thread # run in separate thread
	def collect_plugins(self):
		for name in self.plugin_package_names:
			plugin_wrapper=PluginWrapper(name)
			if plugin_wrapper.is_valid is True:
				plugin_wrapper.bind(is_disabled=self.on_plugin_disable_clicked)
				plugin_wrapper.bind(is_valid=self.on_plugin_validity_changed)
				plugin_wrapper.bind(instance=self.on_plugin_instance_changed)
				self.plugins[plugin_wrapper.id]={'type':plugin_wrapper.type,'disabled':False,'wrapper':plugin_wrapper,'instance':plugin_wrapper.instance}

	def on_plugin_disable_clicked(self,instance,value):
		self.plugins[instance.id]['disabled'] = value
		# value change is not in top-level, so need to dispatch manually
		self.property('plugins').dispatch(self)

	def on_plugin_validity_changed(self,instance,value):
		if value == False:
			self.plugins[instance.id]['disabled'] = True
			# value change is not in top-level, so need to dispatch manually
			self.property('plugins').dispatch(self)
			del self.plugins[instance.id]

	def on_plugin_instance_changed(self,plugin_wrapper,value):
		if plugin_wrapper.instance != None:
			self.plugins[plugin_wrapper.id]={'type':plugin_wrapper.type,'disabled':False,'wrapper':plugin_wrapper,'instance':plugin_wrapper.instance}
			# value change is not in top-level, so need to dispatch manually
			self.property('plugins').dispatch(self)

	def on_collect_plugins_finished(self,*args):
		pass

	def update_gui(self,*ars):
		self.ids.plugin_album.clear_widgets()
		for plugin_id in self.plugins:
			self.ids.plugin_album.add_widget(self.plugins[plugin_id]['wrapper'])

	def reload_all_plugins(self):
		for id in self.plugins:
			self.plugins[id]['wrapper'].reload()


class Test(App):
	data=DictProperty()
	plugins=DictProperty()
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		plugin_manager=PluginManager()
		plugin_manager.load_plugins()
		return plugin_manager

if __name__ == '__main__':
	test=Test().run()
