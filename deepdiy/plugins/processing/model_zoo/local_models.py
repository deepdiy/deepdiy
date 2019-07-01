import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,StringProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from utils.get_file_list import get_file_list
from middleware.widget_handler import WidgetHandler
from middleware.plugin_handler import PluginHandler


class LocalModelCard(BoxLayout):
	"""docstring for LocalModelCard."""

	title=StringProperty()
	id=StringProperty()
	tags=StringProperty()
	abstract=StringProperty()
	logo_path=StringProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py

	def __init__(self, model_id):
		super(LocalModelCard, self).__init__()
		self.id = model_id
		meta_path = os.sep.join([
			self.bundle_dir,'plugins','processing','model_zoo','models',self.id,'meta.json'])
		meta_info = json.load(open(meta_path))
		self.title = meta_info['title']
		self.abstract = meta_info['abstract']
		self.logo_path = meta_info['logo']

	def popup_readme(self):
		readme_path=os.sep.join([
			self.bundle_dir,'plugins','processing','model_zoo','models',self.id,'README.md'])
		f=open(readme_path).read()
		description=Popup(title=self.title,size_hint=(None,None),height=500,width=700)
		description.add_widget(RstDocument(text=f))
		description.open()

	def load_model(self):
		widget_handler=WidgetHandler()
		plugin_handler=PluginHandler()
		widget_handler.switch_screens('processing','predict')
		plugin_handler.set_plugin_attr(
			'predict','model_id',self.id)

	def train_model(self):
		widget_handler=WidgetHandler()
		plugin_handler=PluginHandler()
		widget_handler.switch_screens('processing','train')
		plugin_handler.set_plugin_attr(
			'train','model_id',self.id)
		#

class LocalModels(StackLayout):
	"""docstring for Run."""
	models = ListProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'local_models.kv')

	def __init__(self):
		super(LocalModels, self).__init__()
		self.refresh()

	def collect_models(self):
		model_zoo_dir=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo'])
		if not os.path.isdir(model_zoo_dir+os.sep+'models'):
			return
		self.model_names=os.listdir(model_zoo_dir+os.sep+'models')
		self.models=[name for name in self.model_names if name[:2]!='__']

	def render_model_cards(self):
		for model_id in self.models:
			self.add_widget(Factory.LocalModelCard(model_id))

	def refresh(self,*args):
		self.clear_widgets()
		self.collect_models()
		self.render_model_cards()


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=LocalModels()
		return demo

if __name__ == '__main__':
	test=Test().run()
