import sys,os
bundle_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(bundle_dir)
from mrcnn.config import Config
import numpy as np
import cv2,json

class Api(object):
	"""docstring for Api."""

	def __init__(self):
		super(Api, self).__init__()
		self.input_img_path=''
		self.weight_path=''
		self.config_path=''

	def set_input(self,input_img_path):
		array=np.fromfile(input_img_path,dtype=np.uint8)
		img=cv2.imdecode(array,cv2.IMREAD_COLOR)
		self.input=np.array([img])

	def load_network(self):
		config = Config()
		config.NAME = 'predict'
		config.NUM_CLASSES = 1 + 1
		config.IMAGES_PER_GPU = 1
		config.GPU_COUNT = 1

		additional_info = json.load(open(self.config_path))
		for i,j in additional_info.items():
			try:
				setattr(config,i,eval(j))
			except:
				setattr(config,i,j)
		config.__init__()
		from mrcnn import model as modellib
		self.model = modellib.MaskRCNN(mode="inference", model_dir='./',config=config)

	def load_weight(self):
		self.model.load_weights(self.weight_path, by_name=True)

	def predict(self):
		result=self.model.detect(self.input, verbose=1)
		self.result=result[0]
		self.result['image']=self.input[0]
		self.result['boxes']=self.result['rois']
		return self.result


class Test(object):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

		api=Api()
		api.set_input('../../img/face.jpg')
		api.weight_path='weights/mask_rcnn_coco.h5'
		api.config_path='configs/coco.json'
		api.load_network()
		api.load_weight()
		api.predict()

if __name__ == '__main__':
	test=Test()
