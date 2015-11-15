from qt import *
import string

from guimultilineedit import guiMultiLineEdit

TRUE=1
FALSE=0

class guiListEditor(guiMultiLineEdit):

  def keyPressEvent(self, e):
    if e.key()==Key_Return:
      pass
    elif e.key()==4103 and e.state()==16:
      line=self.cursorPosition()[0]
      self.emit(PYSIGNAL("lineRemoved"),(line,))
    else:
      QMultiLineEdit.keyPressEvent(self, e)

class guiSyncEdit(QSplitter):

  def __init__(self, *args):
    apply(QSplitter.__init__,(self,)+args)
    self.left=guiMultiLineEdit(self)
    self.left.setReadOnly(TRUE)
    self.right=guiListEditor(self)
    self.connect (self.right, PYSIGNAL("lineRemoved"), self.removeLine)
    self.keys=[]
    
  def append(self, key, text, val=""):
    self.keys.append(key)
    self.left.append(text)
    self.right.append(val)
    
  def removeLine(self, line):
    del self.keys[line]
    self.left.removeLine(line)
    self.right.removeLine(line)

  def contents(self):
    c=map( None
         , self.keys
         , string.split(self.left.text(),"\n")
         , string.split(self.right.text(),"\n")
         )
    return c

  def clear(self):
    self.keys=[]
    self.left.clear()
    self.right.clear()

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.1.1.1 $
    Last edited          : $Date: 2002/03/27 23:48:32 $
    
    CVS Log:         
    $Log: guisyncedit.py,v $
    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.2  2001/01/08 20:55:07  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
