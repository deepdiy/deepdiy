import os,sys
sys.path.append('../../deepdiy')
sys.path.append('../../')

from kivy.app import App
from utils.quickplugin import QuickPlugin
import cv2
import numpy as np


class Canny(QuickPlugin):
	def __init__(self):
		super(Canny, self).__init__()
		self.input_type=['file_path']
		self.result_meta={
			'node_id':'canny_edge',
			'type':'img_gray',
			'display':'image_viewer',}
		self.kwargs=[
			{'id':'min_val','type':'text_input','text':'100'},
			{'id':'max_val','type':'text_input','text':'200'}]

	def run(self,img_path,min_val,max_val):
		print(img_path)
		img=cv2.imread(img_path,0)
		edges=cv2.Canny(img,min_val,max_val)
		# cv2.imshow('img',edges)
		# cv2.waitKey(0)
		return edges


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)
		self.canny=Canny()
		self.canny.data.load_sample_data()

	def build(self):
		return self.canny

if __name__ == '__main__':
	Test().run()
