import sys,os
sys.path.append('../../')
from utils.get_parent_path import get_parent_path
from utils.read_img import read_img
bundle_dir=get_parent_path(3)+os.sep+'model_zoo'+os.sep+'mrcnn'
sys.path.append(bundle_dir)
from mrcnn.config import Config
import numpy as np
from core.form_parser import FormParser

class Predictor(FormParser):
	"""docstring for Predictor."""

	def __init__(self):
		super(Predictor, self).__init__()
		self.input_img_path=''
		self.weight_path=''

	def set_input(self,input_img_path):
		img=read_img(input_img_path)
		self.input=np.array([img])

	def load_network(self):
		config = Config()
		config.NAME = 'predict'  # Background + elegans
		config.NUM_CLASSES = 1 + 1  # Background + elegans
		config.IMAGES_PER_GPU = 1
		config.GPU_COUNT = 1
		config.__init__()
		from mrcnn import model as modellib
		self.model = modellib.MaskRCNN(mode="inference", model_dir='./',config=config)

	def load_weight(self):
		self.model.load_weights(self.weight_path, by_name=True)

	def predict(self):
		result=self.model.detect(self.input, verbose=1)
		self.result=result[0]
		return self.result


class Test(object):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

		predictor=Predictor()
		predictor.set_input('../../img/face.jpg')
		predictor.weight_path='assets/mask_rcnn_elegans_0021.h5'
		predictor.load_network()
		predictor.load_weight()
		predictor.predict()
		print(predictor.result)

if __name__ == '__main__':
	test=Test()
