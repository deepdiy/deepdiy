import sys,os

def get_parent_path(level=1):
    bundle_dir=os.path.abspath(__file__)
    for i in range(1,level):
        bundle_dir=os.path.dirname(bundle_dir)
    return bundle_dir
