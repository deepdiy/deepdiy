import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.graphics.texture import Texture
from controllers.zoom import Zoom
from kivy.graphics import Rectangle



class ImageViewer(BoxLayout):
    img=DictProperty()
    Builder.load_file('../views/image_viewer.kv')
    def __init__(self,**kwargs):
        super(ImageViewer, self).__init__(**kwargs)

        self.ids = {child.id:child for child in self.children}
        self.bind(size=self.update)
        # print(self.children[0].children[1].children[0])
        self.zoom=self.children[0].children[0].children[0]

    def img2texture(self):
        self.h,self.w,_=self.img['img'].shape
        self.texture = Texture.create(size=(self.w, self.h), colorfmt='rgb')
        self.texture.blit_buffer(self.img['img'].tostring(), colorfmt='bgr', bufferfmt='ubyte')
        self.texture.flip_vertical()
        w,h=self.size
        if w*h==0:
            self.w_out,self.h_out=self.size
        elif w/h>self.w/self.h:
            self.h_out=h
            self.w_out=h*(self.w/self.h)
        else:
            self.h_out=w*(self.h/self.w)
            self.w_out=w

    def update(self, *args):
        if self.img=={}:
            return
        self.img2texture()
        self.zoom.canvas.clear()
        with self.zoom.canvas:
            Rectangle(texture=self.texture, pos=(0, 0), size=(self.w_out,self.h_out))


class TestApp(App):
    def build(self):
        import cv2
        img=cv2.imread('D:\onedrive\program\worm_analyst/training\mask_rcnn\Mask_RCNN\dataset/train\img/training (9).tif')
        image_viewer=ImageViewer()
        image_viewer.img={'img':img}
        return image_viewer

if __name__ == '__main__':
    TestApp().run()
