import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty,DictProperty,StringProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from plugins.processing.model_zoo.installer import Installer


class ModelCard(BoxLayout):

	meta_info = DictProperty()

	def __init__(self, meta_info):
		super(ModelCard, self).__init__()
		self.meta_info=meta_info
		self.register_event_type('on_install')

	def install(self,*args):
		installer=Installer()
		self.ids.installer.clear_widgets()
		self.ids.installer.add_widget(installer)
		installer.bind(on_success=lambda x:self.dispatch('on_install'))
		installer.install_model(
			self.meta_info['id'],self.meta_info['install_url'])

	def popup_readme(self):
		pass

	def on_install(self,*args):
		pass

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
		self.register_event_type('on_install')

	def collect_local_models(self):
		pass

	def collect_online_models(self):
		req = UrlRequest('http://www.deepdiy.net/model_zoo/api/model_list.json', lambda req,result:setattr(self,'online_models',result))

	def render_model_cards(self,*args):
		for model in self.online_models:
			card=Factory.ModelCard(model)
			self.ids.model_album.add_widget(card)
			card.bind(on_install=lambda x:self.dispatch('on_install'))

	def on_install(self,*args):
		print('hi')


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
