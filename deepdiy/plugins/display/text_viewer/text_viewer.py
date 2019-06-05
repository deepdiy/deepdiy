import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import pprint
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.logger import Logger

class TextViewer(BoxLayout):
	"""docstring for TextViewer."""

	data=DictProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'demo.kv')

	def __init__(self):
		super(TextViewer, self).__init__()
		self.text_input=TextInput(id='text_area',readonly=True)
		self.add_widget(self.text_input)
		self.bind(data=self.refresh)

	def refresh(self,*args):
		self.text_input.text = pprint.pformat(self.data)


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=TextViewer()
		tup = ('spam', ('eggs', ('lumberjack', ('knights', ('ni', ('dead',('parrot', ('fresh fruit',))))))))
		demo.data={'type':'img','content':'abcdefg','children': ['a' * 10, tup, ['a' * 30, 'b' * 30], ['c' * 20, 'd' * 20]]}
		return demo

if __name__ == '__main__':
	Test().run()
