import sys,os
sys.path.append('../../../')

def get_network():
	from model_zoo.unet.unet.unet import UNet
	network=UNet().unet_net()
	return network

def test():
	model=run()

if __name__ == '__main__':
	test()
