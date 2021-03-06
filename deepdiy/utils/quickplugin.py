import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from pebble import concurrent
import copy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,ObjectProperty,ListProperty,NumericProperty
from kivy.uix.boxlayout import BoxLayout
from utils.form_parser import FormParser
from core.data_mgr import Data
from middleware.widget_handler import WidgetHandler

class QuickPlugin(BoxLayout):
	"""docstring for QuickPlugin."""

	data=ObjectProperty()
	kwargs=ListProperty()
	progress_percent=DictProperty()

	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	try:Builder.unload_file(os.sep.join([bundle_dir,'ui','quickplugin.kv']))
	except:pass
	Builder.load_file(os.sep.join([bundle_dir,'ui','quickplugin.kv']))

	def __init__(self,data=Data(),input_type=[],result_meta={},kwargs=[],call_back=lambda:None,tensorflow_graph=None):
		super(QuickPlugin, self).__init__()
		self.bind(kwargs=self.parse_form)
		self.parse_form()
		self.data=data
		self.input_type=input_type
		self.kwargs=kwargs
		self.result_meta=result_meta
		self.call_back=call_back
		self.tensorflow_graph=tensorflow_graph
		self.widget_handler=WidgetHandler()
		self.bind(progress_percent=self.on_progess)

	def parse_form(self,*args):
		self.ids.form.clear_widgets()
		self.form_parser=FormParser()
		self.form_parser.form=self.kwargs
		self.ids.form.add_widget(self.form_parser)

	def start(self):
		kwargs=self.form_parser.get_form_data()
		self.selected_data=self.data.get_selected_data()
		if self.selected_data['type'] in self.input_type:
			task=self.run_in_thread(self.selected_data['content'],**kwargs)
			task.add_done_callback(self.on_task_finished)

	def on_progess(self,*args):
		self.widget_handler.set_progress_bar(self.progress_percent['value'])

	@concurrent.thread
	def run_in_thread(self,input_data,**kwargs):
		if not self.tensorflow_graph is None:
			with self.tensorflow_graph.as_default():
				result=self.run(input_data,**kwargs)
		else:
			result=self.run(input_data,**kwargs)
		return result

	def run(self,input_data=None,**kwargs):
		print('running')

		pass
		return True

	def on_task_finished(self,task):
		output=copy.deepcopy(self.result_meta)
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
		demo=QuickPlugin()
		demo.data.load_sample_data()
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
