#!/usr/bin/env python

#
# Lineedit control where only numeric input is allowed
#

from guilineedit import guiLineEdit
from qt import *


class guiNumberBox(guiLineEdit):

  def __init__(self, *args):
    apply(guiLineEdit.__init__,(self,)+args)
    self.setMaximumHeight(self.sizeHint().height())
    
  def setText(self, value):
    if value != None:
      guiLineEdit.setText(self, unicode(value))
    
  def text(self):
    if guiLineEdit.text(self)==None:
      return None
    else:  
      return int(unicode(guiLineEdit.text(self)))
    

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/10/19 11:09:21 $
    
    CVS Log:         
    $Log: guinumberbox.py,v $
    Revision 1.2  2002/10/19 11:09:21  boud
    Small fixes.

    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.5  2001/01/08 20:55:07  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
