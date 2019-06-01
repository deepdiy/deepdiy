import sys,os
sys.path.append('../')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class DisplayManager(BoxLayout):
	"""docstring for DisplayManager."""

	data=ObjectProperty(force_dispatch=True)

	def __init__(self,**kwargs):
		super(DisplayManager, self).__init__(**kwargs)
		self.app=App.get_running_app()
		self.app.bind(data=self.setter('data'))
		self.bind(data=self.on_data_changed)

	def on_data_changed(self,*args):
		if hasattr(self.app.plugins,'resource_tree'):
			self.update_resource_tree()
		if hasattr(self.data,'select_idx'):
			self.data.bind(select_idx=self.update_display_panel)

	def update_resource_tree(self,*args):
		'''Catch the instance of  ResourceTree plugin, give it new data,
		and tell it to update'''
		resource_tree=self.app.plugins['resource_tree']['instance']
		resource_tree.data=self.data
		resource_tree.property('data').dispatch(resource_tree)

	def update_display_panel(self,*args):
		selected_data=self.data.get_selected_data()
		if 'display' in selected_data: # some data may not have display property
			display_panel=self.app.widget_manager.ids.display_screens
			display_panel.current=selected_data['display']
			display_panel.children[0].children[0].data=selected_data


class Test(App):
	data=ObjectProperty()
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		return DisplayManager()

if __name__ == '__main__':
	Test().run()
