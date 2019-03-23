import cv2
import numpy as np
def read_img(path):
    return cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_COLOR)
