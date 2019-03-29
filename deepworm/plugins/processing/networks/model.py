import sys,os
sys.path.append('../../../')
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
import functools
import threading
from utils.thread_handler import ThreadHandler
from utils.read_img import read_img
from kivy.clock import Clock
import tensorflow as tf
import cv2
from keras import backend as K

class Model(EventDispatcher):
	input=ObjectProperty()
	pre_process=ObjectProperty()
	out=ObjectProperty()

	def __init__(self,**kwargs):
		super(Model, self).__init__(**kwargs)
		self.curent_threads_cbs = {}

	def load_nn(self):
		self.graph = tf.get_default_graph()
		self.model=self.get_network()


	def load_model(self):
		self.t=ThreadHandler(func=lambda:self.load_nn(),on_finished=self.on_load_model)

	def on_load_model(self):
		# self.model=self.t.result
		print('model loaded')

	def run(self,path):
		with self.graph.as_default():
			self.model.load_weights(self.weight_list[0])

			data=self.pre_process(path)
			img=self.model.predict(data, batch_size=1, verbose=0)
			img=self.post_process(img)
			cv2.imshow('img',img)
			cv2.waitKey(0)
		#
		# data=self.





if __name__ == '__main__':
	pass
