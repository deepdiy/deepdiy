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
		plt.close('all')
		fig = plt.figure(frameon=False)
		ax = fig.add_axes([0, 0, 1, 1])
		ax.axis('off')
		display_instances(self.data['image'],
							self.data['boxes'],
							self.data['masks'],
							self.data['class_ids'],
							self.data['class_names'],
							scores=None, title="",
							ax=ax,
							show_mask=True, show_bbox=True,
							colors=None, captions=None)
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
