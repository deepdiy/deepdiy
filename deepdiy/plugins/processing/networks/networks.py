import sys,os
sys.path.append('../../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty,BooleanProperty
from plugins.processing.networks.model_collector import ModelCollector
from utils.get_parent_path import get_parent_path
from core.sandbox import Sandbox
from pebble import concurrent
import json


class Networks(BoxLayout):
	"""docstring for Run."""
	data=DictProperty()
	is_weight_loaded=BooleanProperty(False)
	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'networks.kv')


	def __init__(self):
		super(Networks, self).__init__()
		self.models=ModelCollector().models
		self.ids.model_spinner.values=self.models
		self.ids.model_spinner.bind(text=self.update_weight_list)
		self.ids.model_spinner.bind(text=self.update_config_list)

	def update_config_list(self,instance,text):
		if not hasattr(self.models[text],'config_list'):
			self.ids.config_spinner.text='Default config'
			return
		values=[item.split(os.sep)[-1] for item in self.models[text].config_list]
		if len(values)>0:
			self.ids.config_spinner.text='Select Config'
			self.ids.config_spinner.values=values
		else:
			self.ids.config_spinner.text='No config needed'
			self.ids.config_spinner.values=[]
		self.model=self.models[self.ids.model_spinner.text]
		self.is_weight_loaded=False

	def update_weight_list(self,instance,text):
		values=[item.split(os.sep)[-1] for item in self.models[text].weight_list]
		if len(values)>0:
			self.ids.weight_spinner.text='Select Weight'
			self.ids.weight_spinner.values=values
		else:
			self.ids.weight_spinner.text='No weight available'
			self.ids.weight_spinner.values=[]
		self.model=self.models[self.ids.model_spinner.text]
		self.is_weight_loaded=False

	def load_weight(self):
		import tensorflow as tf
		self.graph=tf.get_default_graph()
		self.ids.btn_load_weight.text='Loading'
		self.model.weight_path=get_parent_path(4)+os.sep+'model_zoo'+os.sep+self.ids.model_spinner.text+os.sep+'weights'+os.sep+self.ids.weight_spinner.text
		self.model.config_path=get_parent_path(4)+os.sep+'model_zoo'+os.sep+self.ids.model_spinner.text+os.sep+'configs'+os.sep+self.ids.config_spinner.text
		test=self.load()

	@concurrent.thread
	def load(self):
		with self.graph.as_default():
			self.model.load_network()
			self.model.load_weight()
			self.is_weight_loaded=True
			self.ids.btn_load_weight.text='Load Model'


	def run(self):
		if self.data['selection']['data']['type']!='file_path':
			return
		self.ids.btn_run.text='Running'
		self.model.set_input(self.data['selection']['data']['content'])
		self.config=json.load(open(self.model.config_path))
		self.sandbox=Sandbox(
			self.data,
			use_selected_data=False,
			graph=self.graph,
			func=self.model.predict,
			kwargs={},
			call_back=self.on_finished,
			result_meta={
				'node_id':'mask',
				'type':'img',
				'display':'detection_viewer',
				'class_names':self.config['CLASS_NAMES']
				}
			)
		with self.graph.as_default():
			self.sandbox.start()

	def on_finished(self):
		self.ids.btn_run.text='Run'

class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		self.networks=Networks()
		self.networks.data={
			'tree':{'children':[]},
			'selection':{'index_chain':[],'data':{'type':'file_path',
			'content':'../../../img/face.jpg',
			'display':'image_viewer',
			'children':[]}}}

	def build(self):
		return self.networks


if __name__ == '__main__':
	test=Test().run()
