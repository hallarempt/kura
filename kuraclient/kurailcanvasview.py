import sys

from qt import *
from qtcanvas import *
from kuragui.constants import *
from kuragui.guiconfig import guiConf

from dbobj.dbexceptions import dbRecordNotFoundException
from kuralib import kuraapp

from kurailcanvas import kuraIlCanvas

class kuraIlCanvasView(QCanvasView):
  
    def __init__(self, *args):
        apply(QCanvasView.__init__,(self, ) + args)
        self.setFocusPolicy(QWidget.StrongFocus)


    def contentsMouseDoubleClickEvent(self, ev):
        self.setFocus()
        item = self.canvas().setCursor(ev.pos())
        if item != None:
            self.emit(PYSIGNAL("sigDoubleClickOn"), (item,))

      
    def contentsDropEvent(self, ev):
        self.setFocus()
        item = self.canvas().setCursor(ev.pos())
        if item != None:
            self.emit(PYSIGNAL("sigDropEventOn"), (item,))

      
    def contentsMousePressEvent(self, ev):
        item = self.canvas().setCursor(ev.pos())
        if item != None:
            self.emit(PYSIGNAL("sigMousePressedOn"), (item,))

    def contentsMouseMoveEvent(self, ev):
        self.startDrag()
            

    def ensureVisible(self, item):
        QCanvasView.ensureVisible(self, item.x(), item.y())
    
    def startDrag(self):
        record = self.canvas().getCurrentItem().getRecord()
        drag = QTextDrag(str(record.getLink()), self)
        drag.dragCopy()
                     
    
               
__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.9 $"""[11:-2]
