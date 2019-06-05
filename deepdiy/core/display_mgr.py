import sys,os
sys.path.append('../')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,BooleanProperty
from kivy.logger import Logger
from kivy.clock import Clock


class DisplayManager(BoxLayout):
	"""Monitor data changes and update contents in widgets

	When data changes, refresh the resource_tree and monitor the change of
	selected item index in the resource_tree, when the select index changes,
	update the content in display_panel.

	Attributes:
		data: Data() object in App
	"""
	data=ObjectProperty(force_dispatch=True)

	def __init__(self,**kwargs):
		super(DisplayManager, self).__init__(**kwargs)
		self.app=App.get_running_app()
		self.data=self.app.data
		self.app.bind(data=self.setter('data'))
		self.bind(data=lambda x,y:Clock.schedule_once(self.on_data_changed))
		self.data.bind(select_idx=lambda x,y:Clock.schedule_once(self.update_display_panel))

	def on_data_changed(self,*args):
		self.update_display_panel()
		if hasattr(self.app.plugins,'resource_tree'): # prevent no resource_tree
			self.update_resource_tree()

	def update_resource_tree(self,*args):
		'''Catch the instance of  ResourceTree plugin, give it new data,
		and tell it to update'''
		resource_tree=self.app.plugins['resource_tree']['instance']
		resource_tree.data=self.data
		resource_tree.property('data').dispatch(resource_tree)
		Logger.debug('Display Manager: Update Resource Tree')

	def update_display_panel(self,*args):
		'''Switch to corresponding display screen, give the viewer selected data'''
		selected_data=self.data.get_selected_data()
		if 'display' in selected_data: # some data may not have display property
			display_panel=self.app.widget_manager.ids.display_screens
			display_panel.current=selected_data['display']
			display_panel.children[0].children[0].data=selected_data
			Logger.debug('Display Manager: show {} in {}'.format(selected_data['node_id'],selected_data['display']))


class Test(App):
	from core.data_mgr import Data
	data=ObjectProperty(Data())
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		return DisplayManager()

if __name__ == '__main__':
	Test().run()
