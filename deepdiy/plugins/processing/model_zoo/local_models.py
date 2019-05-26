import os,rootpath
rootpath.append(pattern='plugins')
import importlib
from utils.get_file_list import get_file_list
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button


class LocalModelCard(BoxLayout):
	"""docstring for LocalModelCard."""

	title=StringProperty()
	id=StringProperty()
	tags=StringProperty()
	abstract=StringProperty()

	def __init__(self, **kwargs):
		super(LocalModelCard, self).__init__()
		self.title=kwargs['title']
		self.id=kwargs['id']
		# self.tags=kwargs['tags']
		self.abstract=kwargs['abstract']


class LocalModels(StackLayout):
	"""docstring for Run."""
	bundle_dir = rootpath.detect(pattern='plugins')
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'local_models.kv')

	def __init__(self):
		super(LocalModels, self).__init__()
		self.models={}
		self.scan_model_zoo()
		self.render_model_cards()

	def scan_model_zoo(self):
		model_zoo_dir=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo'])
		self.model_names=os.listdir(model_zoo_dir+os.sep+'models')
		self.model_names=[name for name in self.model_names if name[:2]!='__']
		for name in self.model_names:
			module_name='.'.join(['plugins','processing','model_zoo','models',name,'api'])
			module=importlib.import_module(module_name)
			self.models[name]=getattr(module,'Api')()
			self.models[name].config_list=get_file_list(model_zoo_dir+os.sep+'models'+os.sep+name+os.sep+'configs')
			self.models[name].weight_list=get_file_list(model_zoo_dir+os.sep+'weights'+os.sep+name)
			self.models[name].train_notebooks=get_file_list(model_zoo_dir+os.sep+'models'+os.sep+name+os.sep+'training',formats=['ipynb'])

	def render_model_cards(self):
		for model in self.models:
			self.add_widget(Factory.LocalModelCard(
				title='MRCNN',id='mrcnn',abstract='wwwwwwwww'))


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=LocalModels()
		print(demo.models)
		return demo

if __name__ == '__main__':
	test=Test().run()
