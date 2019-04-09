import sys,os
sys.path.append('../')
import threading
from kivy.event import EventDispatcher
from kivy.properties import DictProperty
from pebble import concurrent
from utils.add_data_to_tree import add_data_to_tree
from time import time

class Sandbox(EventDispatcher):
	"""docstring for ."""

	def __init__(self, data, func, kwargs,result_meta=None,call_back=None,use_selected_data=True,graph=None):
		super(Sandbox, self).__init__()

		self.data = data
		self.kwargs = kwargs
		self.result_meta=result_meta
		self.use_selected_data=use_selected_data
		self.graph=graph

		if func is not None:
			self.func = func
		else:
			self.func = lambda: None

		if call_back is not None:
			self.call_back = call_back
		else:
			self.call_back = lambda: None

	@concurrent.thread
	def run(self):
		if not self.graph is None:
			with self.graph.as_default():
				if self.use_selected_data:
					input=self.data['selection']['data']['content']
					result=self.func(input,**self.kwargs)
				else:
					result=self.func(**self.kwargs)
		else:
			if self.use_selected_data:
				input=self.data['selection']['data']['content']
				result=self.func(input,**self.kwargs)
			else:
				result=self.func(**self.kwargs)
		return result

	def on_finished(self,job):
		result=job.result()
		output=self.result_meta
		output['children']=[]
		output['content']=result
		add_data_to_tree(self.data['tree'],output,self.data['selection']['index_chain'])
		self.data['selection']={'data':output,'index_chain':self.data['selection']['index_chain'].append(-1)}
		self.data['last_job_time']={'time':time()}
		self.call_back()

	def start(self):
		result=self.run()
		result.add_done_callback(self.on_finished)


def test():
	def plus(data,kw1,kw2):
		return data+kw1+kw2
	def call_back():
		print('I am call_back')
	sandbox=Sandbox(
		data={'tree':{'children':[]},'selection':{'data':{'content':4},'index_chain':[]}},
		kwargs={'kw1':1,'kw2':2},
		func=plus,
		result_meta={
			'node_id':'mask',
			'type':'img',
			'display':'image_viewer'},
		call_back=call_back)
	sandbox.start()
	print(sandbox.data)

if __name__ == '__main__':
	test()
