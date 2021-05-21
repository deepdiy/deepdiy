# coding:utf-8

from setuptools import setup,Command
import subprocess
import distutils.cmd
import os
from setuptools import setup
from setuptools.command.install import install

import atexit
from setuptools.command.install import install


def _post_install():
	os.system('pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew')
	os.system('pip install kivy')
	os.system('garden install --kivy matplotlib')
	print('FINISHED')


class new_install(install):
	def __init__(self, *args, **kwargs):
		super(new_install, self).__init__(*args, **kwargs)
		atexit.register(_post_install)


setup(
	name='deepdiy',
	version='1.0',
	description='Setup for DeepDIY',
	author='huoty',
	author_email='pubrcv@163.com',
	url='https://www.deepdiy.net',
	# packages=['deepdiy'],
	install_requires=[
		'tensorflow==2.5.0',
		'Keras>=2.1',
		'opencv-python',
		'Numpy>=1.15.4',
		'Scipy>=1.1.0',
		'Matplotlib>=3.0.2',
		'pebble',
		'pysnooper',
		'rootpath'
	],
	cmdclass={
	'install': new_install,
	}
)
