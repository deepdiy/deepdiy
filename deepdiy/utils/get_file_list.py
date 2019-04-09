import glob,os

def get_file_list(path):
	file_list=[]
	for fn in glob.glob( path + os.sep + '*.*'):
		if os.path.isdir(fn):
			pass
		else:
			file_list.append(fn)
	file_list=sorted(file_list,key=len)
	return file_list

if __name__ == '__main__':
	path1='../img/'
	path2='../img/face.jpg'
	file_list=get_file_list(path1)
	print(file_list)
