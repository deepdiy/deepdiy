import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
import string

class WidgetManager(BoxLayout):
	"""Provide window for App and organize widgets in window

	Monitor plugins in App. If new plugin appear add the GUI(
	widgets) of the plugin into window; if a plugin is disabled, remove its
	widgets.
	This module also provide the main window and menu bar.

	Attributes:
		plugins: plugins in the App
		bundle_dir: the dir of main.py
	"""

	plugins=DictProperty(force_dispatch=True)
	bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'frame.kv')

	def __init__(self,**kwargs):
		super(WidgetManager, self).__init__(**kwargs)
		app=App.get_running_app()
		app.bind(plugins=self.setter('plugins'))
		self.bind(plugins=self.load_widgets)
		self.widget_list=[]

	def load_widgets(self,instance,value):
		for id in self.plugins:
			if self.plugins[id]['disabled']==False and id not in self.widget_list:
				self.add_widget_to_window(self.plugins[id]['instance'],self.plugins[id]['type'],id)
				self.widget_list.append(id)
		for id in self.widget_list:
			if self.plugins[id]['disabled']==True:
				self.remove_widget_from_window(self.plugins[id]['instance'],self.plugins[id]['type'],id)
				self.widget_list.remove(id)

	def add_widget_to_window(self,ins,type,id):
		if id=='resource_tree':
			self.ids.resource_tree.add_widget(ins)
		elif type=='processing':
			screen=Screen(name=id)
			screen.add_widget(ins)
			self.ids.processing_screens.add_widget(screen)
			self.add_munu_button(id)
		elif type=='display':
			screen=Screen(name=id)
			screen.add_widget(ins)
			self.ids.display_screens.add_widget(screen)

	def remove_widget_from_window(self,ins,type,id):
		if id=='resource_tree':
			self.ids.resource_tree.remove_widget(ins)
		elif type=='processing':
			screen=self.ids.processing_screens.get_screen(id)
			self.ids.processing_screens.remove_widget(screen)
			self.remove_menu_button(id)
		elif type=='display':
			screen=self.ids.display_screens.get_screen(id)
			self.ids.display_screens.remove_widget(screen)

	def add_munu_button(self,id):
		self.ids.action_view.add_widget(Factory.MenuButton(
			text=string.capwords(id.replace('_',' ')),
			on_release=lambda x:setattr(self.ids.processing_screens, 'current', id),
			important=True))

	def remove_menu_button(self,id):
		for i in self.ids.action_view.children:
			if hasattr(i,'text'):
				if i.text==string.capwords(id.replace('_',' ')):
					self.ids.action_view.remove_widget(i)


class Test(App):
	data=DictProperty()
	plugins=DictProperty()
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		return WidgetManager()

if __name__ == '__main__':
	test=Test().run()
