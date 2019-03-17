from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from array import array
from kivy.core.window import Window
import cv2

img=cv2.imread('D:\onedrive\program\worm_analyst/training\mask_rcnn\Mask_RCNN\dataset/train\img/training (9).tif')
# create a 64x64 texture, defaults to rgb / ubyte
texture = Texture.create(size=(1360, 1024), colorfmt='rgb')
texture.wrap='clamp_to_edge'
texture.blit_buffer(img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
texture.flip_vertical()
# texture.flip_horizontal()


root = Widget()
with root.canvas:
    Rectangle(texture=texture, pos=(0, 0), size=(500, 500))

runTouchApp(root)
