import os,rootpath
rootpath.append(pattern='plugins')
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout

class Demo(BoxLayout):
	"""docstring for Demo."""

	bundle_dir = rootpath.detect(pattern='plugins')
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'gallery.kv')
	data=DictProperty()
	def __init__(self):
		super(Demo, self).__init__()


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Demo()
		return demo

if __name__ == '__main__':
	Test().run()
