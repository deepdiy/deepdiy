import os,rootpath
rootpath.append(pattern='plugins')
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,NumericProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import requests
import shutil

class Demo(BoxLayout):
	"""docstring for Demo."""
	url=StringProperty()
	filename=StringProperty()
	percent=NumericProperty()
	bundle_dir = rootpath.detect(pattern='plugins')
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'gallery.kv')
	data=DictProperty()

	def __init__(self):
		super(Demo, self).__init__()
		self.add_widget(Button(text='download',on_release=self.download))

	def download(self,*args):
		with open(self.filename, 'wb') as f:
			response = requests.get(self.url, stream=True)
			total = response.headers.get('content-length')

			if total is None:
				f.write(response.content)
			else:
				downloaded = 0
				total = int(total)
				for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
					downloaded += len(data)
					f.write(data)
					self.percent = int(100*downloaded/total)
					print(self.percent)


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Demo()
		demo.url='https://speed.hetzner.de/100MB.bin'
		demo.filename='100MB.bin'
		return demo

if __name__ == '__main__':
	Test().run()
