import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty

# class Item(BoxLayout):
# 	title=StringProperty()
# 	value=ObjectProperty()
#
# 	def __init__(self,config):
# 		super(Item, self).__init__()
# 		self.config=config
# 		self.title=self.config['id']
# 		self.insert_widget()
# 		self.sync_value()
#
# 	def insert_widget(self):
# 		widget_type=self.config['type'].replace('_',' ').title().replace(' ','')
# 		self.widget=getattr(Factory,widget_type)()
# 		self.ids.widget.add_widget(self.widget)
# 		for i in self.config:
# 			setattr(self.widget,i,self.config[i])
#
# 	def sync_value(self):
# 		if hasattr(self.widget,'value'):
# 			self.value=self.widget.value
# 			self.widget.bind(value=self.setter('value'))
# 		elif hasattr(self.widget,'text'):
# 			self.value=self.widget.text
# 			self.widget.bind(text=self.setter('value'))


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
		mapping={'spinner':Spinner,
		'slider':Slider,
		'text_input':TextInput}
		for item in self.form:
			self.add_widget(Label(text=item['id'],size_hint_y=None,height='30dp'))
			wid=mapping[item['type']]()
			for i in item:
				if i!='type':
					wid.setter(str(i))('',item[i])
				wid.size_hint_y=None
				wid.height='40dp'
			self.add_widget(wid)
			self.add_widget(BoxLayout(size_hint_y=None,height='15dp'))
			self.ids = {child.id:child for child in self.children}
			self.add_binding(item['id'])

	# def parse(self,*args):
	# 	for i in self.form:
	# 		self.add_widget(Item(i))

	def reset(self,*ars):
		self.clear_widgets()
		self.parse()

	def export(self,*args):
		data={item['id']:getattr(self,item['id']) for item in self.form}

		print(data)

	def add_binding(self,id):
		self.__setattr__(id,None)
		if hasattr(self.ids[id],'value'):
			self.__setattr__(id,self.ids[id].value)
			self.ids[id].bind(value=lambda instance,value:self.__setattr__(id,value))
		elif hasattr(self.ids[id],'text'):
			self.__setattr__(id,self.ids[id].text)
			self.ids[id].bind(text=lambda instance,value:self.__setattr__(id,value))


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

		root.add_widget(Button(text='reset',size_hint_x=None,width='100dp',on_release=form_parser.reset))
		root.add_widget(Button(text='export',size_hint_x=None,width='100dp',on_release=form_parser.export))
		# wid=BoxLayout(orientation='vertical')
		# wid.add_widget(Item('hi'))
		# wid.add_widget(Item('hi'))
		# wid.add_widget(Item('hi'))
		# wid.add_widget(Item('hi'))
		# return wid
		return root


if __name__ == '__main__':
	test=Test().run()
