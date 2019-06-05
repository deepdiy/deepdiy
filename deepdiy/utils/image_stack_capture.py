import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import cv2
import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,StringProperty,NumericProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout

class ImageStackCapture(BoxLayout):
	"""docstring for ImageStackCapture."""

	data = ObjectProperty()
	stack = ListProperty()
	path = StringProperty()
	frame_count = NumericProperty()
	pos_frames = NumericProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'demo.kv')

	def __init__(self,path='',stack=[]):
		super(ImageStackCapture, self).__init__()
		self.bind(path=self.read_tiff)
		if path != '':
			self.path = path
		if stack != []:
			self.stack = stack
			self.frame_count = len(self.stack)

	def get(self,param):
		if param == cv2.CAP_PROP_FRAME_COUNT:
			return self.frame_count
		if param == cv2.CAP_PROP_POS_FRAMES:
			return self.pos_frames

	def set(self,param,value):
		if param == cv2.CAP_PROP_POS_FRAMES:
			self.pos_frames = int(value)

	def read(self):
		if self.pos_frames < self.frame_count:
			frame = self.stack[self.pos_frames]
			self.pos_frames += 1
			return True,frame
		else:
			return False, None

	def read_tiff(self,*args):
		ret,self.stack = cv2.imreadmulti(self.path,flags=cv2.IMREAD_ANYDEPTH)
		self.frame_count = len(self.stack)


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build2(self):
		demo=ImageStackCapture()
		demo.path = 'D:\onedrive\program/for_liuyuan_rotation\data/test.tiff'
		ret,img = demo.read()
		img = img/np.max(img)*255
		img = img.astype(np.uint8)
		cv2.imshow('img',cv2.resize(img,(512,512)))
		cv2.waitKey(0)
		return demo

	def build(self):
		path = 'D:\onedrive\program/for_liuyuan_rotation\data/test.tiff'
		ret,video=cv2.imreadmulti(path,flags=cv2.IMREAD_ANYDEPTH)
		demo=ImageStackCapture(stack=video)
		ret,img = demo.read()
		print(img)
		img = img/np.max(img)*255
		img = img.astype(np.uint8)
		cv2.imshow('img',cv2.resize(img,(512,512)))
		cv2.waitKey(0)
		return demo

if __name__ == '__main__':
	Test().run()
