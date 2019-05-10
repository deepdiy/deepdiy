import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path
from core.form_parser import FormParser

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,ObjectProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
from pebble import concurrent

class QuickPlugin(BoxLayout):
	"""docstring for QuickPlugin."""

	data=ObjectProperty(lambda: None)
	input_type=ListProperty()
	kwargs=ListProperty()
	result_meta=DictProperty()

	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'quickplugin.kv')

	def __init__(self,data=lambda:None,input_type=[],result_meta={},kwargs=[],call_back=lambda:None,tensorflow_graph=None):
		super(QuickPlugin, self).__init__()
		self.parse_form()
		self.bind(kwargs=self.parse_form)
		self.data=data
		self.input_type=input_type
		self.kwargs=kwargs
		self.result_meta=result_meta
		self.call_back=call_back
		self.tensorflow_graph=tensorflow_graph

	def parse_form(self,*args):
		self.form_parser=FormParser()
		self.form_parser.form=self.kwargs
		self.add_widget(self.form_parser)

	def start(self):
		kwargs=self.form_parser.get_form_data()
		self.selected_data=self.data.get_selected_data()
		if self.selected_data['type'] in self.input_type:
			task=self.run_in_thread(self.selected_data['content'],**kwargs)
			task.add_done_callback(self.on_task_finished)

	@concurrent.thread
	def run_in_thread(self,input_data,**kwargs):
		if not self.tensorflow_graph is None:
			with self.tensorflow_graph.as_default():
				result=self.run(input_data,**kwargs)
		else:
			result=self.run(input_data,**kwargs)
		return result

	def run(self,input_data=None,**kwargs):
		pass
		return True

	def on_task_finished(self,task):
		output=self.result_meta
		output['children']=[]
		output['content']=task.result()
		self.selected_data['children'].append(output)
		self.property('data').dispatch(self)
		self.call_back()


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		from data_mgr import Data
		demo=QuickPlugin()
		demo.data=Data()
		demo.data.tree={
			'node_id':'root',
			'type':'file_path',
			'content':'../img/face.jpg',
			'display':'image_viewer',
			'children':[]}
		demo.input_type=['file_path']
		demo.output_type='img'
		demo.display='image_viewer'
		demo.kwargs=[{
			'id':'threashold',
			'type':'text_input',
			'text':'w'
		}]

		return demo

if __name__ == '__main__':
	Test().run()
