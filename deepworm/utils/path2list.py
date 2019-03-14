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


if __name__ == '__main__':
	print('hi')
	file_list=get_file_list('./')
	print(file_list)
