import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH 
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout

class Demo(BoxLayout):
	"""docstring for Demo."""

	data=ObjectProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'demo.kv')

	def __init__(self):
		super(Demo, self).__init__()


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Demo()
		return demo

if __name__ == '__main__':
	Test().run()
