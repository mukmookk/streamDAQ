import sys
import os

root_dir = os.path.abspath(os.path.dirname(__file__))

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
    print("Added {} to Python path".format(root_dir))

print("Already in Python path: {}".format(root_dir))