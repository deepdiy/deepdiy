from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty

class DisplayManager(BoxLayout):
	"""docstring for DisplayManager."""

	data=DictProperty()

	def __init__(self,**kwargs):
		super(DisplayManager, self).__init__(**kwargs)
		app=App.get_running_app()
		if app!=None:
			app.bind(data=self.setter('data'))
			self.bind(data=self.display)
			# self.bind(data=app.widget_manager.ids.resource_tree.children[0].setter('data'))
			# app.widget_manager.ids.resource_tree.children[0].bind(data=self.setter('data'))

	def display(self,*args):
		app=App.get_running_app()

		if not hasattr(self.data, 'selection'):
			return
		if not 'display' in self.data['selection']['data']:
			return
		print(self.data['selection']['data']['content'])
		app.widget_manager.ids.display_screens.current=self.data['selection']['data']['display']
		app.widget_manager.ids.display_screens.children[0].children[0].data=self.data['selection']['data']['content']

			# app.widget_manager.ids.display_screens.ids.image_viewer.data=self.data
		# if self.data['selection']['data']['type']=='file_path':
		# 	self.img=read_img(self.data['selection']['data']['content'])
		# else:
		# 	self.img=self.data['selection']['data']['content']


class Test(object):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		class_manager=DisplayManager()

if __name__ == '__main__':
	test=Test()
