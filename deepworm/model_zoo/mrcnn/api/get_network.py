import sys,os
sys.path.append('../../../')
# sys.path.append('../')
from utils.get_parent_path import get_parent_path
bundle_dir=get_parent_path(3)+os.sep+'model_zoo'+os.sep+'mrcnn'
sys.path.append(bundle_dir)
from mrcnn.config import Config



class ElegansConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "elegans"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + elegans

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

config = ElegansConfig()
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

def get_network():
    print('hi')
    from mrcnn import model as modellib
    model = modellib.MaskRCNN(mode="inference", model_dir='./',config=config)
    # model.load_weights(bundle_dir+os.sep+'assets'+os.sep+'elegans.h5', by_name=True)
    return model

def test():
    get_network()

if __name__ == '__main__':
    test()
