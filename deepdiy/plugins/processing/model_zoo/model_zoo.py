import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH 
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout
from plugins.processing.model_zoo.online_models import OnlineModels
from plugins.processing.model_zoo.local_models import LocalModels
from plugins.processing.model_zoo.local_demos import LocalDemos

class ModelZoo(BoxLayout):
	"""docstring for ModelZoo."""

	data=ObjectProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'model_zoo.kv')

	def __init__(self):
		super(ModelZoo, self).__init__()
		self.local_models=LocalModels()
		self.local_demos=LocalDemos()
		self.ids.local_model_container.add_widget(self.local_models)
		self.ids.local_demo_container.add_widget(self.local_demos)

	def load_online_models(self,*args):
		self.online_models=OnlineModels()
		self.online_models.open()


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=ModelZoo()
		return demo


if __name__ == '__main__':
	Test().run()
