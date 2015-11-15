#!/usr/bin/env python

#
# label with the correct minimumsize
#

from qt import *

class guiLabel(QLabel):

  def __init__(self, *args):
    apply(QLabel.__init__,(self,)+args)
    self.setAlignment(Qt.AlignTop or Qt.AlignLeft or Qt.WordBreak)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.1.1.1 $
    Last edited          : $Date: 2002/03/27 23:48:32 $
    
    CVS Log:         
    $Log: guilabel.py,v $
    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.2  2001/01/08 20:55:07  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
