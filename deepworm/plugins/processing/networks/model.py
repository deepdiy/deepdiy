import sys,os
sys.path.append('../../../')
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
import functools
import threading
from utils.thread_handler import ThreadHandler
from utils.read_img import read_img
from kivy.clock import Clock
import cv2

class Model(EventDispatcher):
	input=ObjectProperty()
	pre_process=ObjectProperty()
	out=ObjectProperty()

	def __init__(self,**kwargs):
		super(Model, self).__init__(**kwargs)
		self.model=None
		self.weight_idx=None

	def load_model(self):
		if self.model is None:
			self.model=self.get_network()

	def load_weight(self,weight):
		weight_idx=[item.split(os.sep)[-1] for item in self.weight_list].index(weight)
		if self.weight_idx!=weight_idx:
			self.weight_idx=weight_idx
			self.model.load_weights(self.weight_list[weight_idx])

	def run(self,path,weight):
		self.load_model()
		self.load_weight(weight)
		input=self.pre_process(path)
		result=self.model.predict(input, batch_size=1, verbose=0)
		output=self.post_process(result)
		return output


if __name__ == '__main__':
	pass
