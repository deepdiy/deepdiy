from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
import threading


class Model(EventDispatcher):
	input=ObjectProperty()
	pre_process=ObjectProperty()
	out=ObjectProperty()

	def __init__(self,**kwargs):
		super(Model, self).__init__(**kwargs)

	def add_api(self,name,function):
		self.wrap_function(name,function)

	def wrap_function(self,name,function):
		self.__setattr__(name,function)

	def load_model(self):
		self.model=self.get_network()

if __name__ == '__main__':
	pass
