import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path
from core.form_parser import FormParser

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,ObjectProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout

class QuickPlugin(BoxLayout):
	"""docstring for QuickPlugin."""

	data=ObjectProperty(lambda: None)
	input_type=StringProperty()
	output_type=StringProperty()
	display=StringProperty()
	kwargs=DictProperty()

	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'quickplugin.kv')

	def __init__(self):
		super(QuickPlugin, self).__init__()

	def run(self):
		pass


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=QuickPlugin()
		demo.kwargs={
			'foo':100,'bar':'[1,2,3]'
		}
		return demo

if __name__ == '__main__':
	Test().run()
