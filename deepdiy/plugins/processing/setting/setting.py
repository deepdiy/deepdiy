import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class Setting(BoxLayout):
	"""docstring for Setting."""

	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
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
