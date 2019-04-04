from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty

class DisplayManager(BoxLayout):
	"""docstring for DisplayManager."""

	data=DictProperty({})

	def __init__(self,**kwargs):
		super(DisplayManager, self).__init__(**kwargs)
		app=App.get_running_app()
		if app!=None:
			app.bind(data=self.setter('data'))
			self.bind(data=self.display)

	def display(self,*args):
		if not hasattr(self.data,'selection'):
			return


class Test(object):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		class_manager=DisplayManager()

if __name__ == '__main__':
	test=Test()
