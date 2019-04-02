#coding:utf-8
__author__ = 'MsLili'
#pickle模块主要函数的应用举例
import pickle
import cv2
import numpy as np
dataList = [[1, 1, 'yes'],
            [1, 1, 'yes'],
            [1, 0, 'no'],
            [0, 1, 'no'],
            [0, 1, 'no']]
dataDic = { 0: [1, 2, 3, 4],
            1: ('a', 'b'),
            2: {'c':'yes','d':'no'}}

def pp(input):
    cv2.imshow('img',np.zeros((100,100,3)))
    print('hi')

#使用dump()将数据序列化到文件中
fw = open('dataFile.txt','wb')
# Pickle the list using the highest protocol available.
# pickle.dump(dataList, fw, -1)
# Pickle dictionary using protocol 0.
pickle.dump(pp, fw)
fw.close()

#使用load()将数据从文件中序列化读出
fr = open('dataFile.txt','rb')
data1 = pickle.load(fr)
print(data1)
data1('hi')
# data2 = pickle.load(fr)
# print(data2)
fr.close()

#使用dumps()和loads()举例
# p = pickle.dumps(dataList)
# print( pickle.loads(p) )
# p = pickle.dumps(dataDic)
# print( pickle.loads(p) )
