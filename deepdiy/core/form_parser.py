import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,ListProperty,StringProperty

class Item(BoxLayout):
	title=StringProperty()
	value=ObjectProperty()

	def __init__(self,config):
		super(Item, self).__init__()
		self.config=config
		self.title=self.config['id']
		self.insert_widget()
		self.sync_value()

	def insert_widget(self):
		widget_type=self.config['type'].replace('_',' ').title().replace(' ','')
		self.widget=getattr(Factory,widget_type)()
		self.ids.widget.add_widget(self.widget)
		for i in self.config:
			setattr(self.widget,i,self.config[i])

	def sync_value(self):
		if hasattr(self.widget,'value'):
			self.value=self.widget.value
			self.widget.bind(value=self.setter('value'))
		elif hasattr(self.widget,'text'):
			self.value=self.widget.text
			self.widget.bind(text=self.setter('value'))

class FormParser(BoxLayout):
	"""docstring for FormParser."""
	form=ListProperty()
	bundle_dir = get_parent_path(3)
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'form_parser.kv')

	def __init__(self,**kw):
		super(FormParser, self).__init__(**kw)
		self.bind(form=self.parse)

	def load_json(self,json_path):
		with open(json_path) as f:
			self.form=json.load(f)

	def parse(self,*args):
		for i in self.form:
			self.add_widget(Item(i))

	def reset(self,*ars):
		self.clear_widgets()
		self.parse()

	def export(self,*args):
		data={item.title:item.value for item in reversed(self.children)}
		print(data)


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
		form_parser.load_json('../../model_zoo/mrcnn/config_form.json')

		from kivy.uix.button import Button
		root.add_widget(Button(text='reset',size_hint_x=None,width='100dp',on_release=form_parser.reset))
		root.add_widget(Button(text='export',size_hint_x=None,width='100dp',on_release=form_parser.export))
		
		return root


if __name__ == '__main__':
	test=Test().run()
