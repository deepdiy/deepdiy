import glob,os

def get_file_list(path):
	file_list=[]
	for fn in glob.glob( path + os.sep + '*.jpg' )+glob.glob( path + os.sep + '*.png' )+glob.glob( path + os.sep + '*.tif' ):
		if os.path.isdir(fn):
			pass
		else:
			file_list.append(fn)
	file_list=sorted(file_list,key=len)
	return file_list

def path2tree(path):
	tree={'node_id':os.path.basename(path),'children':[]}
	if os.path.isdir(path):
		file_list=get_file_list(path)
		for file in file_list:
			file_name=file
			tree['children'].append({'node_id':file_name.split(os.sep)[-1],'children':[]})
	return tree

if __name__ == '__main__':
	path1='D:\onedrive\program\worm_analyst/training\mask_rcnn\Mask_RCNN\dataset/train\img'
	path2='D:\onedrive\program\worm_analyst/training\mask_rcnn\Mask_RCNN\dataset/train\img/training (1).tif'
	file_list=get_file_list(path1)
	print(file_list)
	print(path2tree(path1))
