import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.graphics.texture import Texture
from controllers.zoom import Zoom

import cv2
from array import array
from kivy.graphics import Rectangle

class ImageViewer(BoxLayout):
    img=ListProperty()
    def __init__(self,**kwargs):
        super(ImageViewer, self).__init__(**kwargs)

        img=cv2.imread('D:\onedrive\program\worm_analyst/training\mask_rcnn\Mask_RCNN\dataset/train\img/training (9).tif')
        self.h,self.w,_=img.shape
        # create a 64x64 texture, defaults to rgb / ubyte
        self.texture = Texture.create(size=(self.w, self.h), colorfmt='rgb')
        # self.texture.wrap='clamp_to_edge'
        self.texture.blit_buffer(img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        self.texture.flip_vertical()

        self.ids = {child.id:child for child in self.children}
        self.bind(size=self.update)
        # print(self.children[0].children[1].children[0])
        self.zoom=self.children[0].children[0].children[0]
        self.update()


    def update(self, *args):
        self.zoom.canvas.clear()
        with self.zoom.canvas:
            print(self.w,self.h,self.size)
            w,h=self.size
            if w*h==0:
                w_out,h_out=self.size
            elif w/h>self.w/self.h:
                h_out=h
                w_out=h*(self.w/self.h)
            else:
                h_out=w*(self.h/self.w)
                w_out=w
            Rectangle(texture=self.texture, pos=(0, 0), size=(w_out,h_out))
            # Rectangle(texture=self.texture, pos=(0, 0), size=self.size)
        print(self.size)




class TestApp(App):
    Builder.load_file('../views/image_viewer.kv')
    def build(self):
        return ImageViewer()

if __name__ == '__main__':
    TestApp().run()
