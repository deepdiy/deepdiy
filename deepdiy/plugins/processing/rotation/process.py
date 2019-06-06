import numpy as np
import cv2
from matplotlib import pyplot as plt
from pysnooper import snoop

def nomalize_to_8_bit_BGR(img):
    if img.dtype=='uint16':
        img = img/np.max(img)*255
    img = img.astype(np.uint8)
    if len(img.shape) ==2:
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    return img

# @snoop()
def process(frame):
    # plt.subplot(231)
    # plt.imshow(frame)

    # # step1: extract bright field
    # 转为灰度图
    frame = nomalize_to_8_bit_BGR(frame)
    frame = cv2.resize(frame,(256,256))
    img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # 中值模糊去噪点
    MEDIUM_BLUR_RADIUM=5
    img_blur=cv2.medianBlur(img_gray,MEDIUM_BLUR_RADIUM)
    # plt.subplot(232)
    # plt.imshow(img_blur,'gray')

    # 阈值分割
    _,thresh = cv2.threshold(img_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # plt.subplot(233)
    # plt.imshow(thresh,'gray')

    # 提取明亮区域
    img=thresh.copy()
    bright_area_masks=[]
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # 提取轮廓
    for cnt in contours:# 遍历轮廓
        mask = np.zeros(img.shape,np.uint8)# 空mask
        hull = cv2.convexHull(cnt)#考虑到小球可能接触到明场边缘, 需要使用轮廓的凸包
        cv2.drawContours(mask,[hull],0,255,-1) # 用轮廓填充mask
        mean_val = cv2.mean(img,mask = mask)[0]# 用mask计算轮廓内平均灰度
        if mean_val>128:# 如果轮廓内亮度>128
            bright_area_masks.append(mask) # 收集这个mask
    # 一张图可能有多个明亮区域, 但明场视野应该是像素亮度总和最高的
    idx=np.argmax([cv2.mean(img,mask=area)[0]*cv2.countNonZero(area) for area in bright_area_masks])
    bright_field_mask=bright_area_masks[idx]
    # plt.subplot(234)
    # plt.imshow(bright_field_mask,'gray')

    # # step2: 明场内找黑斑

    img_balls=thresh+255-bright_field_mask # 将明场外区域填白
    # plt.subplot(235)
    # plt.imshow(img_balls,'gray')

    contours, hierarchy = cv2.findContours(255-img_balls,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # 提取轮廓(外框需要是黑的,所以反相一下)
    cnt=max(contours,key=cv2.contourArea) # 取面积最大的轮廓
    mask = np.zeros(img_balls.shape,np.uint8)# 空mask
    cv2.drawContours(mask,[cnt],0,255,-1) # 用轮廓填充mask
    ellipse=cv2.fitEllipse(cnt)
    img_label=cv2.ellipse(frame,ellipse,(0,255,0),2)
    # plt.subplot(236)
    # plt.imshow(img_label,'gray')
    return img_label,ellipse[2]

def cal_rotation(a,b):
    if 0<=abs(b-a)<=90:
        return b-a
    elif 90<b-a<180:
        return b-a-180
    elif -180<b-a<-90:
        return 180+b-a

def run_tiff(file_path,progress_percent):
    progress_percent
    angle = 0
    ret,video=cv2.imreadmulti(file_path,flags=cv2.IMREAD_ANYDEPTH)
    video_labeled,table=[],[]
    idx=1
    for frame in video[:]:
        img_label,angle_new=process(frame)
        angle_new = float('{0:.2f}'.format(angle_new))
        rotation=cal_rotation(angle,angle_new)
        rotation = float('{0:.2f}'.format(rotation))
        table.append([angle,rotation,angle_new])
        video_labeled.append(img_label)
        angle=angle_new
        idx+=1
        progress_percent['value']=idx/len(video)*100
        # print(table[-1])
        # cv2.imshow('img',cv2.resize(img_label,(512,512)))
        # if cv2.waitKey(0) & 0xFF == ord('q'):
        #     break
    return video_labeled,table

if __name__ == '__main__':
    run_tiff('D:\onedrive\program/for_liuyuan_rotation\data/test.tiff')
