import sys
import os

root_dir = os.path.abspath(os.path.dirname(__file__))

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
    print(f"Added {root_dir} to Python path")

print(f"Current Python path list: {sys.path}")