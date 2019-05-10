import sys,os
bundle_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(bundle_dir)
import numpy as np
import cv2

class Api(object):
	"""docstring for Api."""

	def __init__(self):
		super(Api, self).__init__()
		self.input_img_path=''
		self.weight_path=''

	def set_input(self,input_img_path):
		array=np.fromfile(input_img_path,dtype=np.uint8)
		img=cv2.imdecode(array,cv2.IMREAD_COLOR)
		img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
		imgdatas=np.array([img])
		imgdatas = imgdatas.astype('float32')
		self.input = imgdatas / 255.0
		print(self.input.shape)

	def load_network(self):
		from model_zoo.unet.unet.unet import UNet
		self.model = network=UNet().unet_net()

	def load_weight(self):
		self.model.load_weights(self.weight_path)

	def predict(self):
		result=self.model.predict(self.input, batch_size=1, verbose=0)
		mask = result[0]
		mask[mask>0.5] = 1
		mask[mask<=0.5] = 0
		mask = mask * 255
		self.result = {'image':mask.astype('uint8')}

		return self.result


class Test(object):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

		api=Api()
		api.set_input('../../img/face.jpg')
		api.weight_path='assets/unet.hdf5'
		api.load_network()
		api.load_weight()
		api.predict()
		print(api.result)

if __name__ == '__main__':
	test=Test()
