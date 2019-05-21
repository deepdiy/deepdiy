import os,rootpath
rootpath.append(pattern='plugins')
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,NumericProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label

class Downloader(BoxLayout):
	"""docstring for Downloader."""

	data=ObjectProperty()
	bundle_dir = rootpath.detect(pattern='plugins')
	percent=NumericProperty(0)
	file_name=StringProperty('')
	status=StringProperty('')
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'downloader.kv')

	def __init__(self):
		super(Downloader, self).__init__()

	def on_success(self,*args):
		self.status='Download Finished'
		if self.extract_dir is None:
			return
		elif self.extract_dir=='./':
			self.unzip(self.file_path,os.path.dirname(self.file_path))
		else:
			self.unzip(self.file_path,self.extract_dir)
		if not self.callbacks is None:
			self.callbacks()

	def on_failure(self,*args):
		self.status='Download Failed'

	def on_progress(self,req,current_size,total_size):
		self.percent=current_size/total_size*100

	def download(self,url,file_path,extract_dir=None,callbacks=None):
		self.file_path=file_path
		self.extract_dir=extract_dir
		self.callbacks=callbacks
		self.status='Downloading '+self.file_name
		req = UrlRequest(url,file_path=file_path,on_success=self.on_success,on_failure=self.on_failure,on_progress=self.on_progress)

	def unzip(self,zip_path,extract_dir):
		import shutil
		shutil.unpack_archive(zip_path,extract_dir)
		os.remove(zip_path)
		self.status='Unzip Finished'


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Downloader()
		demo.download('http://www.deepdiy.net/model_zoo/models/mrcnn.zip', file_path='mrcnn.zip',extract_dir='mrcnn')
		# demo.download('https://speed.hetzner.de/100MB.bin', file_path='100MB.bin')
		return demo

if __name__ == '__main__':
	Test().run()
