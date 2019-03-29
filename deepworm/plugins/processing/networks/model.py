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

	def run(self,path,weight):
		weight_idx=[item.split(os.sep)[-1] for item in self.weight_list].index(weight)
		import tensorflow as tf
		self.graph = tf.get_default_graph()
		with self.graph.as_default():
			if self.model is None:
				self.model=self.get_network()
			if self.weight_idx!=weight_idx:
				self.weight_idx=weight_idx
				self.model.load_weights(self.weight_list[weight_idx])
			input=self.pre_process(path)
			result=self.model.predict(input, batch_size=1, verbose=0)
			output=self.post_process(result)
			# cv2.imshow('img',output)
			# cv2.waitKey(0)
			# output={
			# 	'node_id':'mask',
			# 	'type':'img',
			# 	'content':output,
			# 	'display':'image_viewer',
			# 	'children':[]}
			return output


if __name__ == '__main__':
	pass
