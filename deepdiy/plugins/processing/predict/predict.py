import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import importlib
from pebble.concurrent import thread
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty,DictProperty,BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from utils.get_file_list import get_file_list
from utils.quickplugin import QuickPlugin


class Predict(BoxLayout):
	"""Make prediction/inference with deep learning models

	Because this module rely on models from Model Zoo, so it is designed as
	opening in a passive manner. To be specific, at start the gui will guide
	user to select a model in Model Zoo module, only after deep learning model
	is selected, this module will shift to work mode.

	Attribues:
		data: shared and synchornized within the App.
			This module will use user selected item in data as input and make
			prediction. The result will be saved as a child of selected item.
		model: deep learning model which will be used to make prediction
		model_id: id of model, used to find and load model
		config_id: id of user-selected config file, used to find and load
			config file. The config file stores the configurations of model,
			such as input shape of network. Some model may not need config file.
		weight_id: id of user-selected weight file.
		config_dict: a dictionary stores pairs of id and path of all config
			files available in the selected model.
		weight_dict: a dictionary stores pairs fo id and path of all weight
			files available in the selected model.
		is_weight_loaded: True when weight is loaded. If False, the Run button
			is disabled
		bundle_dir: the dir of main.py
	"""

	data=ObjectProperty()
	model=ObjectProperty()
	model_id=StringProperty()
	config_id=StringProperty()
	weight_id=StringProperty()
	config_dict=DictProperty()
	weight_dict=DictProperty()
	is_weight_loaded=BooleanProperty(False)
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'predict.kv')

	def __init__(self):
		super(Predict, self).__init__()
		self.bind(model_id=self.import_model)
		self.bind(model=self.collect_configs)
		self.bind(model=self.collect_weights)
		self.bind(model=self.switch_screens)

	def import_model(self,*args):
		module_name='.'.join(['model_zoo',self.model_id,'api'])
		module=importlib.import_module(module_name)
		self.model=getattr(module,'Api')()

	def switch_screens(self,*args):
		self.ids.screens.current='work'

	def collect_configs(self,*args):
		config_list=get_file_list(os.sep.join([self.bundle_dir,'plugins','processing','model_zoo','configs',self.model_id]))
		self.config_dict={i.split(os.sep)[-1]:i for i in config_list}

	def collect_weights(self,*args):
		weight_list=get_file_list(os.sep.join([self.bundle_dir,'plugins','processing','model_zoo','weights',self.model_id]))
		self.weight_dict={i.split(os.sep)[-1]:i for i in weight_list}

	def load_weight(self):
		import tensorflow as tf
		self.graph=tf.get_default_graph()
		self.ids.btn_load_weight.text='Loading'
		model_zoo_path=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo'])
		self.model.weight_path=os.sep.join([model_zoo_path,'weights',self.model_id,self.ids.weight_spinner.text])
		if self.ids.config_spinner.text!='No config needed':
			self.model.config_path=os.sep.join([model_zoo_path,'configs',self.model_id,self.ids.config_spinner.text])
		else:
			self.model.config_path=''
		self.load()

	@thread
	def load(self):
		if self.model.config_path!='':
			self.config=json.load(open(self.model.config_path))
		else:
			self.config={'CLASS_NAMES':['background','target']}
		with self.graph.as_default():
			self.model.load_network()
			self.model.load_weight()
			self.is_weight_loaded=True
			self.ids.btn_load_weight.text='Load Model'

	def predict(self,selected_data):
		self.model.set_input(selected_data)
		return self.model.predict()

	def run(self):
		self.ids.btn_run.text='Running'
		quickplugin=QuickPlugin(data=self.data,
			input_type=['file_path'],
			result_meta={'node_id':'detection_result',
				'type':'img',
				'display':'detection_viewer',
				'class_names':self.config['CLASS_NAMES']
				},
			call_back=self.on_finished,
			tensorflow_graph=self.graph)
		quickplugin.run=self.predict
		quickplugin.start()

	def on_finished(self):
		self.property('data').dispatch(self)
		self.ids.btn_run.text='Run'


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Predict()
		demo.model_id = 'mrcnn'
		demo.data = lambda:None
		demo.data.get_selected_data=lambda:{
			'type':'file_path',
			'content':'../../../img/face.jpg',
			'display':'image_viewer',
			'children':[]}
		return demo

if __name__ == '__main__':
	Test().run()
