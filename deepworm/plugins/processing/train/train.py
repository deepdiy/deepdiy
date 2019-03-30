import sys,os
sys.path.append('../../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from utils.get_parent_path import get_parent_path
from plugins.processing.networks.model_collector import ModelCollector
import webbrowser


class Train(BoxLayout):
	"""docstring for Train."""
	data=DictProperty()
	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'train.kv')

	def __init__(self):
		super(Train, self).__init__()
		self.models=ModelCollector().models
		self.ids.model_spinner.values=self.models

	def label(self):
		print('hi')
		webbrowser.open(self.bundle_dir+os.sep+'via'+os.sep+'via.html')

	def train(self):
		print('train')


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		self.train=Train()

	def build(self):
		return self.train


if __name__ == '__main__':
	test=Test().run()
