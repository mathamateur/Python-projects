import argparse
from . import awkpp
import os

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename is a file name which "
                                     "contains information about file "
                                     "that you want to explore and "
                                     "special commands to agregate data. "
                                     "The format is .awkpp")
args = parser.parse_args()
ext = os.path.splitext(args.filename)[-1].lower()
if not os.path.exists(args.filename):
    print('No such file!')
elif ext != '.awkpp':
    print(f'Invalid extension. It should be a .awkpp, not a {ext}')
elif not os.access(args.filename, os.R_OK):
    print('Permission denied!')
else:
    awkpp.aggregate(args.filename)
