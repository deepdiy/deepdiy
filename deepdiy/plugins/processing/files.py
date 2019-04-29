import sys,os
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from utils.select_path_dialog import select_file,select_folder
from utils.get_file_list import get_file_list
from utils.get_parent_path import get_parent_path

class Files(BoxLayout):
	data=DictProperty()
	id='select_path_panel'
	bundle_dir = get_parent_path(3)
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
			self.data['file_list']=get_file_list(path,formats=['jpg','jpeg','bmp','png','tiff','tif'])
		tree={'node_id':'resources','children':[]}
		for file_path in self.data['file_list']:
			tree['children'].append({
				'node_id':'<Path>'+file_path.split(os.sep)[-1],
				'content':file_path,
				'display':'image_viewer',
				'children':[]})
		self.data['tree']=tree
		print(path)


class Test(App):
	def build(self):
		return Files()

if __name__ == '__main__':
	Test().run()
