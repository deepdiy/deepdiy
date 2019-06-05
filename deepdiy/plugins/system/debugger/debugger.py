import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import glob
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
import logging,importlib,pkgutil

class Debugger(BoxLayout):
	"""docstring for Debugger."""

	data=ObjectProperty()
	debug_packages = ListProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'demo.kv')

	def __init__(self):
		super(Debugger, self).__init__()
		self.collect_debug_packages()
		self.run_debug_packages()

	def collect_debug_packages(self):
		for importer, modname, ispkg in pkgutil.walk_packages(
			path=[os.sep.join([self.bundle_dir,'plugins','system','debugger'])],
			prefix='plugins.system.debugger.',
			onerror=lambda x: None):
			if len(modname.split('.'))>4 and '__' not in modname:
				self.debug_packages.append(modname)

	def run_debug_packages(self):
		for modname in self.debug_packages:
			try:
				module=importlib.import_module(modname)
			except Exception as e:
				logging.warning('Fail to load debug script <{}>: {}'.format(modname,e))
		# pass
		# script_path_list=glob.glob(os.sep.join([
		# 	self.bundle_dir,'plugins','system','debugger','*/']))
		# module_names = ['.'.join(path.split(os.sep)[-5:-1]) for path in script_path_list]
		# module_names = [name+'.'+name.split('.')[-1] for name in module_names]
		# module_names = [name for name in module_names if name.split('.')[0] == 'plugins' and '__' not in name]
		# for name in module_names:
		# 	print(name)
		# 	try:module=importlib.import_module(name)
		# 	except Exception as e:
		# 		logging.warning('Fail to load debug script <{}>: {}'.format(name,e))



class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Debugger()
		return demo

if __name__ == '__main__':
	Test().run()
