import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty


class FormParser(BoxLayout):
	"""docstring for FormParser."""
	bundle_dir = get_parent_path(3)
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'form.kv')
	form=ListProperty()

	def __init__(self,**kw):
		super(FormParser, self).__init__(**kw)
		self.parse_tools={
			'spinner':self.add_spinner,
			'slider':self.add_slider,
			'text_input':self.add_text_input,
			'path':self.add_path_selector}
		self.bind(form=self.parse)
		self.bind(on_resize = self.alert)
		self.spin='a'
		self.orientation='vertical'
		self.size_hint_y=None
		self.padding=[20,20,20,20]

	def alert(self,*args):
		print(args)

	def parse(self,*args):
		for i in self.form:
			self.parse_tools[i['type']](i)

	def alert(self,*arg):
		print(self.height)

	def add_spinner(self,config):
		# widget=BoxLayout(size_hint_y=None,height='48dp',orientation='vertical')
		self.add_widget(Label(text=config['id'],size_hint_y=None,height='30dp'))
		self.add_widget(Spinner(
			id=config['id'],
			text=config['text'],
			size_hint_y=None,
			height='40dp',
			values=config['values']))
		self.add_widget(BoxLayout(size_hint_y=None,height='15dp'))
		# self.add_widget(widget)
		self.add_binding(config['id'])

	def add_slider(self,config):
		# widget=BoxLayout(size_hint_y=None,height='48dp',orientation='vertical')
		self.add_widget(Label(text=config['id'],size_hint_y=None,height='30dp'))
		self.add_widget(Slider(
			id=config['id'],
			min=config['min'],
			max=config['max'],
			value=config['value'],
			size_hint_y=None,
			height='30dp'))
		self.add_widget(BoxLayout(size_hint_y=None,height='15dp'))
		# self.add_widget(widget)
		# self.add_binding(config['id'])

	def add_text_input(self,config):
		# widget=BoxLayout(size_hint_y=None,height='96dp',orientation='vertical')
		self.add_widget(Label(text=config['id'],size_hint_y=None,height='30dp'))
		self.add_widget(TextInput(
			id=config['id'],
			text=config['text'],
			size_hint_y=None,
			height='30dp',
			multiline=False,
		))
		self.add_widget(BoxLayout(size_hint_y=None,height='15dp'))
		# self.add_widget(widget)
		self.add_binding(config['id'])

	def add_binding(self,id):

		if not hasattr(self,id):
			self.__setattr__(id,None)
		# self.ids[id].bind(text=lambda instance,value:self.__setattr__(id,value))

	def add_path_selector(self):
		pass


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		root=BoxLayout()
		window=ScrollView(scroll_type=["bars"],  bar_width=20)
		root.add_widget(window)
		form_parser=FormParser()
		window.add_widget(form_parser)
		form_parser.form=[
			{
				'id':'spin1',
				'type':'spinner',
				'text':'foo',
				'values':['a','b','c']
			},{
				'id':'slider1',
				'type':'slider',
				'min':1,
				'max':100,
				'value':20
			},{
				'id':'text1',
				'type':'text_input',
				'text':'Please input a text'
			}
		]
		return root


if __name__ == '__main__':
	test=Test().run()
