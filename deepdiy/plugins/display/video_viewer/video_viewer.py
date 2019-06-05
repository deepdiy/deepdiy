import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,StringProperty,NumericProperty,BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import numpy as np
import cv2
from utils.image_stack_capture import ImageStackCapture

class VideoViewer(BoxLayout):
	"""Display video file, tiff img, camera stream

	1. When data updated or window size changed: set_capture_source()
	2.1 When Capture source setted: change frame_idx -> 0
	2.2 When user drag process bar: change frame_idx -> ?
	3. When frame_idx changed: fetch_frame(), render(), schedule_play()
	4.1 When user click 'Play' button: change state to 'play'
	4.2 schedule_play(): if state = 'play', change frame_idx -> +1

	Attributes:
		FPS: FPS of play
		data: dict, given by DisplayManager.
			contain the type and content for displaying
		cap: obj, the capture tool which output frame once a time
		frame_idx: int, index of current frame
		status: str, 'play','stop' or 'end'
		bundle_dir: the dir of main.py
	"""
	FPS=20
	data=DictProperty(force_dispatch=True)
	cap=ObjectProperty()
	frame_idx=NumericProperty()
	total_frames=NumericProperty(1)
	status=StringProperty('stop')
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'video_viewer.kv')

	def __init__(self):
		super(VideoViewer, self).__init__()
		self.bind(size=self.start_capture)
		self.bind(data=self.start_capture)
		self.bind(frame_idx=self.fetch_frame)
		self.bind(frame_idx=self.schedule_play)
		self.bind(status=self.schedule_play)

	def start_capture(self,*args):
		if self.data == {}:
			return
		if self.data['type'] == 'file_path':
			if self.data['content'].split('.')[-1] in 'tiff':
				self.cap = ImageStackCapture(path=self.data['content'])
			else:
				self.cap = cv2.VideoCapture(self.data['content'])
		elif self.data['type'] == 'img_stack':
			self.cap = ImageStackCapture(stack=self.data['content'])
		elif self.data['type'] == 'camera':
			self.cap = cv2.VideoCapture(0)
		if self.cap != None:
			self.total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
			self.frame_idx = 0
			'''in case of frame_idx unchange, force dispactch'''
			self.property('frame_idx').dispatch(self)

	def fetch_frame(self,*args):
		'''Read a new frame, then render()'''
		prev_frame_idx = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
		if self.frame_idx != prev_frame_idx +1:
			self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.frame_idx)
		ret, frame = self.cap.read()
		if ret==True:
			self.frame = cv2.flip(frame,0)
			self.render()
		else:
			frame=None
			self.status = 'end'

	def render(self,*args):
		bug = self.nomalize_to_8_bit_BGR(self.frame)
		buf = bug.tostring()
		texture1 = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
		texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		self.ids.preview.texture = texture1
		self.ids.play_progress.value=self.frame_idx+1

	def on_play_clicked(self):
		if self.status == 'play':
			self.status = 'stop'
		elif self.status == 'end': # if at end, restart
			self.frame_idx = 0
			self.status = 'play'
		elif self.status == 'stop':
			self.status = 'play'

	def schedule_play(self,*args):
		if self.status != 'play':
			return
		Clock.schedule_once(lambda *args:setattr(
			self,'frame_idx',self.frame_idx+1), 1 / self.FPS)

	def nomalize_to_8_bit_BGR(self,img):
		if img.dtype=='uint16':
			img = img/np.max(img)*255
		img = img.astype(np.uint8)
		if len(img.shape) ==2:
			img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
		return img


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty(lambda:None)
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=VideoViewer()
		# demo.data = {'type':'file_path','content':os.sep.join([demo.bundle_dir,'video','drop.avi'])}
		demo.data = {'type':'file_path','content':'D:\onedrive\program/for_liuyuan_rotation\data/test.tiff'}
		return demo

if __name__ == '__main__':
	Test().run()
