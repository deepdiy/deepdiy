import sys,os
sys.path.append('../../')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from utils.get_parent_path import get_parent_path

class Setting(BoxLayout):
	"""docstring for Setting."""

	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'setting.kv')
	def __init__(self):
		super(Setting, self).__init__()

class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		return Setting()


if __name__ == '__main__':
	test=Test().run()
