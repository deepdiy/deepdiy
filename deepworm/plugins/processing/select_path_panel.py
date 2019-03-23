import sys,os
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from utils.select_path_dialog import select_file,select_folder
from utils.get_file_list import get_file_list

class SelectPathPanel(BoxLayout):
	data=DictProperty()
	id='select_path_panel'
	bundle_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'select_path_panel.kv')

	def open_file(self):
		path=select_file()
		self.add_to_tree(path)

	def open_folder(self):
		path=select_folder()
		self.add_to_tree(path)

	def add_to_tree(self,path):
		self.data['directory']=path
		self.data['file_list']=get_file_list(path)
		tree={'node_id':'resources','children':[]}
		for file_path in self.data['file_list']:
			tree['children'].append({'node_id':file_path.split(os.sep)[-1],'type':'file_path','content':file_path,'children':[]})
		self.data['tree']=tree
		print(path)


class Test(App):
	def build(self):
		return SelectPathPanel()

if __name__ == '__main__':
	Test().run()
