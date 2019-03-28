import sys
sys.path.insert(0,'../../..')
import cv2
import numpy as np
from utils import get_parent_path,read_img

def post_process(preds):
	mask = preds[0]
	mask[mask>0.5] = 1
	mask[mask<=0.5] = 0
	mask = mask * 255
	mask = mask.astype('uint8')
	return mask

def test():
	path='../../../img/face.jpg'
	mask=cv2.imread(path,0)
	mask = np.array(mask)
	mask = mask.astype('float32')
	mask=mask/255
	result=run([mask])
	cv2.imshow('img',result)
	cv2.waitKey(0)
	print(result.shape)

if __name__ == '__main__':
	test()
