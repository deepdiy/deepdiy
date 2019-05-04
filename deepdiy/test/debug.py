from kivy.app import App
import threading
import os,json


def import_tf():
	import tensorflow as tf
	graph = tf.get_default_graph()
	print('333333333333333333333')

# def open():
# 	app.widget_manager.ids.processing_screens.current='files'

def load_demo():
	app.widget_manager.ids.processing_screens.current='files'
	app.widget_manager.ids.processing_screens.children[0].children[0].add_to_tree('D:\onedrive\program\worm_analyst\demo_img\elegans')
	app.widget_manager.ids.processing_screens.current='networks'

def load_network():
	networks=app.widget_manager.ids.processing_screens.children[0].children[0]
	networks.ids.model_spinner.text='mrcnn'
	networks.ids.weight_spinner.text='mask_rcnn_balloon_0300.h5'
	networks.ids.config_spinner.text='ecoli.json'
	# print(networks.ids)

	# threading.Thread(target=import_tf).start()
def load_ecoli():
	app.widget_manager.ids.processing_screens.current='files'
	app.widget_manager.ids.processing_screens.children[0].children[0].add_to_tree('D:\onedrive\program\deepdiy\datasets\ecoli')
	app.widget_manager.ids.processing_screens.current='networks'

def load_train():
	app.widget_manager.ids.processing_screens.current='train'

def load_coco():
	app.widget_manager.ids.processing_screens.current='files'
	app.widget_manager.ids.processing_screens.children[0].children[0].add_to_tree(os.sep.join(['plugins','processing','gallery','demos','Mask-RCNN+COCO_instance_segmentation','images']))
	app.widget_manager.ids.processing_screens.current='networks'
	json_path=os.sep.join(['plugins','processing','gallery','demos','Mask-RCNN+COCO_instance_segmentation','config.json'])
	f=open(json_path,'r')
	demo_config=json.load(f)
	networks=app.widget_manager.ids.processing_screens.children[0].children[0]
	networks.ids.model_spinner.text=demo_config['model']
	networks.ids.weight_spinner.text=demo_config['weight']
	networks.ids.config_spinner.text=demo_config['config']

def debug():
	global app
	app=App.get_running_app()
	# open()
	# load_ecoli()
	# load_network()
	# load_train()
	load_coco()
