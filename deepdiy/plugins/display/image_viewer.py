import sys,os
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from utils.read_img import read_img


class ImageViewer(BoxLayout):
	data=DictProperty()
	def __init__(self,**kwargs):
		super(ImageViewer, self).__init__(**kwargs)
		# self.add_widget(FigureCanvasKivyAgg(plt.gcf()))
		self.bind(size=self.update)
		self.bind(data=self.update)

		# self.add_widget(Image(size=(32,32),texture=self.texture,keep_ratio=True,allow_stretch=False))

	def img2texture(self):
		self.h,self.w=self.img.shape[:2]
		self.texture = Texture.create(size=(self.w, self.h), colorfmt='rgb')
		self.texture.blit_buffer(self.img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
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
		if self.data=={}:
			return
		self.img=read_img(self.data['content'])
		self.img2texture()
		self.canvas.clear()
		with self.canvas:
			Rectangle(texture=self.texture, pos=(0, 0), size=(self.w_out,self.h_out))

class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		iv=ImageViewer()
		iv.data={'content':'../../img/face.jpg'}
		return iv


if __name__ == '__main__':
	test=Test().run()
