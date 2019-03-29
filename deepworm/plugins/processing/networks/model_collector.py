import sys,os
sys.path.append('../../../')
import importlib
from utils.get_parent_path import get_parent_path
from utils.get_file_list import get_file_list
from plugins.processing.networks.model import Model


class ModelCollector(object):
	"""docstring for Run."""
	bundle_dir = get_parent_path(3)

	def __init__(self):
		super(ModelCollector, self).__init__()
		self.models={}
		self.scan_model_zoo()

	def scan_model_zoo(self):
		self.model_names=os.listdir(self.bundle_dir+os.sep+'model_zoo')
		self.model_names=[name for name in self.model_names if name[:2]!='__']
		for name in self.model_names:
			self.models[name]=Model()
			self.collect_model_apis(name)
			self.collect_weight_file(name)

	def collect_model_apis(self,name):
		for func in ['get_network','pre_process','post_process']:
			try:
				func_name='.'.join(['model_zoo',name,'api',func])
				module=importlib.import_module(func_name)
			except Exception as e:
				print('[Warning]',func,'not found. ',e)
			if module !=None:
				self.models[name].__setattr__(func, getattr(module,func))

	def collect_weight_file(self,name):
		weight_list=get_file_list(self.bundle_dir+os.sep+'model_zoo'+os.sep+name+os.sep+'assets')
		self.models[name].__setattr__('weight_list',weight_list)

class Test(object):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

		mc=ModelCollector()
		print(mc.models)

if __name__ == '__main__':
	test=Test()
