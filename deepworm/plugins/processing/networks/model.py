import sys,os
sys.path.append('../../../')
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
import functools
import threading
from utils.thread_handler import ThreadHandler
from kivy.clock import Clock

class Model(EventDispatcher):
	input=ObjectProperty()
	pre_process=ObjectProperty()
	out=ObjectProperty()

	def __init__(self,**kwargs):
		super(Model, self).__init__(**kwargs)
		self.curent_threads_cbs = {}

	# def run_in_thread(self,func):
	# 	@functools.wraps(func)
	# 	def wrapper(*args, **kw):
	# 		print('i am running')
	# 		sf.__setattr__(func.__name__,ThreadHandler(func=lambda))
	# 		# threading.Thread(target=func).start()
	# 	return wrapper
	#
	# def add_api(self,name,function):
	# 	func=self.run_in_thread(function)
	# 	self.__setattr__(name,func)

	def load_model(self):
		self.t=ThreadHandler(func=lambda:self.get_network(),on_finished=self.on_load_model)

	def on_load_model(self):
		self.model=self.t.result
		print('model loaded')


if __name__ == '__main__':
	pass
