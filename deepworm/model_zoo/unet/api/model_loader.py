import sys,os
sys.path.append(os.path.dirname(sys.path[0]))
from unet.unet import UNet

model=UNet().unet_net()
bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model.load_weights(bundle_dir+'/assets/unet.hdf5')
