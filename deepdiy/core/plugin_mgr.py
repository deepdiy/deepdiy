import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import DictProperty,StringProperty,ObjectProperty,BooleanProperty,AliasProperty
import plugins
import pkgutil,importlib,inspect,string,shutil
from pebble.concurrent import thread
from core.plugin_wrapper import PluginWrapper


class PluginManager(ModalView):
	"""docstring for PluginManager."""
	plugins=DictProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'plugin_mgr.kv')
	def __init__(self,**kwargs):
		super(PluginManager, self).__init__(**kwargs)
		app=App.get_running_app()
		if app!=None:
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
		# plugins={}
		for name in self.plugin_package_names:
			plugin_wrapper=PluginWrapper(name)
			if plugin_wrapper.is_valid is True:
				plugin_wrapper.bind(is_disabled=self.on_plugin_disable_clicked)
				plugin_wrapper.bind(is_valid=self.on_plugin_validity_changed)
				plugin_wrapper.bind(instance=self.on_plugin_instance_changed)
				self.plugins[plugin_wrapper.id]={'type':plugin_wrapper.type,'disabled':False,'wrapper':plugin_wrapper,'instance':plugin_wrapper.instance}
		# self.plugins=plugins

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
			if plugin_id=='time':
				continue
			self.ids.plugin_album.add_widget(self.plugins[plugin_id]['wrapper'])

	def reload_all_plugins(self):
		plugins=[str(id) for id in self.plugins]
		for id in plugins:
			self.reload_plugin(id)



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
