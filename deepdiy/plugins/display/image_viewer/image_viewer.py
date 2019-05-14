import sys,os
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from utils.read_img import read_img
import cv2
from kivy.clock import Clock
from functools import partial


class ImageViewer(BoxLayout):
	data=DictProperty()
	def __init__(self,**kwargs):
		super(ImageViewer, self).__init__(**kwargs)
		self.bind(size=self.update)
		self.bind(data=self.update)

	def img2texture(self,*arg):
		self.h,self.w=self.img.shape[:2]
		self.texture = Texture.create(size=(self.w, self.h), colorfmt='rgb')
		self.texture.blit_buffer(self.img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
		self.texture.flip_vertical()
		w,h=self.size
		if w*h==0:
			self.w_out,self.h_out=self.size
		elif w/h>self.w/self.h:
			self.h_out=h
			self.w_out=h*(self.w/self.h)
		else:
			self.h_out=w*(self.h/self.w)
			self.w_out=w

	def update(self, *args):
		if self.data=={}:
			return
		if self.data['type']=='file_path':
			self.img=read_img(self.data['content'])
		elif self.data['type']=='img_bgr':
			self.img=self.data['content']
		elif self.data['type']=='img_gray':
			self.img=cv2.cvtColor(self.data['content'],cv2.COLOR_GRAY2BGR)
		self.canvas.clear()
		Clock.schedule_once(partial(self.draw),0.01)

	def draw(self,*args):
		self.img2texture()
		with self.canvas:
			Rectangle(texture=self.texture,
			pos=(int(self.center_x-self.w_out/2),int(self.center_y-self.h_out/2)),
			size=(self.w_out,self.h_out))

class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		iv=ImageViewer()
		img=cv2.imread('../../img/face.jpg',0)
		# iv.data={'type':'file_path','content':'../../img/face.jpg'}
		iv.data={'type':'img_gray','content':img}
		return iv


if __name__ == '__main__':
	test=Test().run()
