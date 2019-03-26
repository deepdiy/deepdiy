import sys,os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty
from kivy.factory import Factory
import string



class Run(BoxLayout):
	"""docstring for Run."""
	data=DictProperty()
	bundle_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'run.kv')


	def __init__(self):
		super(Run, self).__init__()
		self.scan_model_zoo()

	def scan_model_zoo(self):
		self.model_lst=os.listdir(self.bundle_dir+os.sep+'model_zoo')
		for id in self.model_lst:
			name=string.capwords(id.replace('_',' '))
			self.ids.dropdown.add_widget(Factory.Button(
				text=name,
				id=id,
				on_release=lambda x:self.ids.dropdown.select(x.id),
				size_hint_y=None,
				height='50dp'))



class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		return Run()


if __name__ == '__main__':
	test=Test().run()
