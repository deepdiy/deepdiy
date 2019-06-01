import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH 
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,StringProperty,NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import numpy as np
import cv2

class VideoViewer(BoxLayout):
	"""docstring for VideoViewer."""

	data=DictProperty()
	video_path=StringProperty()
	frame_idx=NumericProperty(-1)
	total_frames=NumericProperty(1)
	status=StringProperty('start')
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'video_viewer.kv')

	def __init__(self):
		super(VideoViewer, self).__init__()
		self.bind(size=self.update)
		self.bind(data=self.update)
		self.bind(video_path=self.open_video)
		self.bind(frame_idx=self.render)
		self.ids.play_progress.bind(value=self.on_progress)

	def open_video(self,*args):
		self.cap = cv2.VideoCapture(self.video_path)
		self.total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
		self.fetch_frame()

	def fetch_frame(self,*args):
		frame=None
		ret, frame = self.cap.read()
		if ret==True:
			self.frame = cv2.flip(frame,0)
			self.frame_idx+=1
		else:
			self.status='end'

	def to_certain_frame(self,frame_idx):
		if 0 <= frame_idx <= self.total_frames:
			self.frame_idx=frame_idx-1
			self.cap.set(cv2.CAP_PROP_POS_FRAMES,frame_idx)
			self.fetch_frame()

	def to_next_frame(self):
		self.fetch_frame()

	def to_previous_frame(self):
		self.to_certain_frame(self.frame_idx-1)

	def play(self):
		if self.status=='end':
			self.ids.play_progress.value=0
		self.status='play'
		Clock.schedule_once(self.fetch_frame, 1 / 20.)

	def pause(self):
		self.status='palse'

	def on_progress(self,ins,value):
		if value!=self.frame_idx+1:
			self.to_certain_frame(value)
		if self.status=='play':
			Clock.schedule_once(self.fetch_frame, 1 / 20.)

	def render(self,*args):
		if self.frame is None:
			return
		buf = self.frame.tostring()
		texture1 = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
		texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		self.ids.preview.texture = texture1
		self.ids.play_progress.value=self.frame_idx+1

	def update(self,*args):
		if self.data=={}:
			return
		if self.data['type']=='file_path':
			self.video_path=self.data['content']
			self.frame_idx=0
		elif self.data['type']=='img_bgr':
			self.img=self.data['content']
		elif self.data['type']=='img_gray':
			self.img=cv2.cvtColor(self.data['content'],cv2.COLOR_GRAY2BGR)


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=VideoViewer()
		demo.video_path=os.sep.join([demo.bundle_dir,'video','drop.avi'])
		return demo

if __name__ == '__main__':
	Test().run()
