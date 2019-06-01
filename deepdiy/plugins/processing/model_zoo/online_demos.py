import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH 
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,ListProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.network.urlrequest import UrlRequest
from utils.downloader import Downloader

class DemoCard(BoxLayout):

	title=StringProperty()
	id=StringProperty()
	tags=StringProperty()
	abstract=StringProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py

	def __init__(self, **kwargs):
		super(DemoCard, self).__init__()
		self.title=kwargs['title']
		self.id=kwargs['id']
		# self.tags=kwargs['tags']
		self.abstract=kwargs['abstract']
		self.dowload=kwargs['download']

	def install(self,*args):
		installer=Installer()
		url=self.dowload
		self.ids.installer.clear_widgets()
		self.ids.installer.add_widget(installer)
		installer.install_demo(self.id,self.dowload)

class OnlineDemos(ModalView):
	"""docstring for OnlineDemos."""

	data=ObjectProperty()
	local_demos=ListProperty()
	online_demos=ListProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'online_demos.kv')

	def __init__(self):
		super(OnlineDemos, self).__init__()
		self.collect_local_demos()
		self.collect_online_demos()
		self.bind(online_demos=self.insert_model_cards)

	def collect_local_demos(self):
		pass

	def collect_online_demos(self):
		req = UrlRequest('http://www.deepdiy.net/model_zoo/api/demo_list.json', lambda req,result:setattr(self,'online_demos',result))

	def insert_model_cards(self,*args):
		for model in self.online_demos:
			self.ids.model_album.add_widget(Factory.DemoCard(
				title=model['title'],id=model['id'],abstract=model['abstract'],download=model['download']))


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()



	def build(self):
		demo=OnlineDemos()
		return demo

if __name__ == '__main__':
	Test().run()
