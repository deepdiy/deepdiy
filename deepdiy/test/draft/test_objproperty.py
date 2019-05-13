import os,rootpath
rootpath.append(pattern='plugins')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
from kivy.uix.button import Button

class Data(EventDispatcher):
	"""docstring for Data."""

	def __init__(self):
		super(Data, self).__init__()


class Demo(BoxLayout):
	"""docstring for Demo."""

	bundle_dir = rootpath.detect(pattern='plugins')
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'gallery.kv')
	data=ObjectProperty(force_dispatch=True)
	def __init__(self):
		super(Demo, self).__init__()
		self.data=Data()
		self.data.room=0
		self.bind(data=lambda x,y:print(self.data.room))
		self.data.room='hi'
		self.data=self.data
		self.data.room=1
		self.property('data').dispatch(self)

class Window(BoxLayout):
	"""docstring for Window."""

	foo=ObjectProperty(force_dispatch=True)
	def __init__(self):
		super(Window, self).__init__()
		self.demo=Demo()
		self.demo.bind(data=self.setter('foo'))
		self.demo.property('data').dispatch(self.demo)
		self.add_widget(Button(text='pp',on_release=self.update))
		self.bind(foo=lambda x,y:print(self.foo))

	def update(self,*args):
		print(self.foo.room)
		self.demo.data.room+=1
		# self.foo.room='202'


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		window=Window()
		return window

if __name__ == '__main__':
	Test().run()
