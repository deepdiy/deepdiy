import cv2
# import numpy as np

def read_img(path):
    file_path_gbk = path.encode('gbk')
    img_mat = cv2.imread(file_path_gbk.decode())
    return img_mat

    # array=np.fromfile(path,dtype=np.uint8)
    # return cv2.imdecode(array,cv2.IMREAD_COLOR)
