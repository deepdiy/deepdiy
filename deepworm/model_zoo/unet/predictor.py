import sys,os
sys.path.append('../../')
from utils.get_parent_path import get_parent_path
from utils.read_img import read_img
bundle_dir=get_parent_path(3)+os.sep+'model_zoo'+os.sep+'unet'
sys.path.append(bundle_dir)
import numpy as np
import cv2
from core.form_parser import FormParser

class Predictor(FormParser):
	"""docstring for Predictor."""

	def __init__(self):
		super(Predictor, self).__init__()
		self.input_img_path=''
		self.weight_path=''

	def set_input(self,input_img_path):
		img=read_img(input_img_path)
		img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
		imgdatas=np.array([img])
		imgdatas = imgdatas.astype('float32')
		self.input = imgdatas / 255.0
		return imgdatas

	def load_network(self):
		from model_zoo.unet.unet.unet import UNet
		self.model = network=UNet().unet_net()

	def load_weight(self):
		self.model.load_weights(self.weight_path)

	def predict(self):
		result=self.model.predict(self.input, batch_size=1, verbose=0)
		self.result=result[0]


class Test(object):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

		predictor=Predictor()
		predictor.set_input('../../img/face.jpg')
		predictor.weight_path='assets/unet.hdf5'
		predictor.load_network()
		predictor.load_weight()
		predictor.predict()
		print(predictor.result)

if __name__ == '__main__':
	test=Test()
