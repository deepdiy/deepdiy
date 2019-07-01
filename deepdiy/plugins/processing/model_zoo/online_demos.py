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
from plugins.processing.model_zoo.installer import Installer

class DemoCard(BoxLayout):

	title=StringProperty()
	id=StringProperty()
	tags=StringProperty()
	abstract=StringProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py

	def __init__(self, meta_info):
		super(DemoCard, self).__init__()
		self.title=meta_info['title']
		self.id=meta_info['id']
		self.abstract=meta_info['abstract']
		self.meta_info=meta_info
		self.register_event_type('on_install')

	def install(self,*args):
		installer=Installer()
		self.ids.installer.clear_widgets()
		self.ids.installer.add_widget(installer)
		installer.bind(on_success=lambda x:self.dispatch('on_install'))
		installer.install_demo_full(self.id,self.meta_info)

	def on_install(self,*args):
		pass

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
		self.register_event_type('on_install')

	def collect_local_demos(self):
		pass

	def collect_online_demos(self):
		req = UrlRequest('http://www.deepdiy.net/model_zoo/api/demo_list.json', lambda req,result:setattr(self,'online_demos',result))

	def insert_model_cards(self,*args):
		for meta_info in self.online_demos:
			card = Factory.DemoCard(meta_info)
			self.ids.model_album.add_widget(card)
			card.bind(on_install=lambda x:self.dispatch('on_install'))

	def on_install(self,*args):
		pass


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
