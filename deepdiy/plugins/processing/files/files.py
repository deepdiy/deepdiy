import os,rootpath
rootpath.append(pattern='plugins')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from utils.select_path_dialog import select_file,select_folder
from utils.get_file_list import get_file_list

class Files(BoxLayout):
	data=ObjectProperty(lambda: None)
	id='select_path_panel'
	bundle_dir = rootpath.detect(pattern='plugins')
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'files.kv')

	def open_file(self):
		path=select_file()
		self.data['file_list']=[path.replace('/',os.sep)]
		self.add_to_tree()

	def open_folder(self):
		path=select_folder()
		if path=='':
			return
		self.add_to_tree(path=path)

	def add_to_tree(self,path=''):
		if path!='':
			self.data.file_list=get_file_list(path,formats=['jpg','jpeg','bmp','png','tiff','tif'])
		tree={'node_id':'resources','children':[]}
		for file_path in self.data.file_list:
			tree['children'].append({
				'node_id':file_path.split(os.sep)[-1],
				'type':'file_path',
				'content':file_path,
				'display':'image_viewer',
				'children':[]})
		self.data.tree=tree
		self.property('data').dispatch(self)
		print(path)


class Test(App):
	def build(self):
		return Files()

if __name__ == '__main__':
	Test().run()
