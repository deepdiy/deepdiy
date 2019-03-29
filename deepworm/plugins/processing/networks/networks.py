import sys,os
sys.path.append('../../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.factory import Factory
from plugins.processing.networks.model_collector import ModelCollector
from utils.get_parent_path import get_parent_path
from utils.add_data_to_tree import add_data_to_tree
import string
import threading
from pebble import concurrent

class Networks(BoxLayout):
	"""docstring for Run."""
	data=DictProperty()
	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'networks.kv')

	def __init__(self):
		super(Networks, self).__init__()
		self.models=ModelCollector().models
		self.ids.model_spinner.values=self.models
		self.ids.model_spinner.bind(text=self.update_weight_list)
		threading.Thread(target=self.import_tf).start()
		# self.bind(data=self.update)

	def import_tf(self):
		import tensorflow as tf

	def update_weight_list(self,instance,text):
		values=[item.split(os.sep)[-1] for item in self.models[text].weight_list]
		if len(values)>0:
			self.ids.weight_spinner.text='Select Weight'
			self.ids.weight_spinner.values=values
		else:
			self.ids.weight_spinner.text='No weight available'
			self.ids.weight_spinner.values=[]
		self.model=self.models[self.ids.model_spinner.text]

	def run(self,path):
		weight_index=self.ids.weight_spinner.values.index(self.ids.weight_spinner.text)
		output=self.model.run(path,weight_index)
		return output

	@concurrent.thread
	def update(self):
		path=self.data['selection']['data']['content']
		result=self.run(path)
		result={
			'node_id':'mask',
			'type':'img',
			'content':result,
			'display':'image_viewer',
			'children':[]}
		data=self.data
		add_data_to_tree(data['tree'],result,data['selection']['index_chain'])
		self.data={}
		self.data=data

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
