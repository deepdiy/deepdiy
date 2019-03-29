import sys,os
sys.path.append('../../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty
from kivy.factory import Factory
from plugins.processing.networks.model_collector import ModelCollector
from utils.get_parent_path import get_parent_path
import string
from kivy.uix.spinner import Spinner


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
		self.ids.weight_spinner.bind(text=self.active_run)

	def update_weight_list(self,instance,text):
		values=[item.split(os.sep)[-1] for item in self.models[text].weight_list]
		if len(values)>0:
			self.ids.weight_spinner.disabled=False
			self.ids.btn_test_load_model.disabled=False
			self.ids.btn_test_pre_processing.disabled=False
			self.ids.btn_test_post_processing.disabled=False
			self.ids.weight_spinner.text='Select Weight'
			self.ids.weight_spinner.values=values
		else:
			self.ids.weight_spinner.text='No weight available'
			self.ids.weight_spinner.values=[]

	def test_load_model(self):
		self.model=self.models[self.ids.model_spinner.text]
		self.model.network=self.model.load_model()

	def active_run(self,*args):
		if self.ids.weight_spinner.disabled==False and self.ids.weight_spinner.text not in ['Select Weight','No weight available']:
			self.ids.btn_run.disabled=False
		else:
			self.ids.btn_run.disabled=True

	def run(self):
		
		self.model.network=self.model.run('../../../img/face.jpg')

class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		return Networks()


if __name__ == '__main__':
	test=Test().run()
