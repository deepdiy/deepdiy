import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import importlib
import glob
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from middleware.widget_handler import WidgetHandler
from middleware.plugin_handler import PluginHandler


class LocalDemoCard(BoxLayout):
	"""docstring for LocalDemoCard."""
	demo_id = StringProperty()
	demo_path = StringProperty()
	meta_info = DictProperty()
	bundle_dir=rootpath.detect(pattern='main.py')

	def __init__(self,demo_id):
		super(LocalDemoCard, self).__init__()
		self.demo_id = demo_id
		self.demo_path = os.sep.join([
			self.bundle_dir,'plugins','processing','model_zoo','demos',self.demo_id])
		self.load_meta_info()

	def load_meta_info(self):
		meta_path = os.sep.join([
			self.bundle_dir,'plugins','processing','model_zoo','demos',self.demo_id,'meta.json'])
		self.meta_info = json.load(open(meta_path))

	def popup_readme(self):
		f=open(os.sep.join([self.demo_path,'readme.md'])).read()
		description=Popup(title=self.meta_info['title'],size_hint=(None,None),height=500,width=700)
		description.add_widget(RstDocument(text=f))
		description.open()

	def load_demo(self):
		widget_handler=WidgetHandler()
		plugin_handler=PluginHandler()
		widget_handler.switch_screens('processing','predict')
		plugin_handler.set_plugin_attr(
			'files','path',os.sep.join([self.demo_path,'images']))
		plugin_handler.set_plugin_attr(
			'predict','model_id',self.meta_info['model'])
		plugin_handler.set_plugin_attr(
			'predict','config_id',self.meta_info['model_config'])
		plugin_handler.set_plugin_attr(
			'predict','weight_id',self.meta_info['weight_url'].split('/')[-1])


class LocalDemos(StackLayout):
	"""docstring for Run."""
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'local_demos.kv')

	def __init__(self):
		super(LocalDemos, self).__init__()
		self.models={}
		self.refresh()

	def collect_demos(self):
		demos_path_list=glob.glob(os.sep.join([self.bundle_dir,'plugins','processing','model_zoo','demos','*']))
		for path in demos_path_list:
			demo_id = path.split(os.sep)[-1]
			self.add_widget(
				Factory.LocalDemoCard(demo_id))

	def refresh(self,*arg):
		self.clear_widgets()
		self.collect_demos()


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=LocalDemos()
		return demo

if __name__ == '__main__':
	test=Test().run()
