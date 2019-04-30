import sys,os
sys.path.append('../../../')
from utils.get_parent_path import get_parent_path

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,StringProperty,ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument

import glob
import string
import json

class DemoCard(BoxLayout):
	title=StringProperty()
	id=StringProperty()
	type=StringProperty()
	image_source=StringProperty()
	operations=ObjectProperty()
	def __init__(self,demo_path):
		super(DemoCard, self).__init__()
		self.demo_path=demo_path
		name=demo_path.split(os.sep)[-1]
		self.title=name.split('+')[1].replace('_',' ')
		self.type=name.split('+')[0]
		self.image_source=os.sep.join([self.demo_path,'logo.png'])

	def load_description(self):
		f=open(os.sep.join([self.demo_path,'readme.md'])).read()
		description=Popup(title=self.title,size_hint=(None,None),height=500,width=700)
		description.add_widget(RstDocument(text=f))
		description.open()

	def load_demo(self):
		app=App.get_running_app()
		json_path=os.sep.join([self.demo_path,'config.json'])
		demo_config=json.load(open(json_path))
		print(demo_config)
		if hasattr(app,'widget_manager'):
			app.widget_manager.ids.processing_screens.children[0].children[0]
			app.widget_manager.ids.processing_screens.current='files'
			app.widget_manager.ids.processing_screens.children[0].children[0].add_to_tree(os.sep.join([self.demo_path,'images']))
			app.widget_manager.ids.processing_screens.current='networks'
			networks=app.widget_manager.ids.processing_screens.children[0].children[0]
			networks.ids.model_spinner.text=demo_config['model']
			networks.ids.weight_spinner.text=demo_config['weight']
			networks.ids.config_spinner.text=demo_config['config']


class Gallery(BoxLayout):
	"""docstring for Gallery."""

	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'gallery.kv')

	def __init__(self):
		super(Gallery, self).__init__()
		self.collect_demos()

	def collect_demos(self):
		demos=glob.glob(os.sep.join([self.bundle_dir,'plugins','processing','gallery','demos','*']))
		for demo in demos:
			self.ids.demo_album.add_widget(DemoCard(demo))


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		gallery=Gallery()
		return gallery

if __name__ == '__main__':
	Test().run()
