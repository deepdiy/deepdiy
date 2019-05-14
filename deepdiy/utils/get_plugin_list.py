import os,rootpath
rootpath.append(pattern='plugins')
from core.plugin_mgr import PluginManager
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout

class Demo(BoxLayout):
	"""docstring for Demo."""

	data=DictProperty()
	bundle_dir = rootpath.detect(pattern='plugins')
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'gallery.kv')

	def __init__(self):
		super(Demo, self).__init__()
		self.plugin_mgr=PluginManager()
		self.plugin_mgr.load_plugins()
		print(*self.plugin_mgr.plugins.items(),sep='\n')
		# print(self.plugin_mgr.plugins)


class Test(App):
	"""docstring for Test."""

	data=DictProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Demo()
		return demo

if __name__ == '__main__':
	Test().run()
