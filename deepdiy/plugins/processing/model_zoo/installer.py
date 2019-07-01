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
		self.register_event_type('on_success')

	def reset(self,type,id):
		self.target=[type,id]
		self.status='Start'
		self.downloader=Downloader()
		self.downloader.bind(status=self.setter('status'))
		self.clear_widgets()
		self.add_widget(self.downloader)
		self.working_dir=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo',type+'s',id])
		os.makedirs(self.working_dir, exist_ok=True)

	def on_status_changed(self,ins,value):
		if 'Fail' in value:
			self.on_failure()
		elif value=='Unzip Finished':
			self.dispatch('on_success')

	def on_success(self):
		self.clear_widgets()
		self.add_widget(Label(text='[color=00ff33]Succesfully installed '+' : '.join(self.target)+'[/color]',text_size=self.size,valign='center',markup = True,font_size=18))

	def on_failure(self):
		self.clear_widgets()
		try: shutil.rmtree(self.working_dir)
		except: pass
		self.add_widget(Label(text='[color=ff3333]'+self.status+'[/color]',text_size=self.size,valign='center',markup = True,font_size=18))

	def install_model(self,id,url,callbacks=None):
		self.reset('model',id)
		file_path=self.working_dir+os.sep+url.split('/')[-1]
		self.downloader.download(url,file_path,extract_dir='./',callbacks=callbacks)

	def install_demo(self,id,url,callbacks=None):
		self.reset('demo',id)
		file_path=self.working_dir+os.sep+url.split('/')[-1]
		self.downloader.file_name='Demo('+id+')'
		self.downloader.download(url,file_path,extract_dir='./',callbacks=callbacks)

	def install_weight(self,model,url,callbacks=None):
		self.reset('weight',model)
		file_path=self.working_dir+os.sep+url.split('/')[-1]
		self.downloader.file_name='Weight('+url.split('/')[-1]+')'
		self.downloader.download(url,file_path,callbacks=callbacks)

	def copy_config(self,demo_id,model_id,model_config):
		path1=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo','demos',demo_id,model_config])
		path2=os.sep.join([self.bundle_dir,'plugins','processing','model_zoo','configs',model_id,model_config])
		os.makedirs(os.path.dirname(path2),exist_ok=True)
		shutil.copyfile(path1,path2)

	def install_demo_full(self,id,meta_info):
		model_id=meta_info['model']
		def t3():
			if 'model_config' in meta_info:
				self.copy_config(id,model_id,meta_info['model_config'])
		def t2():
			self.install_demo(id,meta_info['demo_url'],callbacks=t3)
		def t1():
			if 'model_url' in meta_info:
				self.install_model(model_id,meta_info['model_url'],callbacks=t2)
			else:
				t2()
		if 'weight_url' in meta_info:
			self.install_weight(model_id,meta_info['weight_url'],callbacks=t1)



class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Installer()
		# demo.install_model('mrcnn','http://www.deepdiy.net/model_zoo/models/mrcnn.zip')
		# demo.install_weight('mrcnn','http://www.deepdiy.net/model_zoo/models/mrcnn.zip')
		# demo.install_weight('mrcnn','http://www.deepdiy.net/model_zoo/weights/mrcnn/mask_rcnn_coco.h5')
		meta_info = {
			"title":"Mask-RCNN",
			"abstract":"The model generates bounding boxes and segmentation masks for each instance of an object in the image. It's based on Feature Pyramid Network (FPN) and a ResNet101 backbone.",
			"id":"mrcnn_coco",
			"ref_url":"https://github.com/matterport/Mask_RCNN",
			"model":"mrcnn",
			"model_config":"coco.json",
			"demo_url":"http://www.deepdiy.net/model_zoo/demos/mrcnn_coco.zip",
			"model_url":"http://www.deepdiy.net/model_zoo/models/mrcnn.zip",
			"weight_url":"http://www.deepdiy.net/model_zoo/weights/mrcnn/mask_rcnn_coco.h5"
		}
		demo.install_demo_full('mrcnn_coco',meta_info)
		return demo

if __name__ == '__main__':
	Test().run()
