import sys
sys.path.insert(0,'../../..')
import cv2
import numpy as np
from utils import get_parent_path,read_img

def pre_process(path):
	img=read_img.read_img(path)
	img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	imgdatas = []
	img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
	imgdatas.append(img)
	imgdatas = np.array(imgdatas)
	imgdatas = imgdatas.astype('float32')
	imgdatas = imgdatas / 255.0
	return imgdatas

def test():
	path='../../../img/face.jpg'
	result=run(path)
	print(result.shape)

if __name__ == '__main__':
	test()
