import os,rootpath
rootpath.append(pattern='plugins')
import importlib,glob
from utils.get_file_list import get_file_list
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument


class LocalDemoCard(BoxLayout):
	"""docstring for LocalDemoCard."""

	title=StringProperty()
	id=StringProperty()
	tags=StringProperty()
	abstract=StringProperty()
	demo_path=StringProperty()
	image_source=StringProperty()

	def __init__(self,demo_path=''):
		super(LocalDemoCard, self).__init__()
		self.demo_path=demo_path
		self.title=demo_path.split(os.sep)[-1]
		# self.tags=kwargs['tags']
		self.abstract='mrcnn'
		self.image_source=os.sep.join([self.demo_path,'logo.png'])

	def popup_readme(self):
		f=open(os.sep.join([self.demo_path,'readme.md'])).read()
		description=Popup(title=self.title,size_hint=(None,None),height=500,width=700)
		description.add_widget(RstDocument(text=f))
		description.open()
	#
	# def load_demo(self):
	# 	app=App.get_running_app()
	# 	json_path=os.sep.join([self.demo_path,'config.json'])
	# 	demo_config=json.load(open(json_path))
	# 	print(demo_config)
	# 	if hasattr(app,'widget_manager'):
	# 		app.widget_manager.ids.processing_screens.children[0].children[0]
	# 		app.widget_manager.ids.processing_screens.current='files'
	# 		app.widget_manager.ids.processing_screens.children[0].children[0].add_to_tree(os.sep.join([self.demo_path,'images']))
	# 		app.widget_manager.ids.processing_screens.current='networks'
	# 		networks=app.widget_manager.ids.processing_screens.children[0].children[0]
	# 		networks.ids.model_spinner.text=demo_config['model']
	# 		networks.ids.weight_spinner.text=demo_config['weight']
	# 		networks.ids.config_spinner.text=demo_config['config']


class LocalDemos(StackLayout):
	"""docstring for Run."""
	bundle_dir = rootpath.detect(pattern='plugins')
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'local_demos.kv')

	def __init__(self):
		super(LocalDemos, self).__init__()
		self.models={}
		self.collect_demos()

	def collect_demos(self):
		demos=glob.glob(os.sep.join([self.bundle_dir,'plugins','processing','model_zoo','demos','*']))
		for demo in demos:
			print(1)
			self.add_widget(Factory.LocalDemoCard(demo_path=demo))


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
