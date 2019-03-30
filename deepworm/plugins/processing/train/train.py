import sys,os
sys.path.append('../../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from utils.get_parent_path import get_parent_path
import webbrowser


class Train(BoxLayout):
	"""docstring for Train."""
	data=DictProperty()
	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'train.kv')

	def __init__(self):
		super(Train, self).__init__()

	def label(self):
		print('hi')
		webbrowser.open(self.bundle_dir+os.sep+'via'+os.sep+'via.html')




class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		self.train=Train()

	def build(self):
		return self.train


if __name__ == '__main__':
	test=Test().run()
