import cv2
import numpy as np

def read_img(path):
    array=np.fromfile(path,dtype=np.uint8)
    return cv2.imdecode(array,cv2.IMREAD_COLOR)
