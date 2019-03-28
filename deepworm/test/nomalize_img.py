import cv2
import numpy as np

def run(img,size=(None,None),color_convert=None,dtype=None):
	if img is None:
		print('[Error] Empty image.')
	else:
		h,w=img.shape[:2]
	if not size[0] is None:
		w=size[0]
	if not size[1] is None:
		h=size[1]

	img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
	# img = np.reshape(img,img.shape+(1,))
	# imgdatas = np.array(imgdatas)
	# imgdatas = imgdatas.astype('float32')
	# imgdatas = imgdatas / 255.0
	return img

def test():
	from scipy.misc import face
	img=face()
	img=run(img)
	cv2.imshow('img',img)
	cv2.waitKey(0)


if __name__ == '__main__':
	test()
