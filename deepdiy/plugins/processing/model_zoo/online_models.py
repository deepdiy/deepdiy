import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH 
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,StringProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.network.urlrequest import UrlRequest
from plugins.processing.model_zoo.installer import Installer


class ModelCard(BoxLayout):

	title=StringProperty()
	id=StringProperty()
	tags=StringProperty()
	abstract=StringProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py

	def __init__(self, **kwargs):
		super(ModelCard, self).__init__()
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
		installer.install_model(self.id,self.dowload)

class OnlineModels(ModalView):
	"""docstring for OnlineModels."""

	data=ObjectProperty()
	local_models=ListProperty()
	online_models=ListProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'online_models.kv')

	def __init__(self):
		super(OnlineModels, self).__init__()
		self.collect_local_models()
		self.collect_online_models()
		self.bind(online_models=self.render_model_cards)

	def collect_local_models(self):
		pass

	def collect_online_models(self):
		req = UrlRequest('http://www.deepdiy.net/model_zoo/api/model_list.json', lambda req,result:setattr(self,'online_models',result))

	def render_model_cards(self,*args):
		for model in self.online_models:
			self.ids.model_album.add_widget(Factory.ModelCard(
				title=model['title'],id=model['id'],abstract=model['abstract'],download=model['download']))


class Test(App):
	"""docstring for Test."""

	data=ObjectProperty()
	plugins=DictProperty()

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=OnlineModels()
		return demo

if __name__ == '__main__':
	Test().run()
