import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import json
import webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import DictProperty,StringProperty,ListProperty
from plugins.processing.train.dataset import Dataset
from utils.select_path_dialog import select_file,select_folder
from utils.form_parser import FormParser
from utils.get_file_list import get_file_list
from middleware.widget_handler import WidgetHandler

class Train(BoxLayout):
	"""Train a deep learning model with own data

	Because this module rely on models from Model Zoo, so it is designed as
	opening in a passive manner. To be specific, at start the GUI will guide
	user to select a model in Model Zoo module, only after deep learning model
	is selected, this module will shift to work mode.

	Attributes:
		model_id: id of model, used to find and load configuration of the model
		train_notebooks: list of notebook pathes. Each model may have one or
		 	more notebooks for training different kind of data.
		bundle_dir: the dir of main.py

	"""
	model_id = StringProperty()
	train_notebooks = ListProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'train.kv')

	def __init__(self):
		super(Train, self).__init__()
		self.bind(model_id=self.switch_screens)
		self.bind(model_id=self.show_config)
		self.bind(model_id=self.collect_train_notebooks)

	def switch_screens(self,*args):
		self.ids.screens.current='work'

	def jump_to_model_zoo(self,*args):
		widget_handler=WidgetHandler()
		widget_handler.switch_screens('processing','model_zoo')

	def show_config(self,instance,text):
		self.ids.config_panel.clear_widgets()
		path=os.sep.join([self.bundle_dir,'model_zoo',text,'config_form.json'])
		if not os.path.exists(path):
			self.ids.config_panel.add_widget(Label(text='This network do not need configuration'))
			return
		self.form_parser=FormParser()
		self.form_parser.load_json(path)
		self.ids.config_panel.add_widget(self.form_parser)

	def collect_train_notebooks(self,*args):
		self.train_notebooks=get_file_list(os.sep.join([
			self.bundle_dir,'plugins','processing','model_zoo','models',self.model_id,'training']),formats=['ipynb'])

	def open_via(self):
		webbrowser.open('http://www.robots.ox.ac.uk/~vgg/software/via/via-2.0.4.html')

	def train(self):
		webbrowser.open('https://colab.research.google.com/github/deepdiy/deepdiy/blob/master/deepdiy/model_zoo/'+self.model_id+'/training/'+self.ids.run_notebook_spinner.text)

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
		self.train.model_id = 'mrcnn'

	def build(self):
		return self.train


if __name__ == '__main__':
	test=Test().run()
