import sys
import os

root_dir = os.path.abspath(os.path.dirname(__file__))

if root_dir not in sys.path[1:]:
    sys.path.insert(1, root_dir)
    print("Added {} to Python path".format(root_dir))
else:
    print("Already in Python path: {}".format(root_dir))
