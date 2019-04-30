import sys,os
sys.path.append('../../../')
from utils.get_parent_path import get_parent_path
bundle_dir=get_parent_path(3)+os.sep+'model_zoo'+os.sep+'mrcnn'
from utils.read_img import read_img

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.properties import DictProperty,ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from plugins.display.detection_viewer.visualize import random_colors,apply_mask,display_instances
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import cv2
import numpy as np
from pebble import concurrent
from functools import partial

class DetectionViewer(BoxLayout):
	data=DictProperty()
	img=DictProperty()
	w_out,h_out=[640,480]
	def __init__(self,**kwargs):
		super(DetectionViewer, self).__init__(**kwargs)
		self.bind(data=self.update)
		self.bind(size=self.draw)
		self.bind(img=self.draw)

	def img2texture(self):
		img=self.img['img']
		self.h,self.w=img.shape[:2]
		w,h=self.size
		if w*h==0:
			self.w_out,self.h_out=self.size
		elif w/h>self.w/self.h:
			self.h_out=h
			self.w_out=h*(self.w/self.h)
		else:
			self.h_out=w*(self.h/self.w)
			self.w_out=w
		self.texture = Texture.create(size=(self.w, self.h), colorfmt='rgb')
		self.texture.blit_buffer(img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
		self.texture.flip_vertical()

	def update(self, *args):
		if self.data=={}:
			return
		self.add_widget(Label(text='Rendering...Please wait...'))
		self.data['content']['image']=cv2.cvtColor(self.data['content']['image'],cv2.COLOR_BGR2RGB)
		render=self.render()
		render.add_done_callback(lambda job:Clock.schedule_once(partial(self.on_render_finished,job),0.01))


	@concurrent.thread
	def render(self):
		plt.close('all')
		fig = plt.figure(frameon=False)
		ax = fig.add_axes([0, 0, 1, 1])
		ax.axis('off')
		kwargs={'ax':ax,'title':'','show_mask':True,'show_bbox':True,'captions':None,'class_names':['background','target'],'boxes':np.array([]),'masks':None,'class_ids':None}
		for i in ['image','boxes','masks','class_ids','class_names','scores','colors']:
			if i in self.data['content']:
				kwargs[i]=self.data['content'][i]
		kwargs['class_names']=self.data['class_names']
		display_instances(**kwargs)
		fig.canvas.draw()
		img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
		img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		return img

	def on_render_finished(self,job,*ars):
		img=job.result()
		self.img={'img':img}

	def draw(self,*args):
		if len(self.img) ==0:
			return
		self.img2texture()
		self.clear_widgets()
		self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		image=cv2.imread('../../../img/face.jpg')
		iv=DetectionViewer()
		iv.data={
			'content':{
				'image':image,
				'boxes':np.array([[ 51,  80, 679, 852],
				[351, 156, 768, 601],
				[413,   7, 761, 197],
				[442, 189, 768, 305]]),
				'masks':np.zeros((768,1024,4)),
				'class_ids':np.array([1, 1, 1, 1]),
				'class_names':['background','elegans']
			},
			'class_names':['background','target']
		}
		return iv


if __name__ == '__main__':
	test=Test().run()
