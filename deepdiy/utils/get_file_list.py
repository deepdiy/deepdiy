import glob,os

def get_file_list(path,formats=['*']):
	file_list=[]
	for format in formats:
		file_list.extend(glob.glob(path + os.sep + '*.'+format))
	file_list=sorted(file_list,key=len)
	return file_list

if __name__ == '__main__':
	path1='../img/'
	path2='../img/face.jpg'
	file_list=get_file_list(path1,formats=['jpg'])
	print(file_list)
