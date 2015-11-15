#!/usr/bin/env python

from distutils.core import setup
from distutils import sysconfig

import sys

try:
    import qt
except:
    print """Could not import the PyQt library. Please install it. The
source for PyQt can be found at: http://www.riverbankcomputing.co.uk."""
    sys.exit(1)

print "PyQt is installed"

if int(qt.QT_VERSION_STR[0]) < 3:
    print """Kura does not work with a Qt library with a version < 3.0.0
Please upgrade your Qt library. The source for Qt can be found at:
http://www.trolltech.com"""

print "Qt is recent enough"

if hasattr(sys, 'setappdefaultencoding'):
    sys.setappdefaultencoding('utf-8')
elif sys.getdefaultencoding() != 'utf-8':
    print """Warning: encoding not set for unicode - copy sitecustomize.py to 
/usr/local/lib/python/site-packages"""


setup(name = "kura",
      version = "2.0",
      description = "Kura -- the opensource linguistics database",
      author = "Boudewijn Rempt",
      author_email = "boud@valdyas.org",
      url = "http://www.valdyas.org/linguistics",
      packages = ["dbobj", "dbobj/textdb", "kuraclient",
                  "kuragui", "kuralib",
                  "utils", ""],
      data_files = [("pixmaps",
                     ["pixmaps/edit.png",
                     "pixmaps/fileimport.png",
                     "pixmaps/folder_new.png",
                     "pixmaps/abort.png",
                     "pixmaps/editdelete.png",
                     "pixmaps/filenew.png",
                     "pixmaps/insert_stream.png",
                     "pixmaps/cell_edit.png",
                     "pixmaps/fileclose.png",
                     "pixmaps/fileprint.png",
                     "pixmaps/insertcell.png",
                     "pixmaps/connect_creating.png",
                     "pixmaps/fileexport.png",
                     "pixmaps/filesave.png",
                     "pixmaps/project_open.png",
                     "pixmaps/done.png",
                     "pixmaps/filefind.png",
                     "pixmaps/filesaveas.png",
                     "pixmaps/removecell.png"]),
                    ("",
		      ["kura.jpg",
                       "template.dbobj",
                       "example.dbobj",
                       "sitecustomize.py",
                       "kura.py",
                       "test.dbobj"]),
                    ("doc",
                      ["doc/manual.pdf",
                       "doc/script1.py",
                       "doc/script2.py",
                       "doc/script3.py",
                       "doc/script4.py",
                       "doc/script5.py",
                       "doc/lexicon.csv"]),
                    ("datamodel",
                     ["datamodel/config.sql"])
                    ],
      scripts = ["kura"],
      long_description = """Kura

Kura is an extensible database application meant for the handling
of language data. You can store words in a lexicon, recordings,
manuscript scans and interlinearly glossed texts.

This data can be used to generate gramamrs of papers or to do
research on the languages.""")

