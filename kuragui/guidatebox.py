#!/usr/bin/env python

#
# Lineedit that checks whether the string entered is a valid data/time
#
from guiconfig import guiConfig
from guilineedit import guiLineEdit

class guiDateBox(guiLineEdit):

  def __init__(self, *args):
    apply(guiLineEdit.__init__,(self,)+args)
    self.setFont(guiConfig.font)
    self.setMaximumHeight(self.sizeHint().height())
__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.1.1.1 $
    Last edited          : $Date: 2002/03/27 23:48:32 $
    
    CVS Log:         
    $Log: guidatebox.py,v $
    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.3  2001/01/08 20:55:06  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
