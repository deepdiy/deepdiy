import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
import string

class WidgetManager(BoxLayout):
	"""docstring for WidgetManager."""

	plugins=DictProperty({})
	bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'frame.kv')

	def __init__(self,**kwargs):
		super(WidgetManager, self).__init__(**kwargs)
		app=App.get_running_app()
		if app!=None:
			app.bind(plugins=self.setter('plugins'))
			self.bind(plugins=self.load_widgets)

	def load_widgets(self,instance,value):
		if not hasattr(self.plugins,'instances'):
			return
		for ins in self.plugins.instances:
			self.add_widget_to_window(ins,ins['type'],ins['id'])

	def add_widget_to_window(self,ins,type,id):
		print(id)
		if id=='resource_tree':
			self.ids.resource_tree.add_widget(ins['obj'])
		elif type=='processing':
			screen=Screen(name=id)
			screen.add_widget(ins['obj'])
			self.ids.processing_screens.add_widget(screen)
			self.add_munu_button(id)
		elif type=='display':
			screen=Screen(name=id)
			screen.add_widget(ins['obj'])
			self.ids.display_screens.add_widget(screen)

	def add_munu_button(self,id):
		# if id in ['open','models','plugins','scripts','train']:
		self.ids.action_view.add_widget(Factory.MenuButton(
			text=string.capwords(id.replace('_',' ')),
			on_release=lambda x:setattr(self.ids.processing_screens, 'current', id),
			important=True))
		# elif id in ['detect','segment']:
		# 	self.ids.menu_btn_group.add_widget(Factory.MenuButton(text=string.capwords(id.replace('_',' '))))


class Test(App):
	data=DictProperty()
	plugins=DictProperty()
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)


	def build(self):
		return WidgetManager()

if __name__ == '__main__':
	test=Test().run()
