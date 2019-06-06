import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plugins.processing.rotation.process import run_tiff
from utils.quickplugin import QuickPlugin
import cv2
import numpy as np
import copy

class Rotation(QuickPlugin):
    """docstring for Rotation."""

    data=ObjectProperty()
    bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
    # Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'demo.kv')

    def __init__(self):
        super(Rotation, self).__init__()
        self.input_type=['file_path']
        self.result_meta={
            'node_id':'result',
            'type':'table',
            'display':'table_viewer',}
        # self.kwargs=[
        # 	{'id':'min_val','type':'text_input','text':'100'},
        # 	{'id':'max_val','type':'text_input','text':'200'}]
    def on_task_finished(self,task):
        video,table=task.result()
        table={
            'node_id':'table',
            'type':'table',
            'display':'table_viewer',
            'content':table,
            'children':[]}
        video={
            'node_id':'video',
            'type':'img_stack',
            'display':'video_viewer',
            'content':video,
            'children':[]}
        self.selected_data['children']+=[video,table]
        self.property('data').dispatch(self)
        self.call_back()

    def run(self,img_path):
        video,table = run_tiff(img_path,self.progress_percent)
        return video,table


class Test(App):
    """docstring for Test."""

    data=ObjectProperty()
    plugins=DictProperty()

    def __init__(self):
        super(Test, self).__init__()

    def build(self):
        demo=Rotation()
        print(demo.data.select_idx)
        demo.data.select_idx = [0]
        demo.data.tree={'node_id':'img','children':[],'type':'file_path','content':'D:\onedrive\program/for_liuyuan_rotation\data/test.tiff'}
        return demo

if __name__ == '__main__':
    Test().run()
