import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty,StringProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from utils.downloader import Downloader
import shutil

class Installer(BoxLayout):
	"""docstring for Installer."""

	data=ObjectProperty()
	status=StringProperty()
	target=ListProperty()
	bundle_dir = rootpath.detect(pattern='main.py')
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'demo.kv')

	def __init__(self):
		super(Installer, self).__init__()
		self.bind(status=self.on_status_changed)

	def reset(self,type,id):
		self.target=[type,id]
		self.status='Start'
		self.downloader=Downloader()
		self.downloader.bind(status=self.setter('status'))
		self.clear_widgets()
		self.add_widget(self.downloader)
		self.working_dir=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo',type+'s',id])
		print(self.working_dir)
		os.makedirs(self.working_dir, exist_ok=True)

	def on_status_changed(self,ins,value):
		if 'Fail' in value:
			self.on_failure()
		elif value=='Unzip Finished':
			self.on_success()

	def on_success(self):
		self.clear_widgets()
		self.add_widget(Label(text='[color=00ff33]Succesfully installed '+' : '.join(self.target)+'[/color]',text_size=self.size,valign='center',markup = True,font_size=18))

	def on_failure(self):
		self.clear_widgets()
		try: shutil.rmtree(self.working_dir)
		except: pass
		self.add_widget(Label(text='[color=ff3333]'+self.status+'[/color]',text_size=self.size,valign='center',markup = True,font_size=18))

	def install_model(self,id,url):
		self.reset('model',id)
		file_path=self.working_dir+os.sep+url.split('/')[-1]
		self.downloader.download(url,file_path,extract_dir='./')

	def install_demo(self,id,model,demo_url,weight_url=None):
		def install_weight():
			self.install_weight(model,weight_url)
		self.reset('demo',id)
		file_path=self.working_dir+os.sep+demo_url.split('/')[-1]
		self.downloader.file_name='Demo('+id+')'
		self.downloader.download(demo_url,file_path,extract_dir='./',callbacks=install_weight)

	def install_weight(self,model,url):
		self.reset('weight',model)
		file_path=self.working_dir+os.sep+url.split('/')[-1]
		self.downloader.file_name='Weight('+url.split('/')[-1]+')'
		self.downloader.download(url,file_path)



class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Installer()
		demo.install_model('mrcnn','http://www.deepdiy.net/model_zoo/models/mrcnn.zip')
		# demo.install_weight('mrcnn','http://www.deepdiy.net/model_zoo/models/mrcnn.zip')
		# demo.install_weight('mrcnn','http://www.deepdiy.net/model_zoo/weights/mrcnn/mask_rcnn_coco.h5')
		# demo.install_demo('mrcnn_coco','mrcnn','http://www.deepdiy.net/model_zoo/demos/mrcnn_coco.zip','http://www.deepdiy.net/model_zoo/weights/mrcnn/mask_rcnn_coco.h5')
		return demo

if __name__ == '__main__':
	Test().run()
