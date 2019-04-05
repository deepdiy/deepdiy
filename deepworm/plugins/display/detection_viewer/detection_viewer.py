import sys,os
sys.path.append('../../../')
from utils.get_parent_path import get_parent_path
bundle_dir=get_parent_path(3)+os.sep+'model_zoo'+os.sep+'mrcnn'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from utils.read_img import read_img
from plugins.display.detection_viewer.visualize import random_colors,apply_mask,display_instances
import matplotlib.pyplot as plt
import cv2
import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class DetectionViewer(BoxLayout):
	data=DictProperty()
	def __init__(self,**kwargs):
		super(DetectionViewer, self).__init__(**kwargs)
		self.bind(data=self.update)

	def update(self, *args):
		self.clear_widgets()
		plt.close('all')
		fig = plt.figure(frameon=False)
		ax = fig.add_axes([0, 0, 1, 1])
		ax.axis('off')
		kwargs={'ax':ax,'title':'','show_mask':True,'show_bbox':True,'captions':None,'class_names':['background','target'],'boxes':np.array([]),'masks':None,'class_ids':None}
		for i in ['image','boxes','masks','class_ids','class_names','scores','colors']:
			if i in self.data:
				kwargs[i]=self.data[i]
		display_instances(**kwargs)
		self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		image=cv2.imread('../../../img/face.jpg')
		iv=DetectionViewer()
		iv.data={
			'image':image,
			'boxes':np.array([[ 51,  80, 679, 852],
		       [351, 156, 768, 601],
		       [413,   7, 761, 197],
		       [442, 189, 768, 305]]),
			'masks':np.zeros((768,1024,4)),
			'class_ids':np.array([1, 1, 1, 1]),
			'class_names':['background','elegans']
		}
		return iv


if __name__ == '__main__':
	test=Test().run()
