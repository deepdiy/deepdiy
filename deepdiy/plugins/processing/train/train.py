import sys,os
sys.path.append('../../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import DictProperty
from utils.get_parent_path import get_parent_path
from plugins.processing.networks.model_collector import ModelCollector
import webbrowser
from utils.select_path_dialog import select_file,select_folder
from plugins.processing.train.dataset import Dataset
from core.form_parser import FormParser
import json

class Train(BoxLayout):
	"""docstring for Train."""
	bundle_dir = get_parent_path(3)
	models=ModelCollector().models
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'train.kv')

	def __init__(self):
		super(Train, self).__init__()
		self.ids.config_spinner.bind(text=self.load_config)

	def load_config(self,instance,text):
		self.ids.config_panel.clear_widgets()
		path=os.sep.join([get_parent_path(3),'model_zoo',text,'training','config_form.json'])
		if not os.path.exists(path):
			self.ids.config_panel.add_widget(Label(text='This network do not need configuration'))
			return
		self.form_parser=FormParser()
		self.form_parser.load_json(path)
		self.ids.config_panel.add_widget(self.form_parser)

	def open_via(self):
		webbrowser.open('http://www.robots.ox.ac.uk/~vgg/software/via/via-2.0.4.html')

	def train(self):
		webbrowser.open('https://colab.research.google.com/github/deepdiy/deepdiy/blob/master/deepdiy/model_zoo/'+self.ids.run_net_spinner.text+'/training/'+self.ids.run_notebook_spinner.text)

	def select_annotation_path(self):
		self.annoation_path=select_file()

	def select_config_path(self):
		self.config_path=select_file()

	def select_img_dir(self):
		self.img_dir=select_folder()

	def save_zip(self):
		dataset=Dataset()
		dataset.destination_dir=select_folder()
		dataset.annotation_path=self.annoation_path
		dataset.img_dir=self.img_dir
		dataset.config_path=self.config_path
		dataset.run()


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		self.train=Train()

	def build(self):
		return self.train


if __name__ == '__main__':
	test=Test().run()
