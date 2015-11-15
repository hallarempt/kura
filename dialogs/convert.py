#!/usr/bin/env python

import glob
import os


for file in glob.glob("*.ui"):
    print "Processing", file
    os.system("pyuic -x %s -o ../kuraclient/%s.py" %
              (file, os.path.splitext(file)[0]))
