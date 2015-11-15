#!/usr/bin/env python

#
# listbox with key-to-index and index-to-key mapping
#
from qt import *

class guiListBox(QListBox):

    def __init__(self, *args):
        QListBox.__init__(self, *args)
        self.data2key = {}
        self.key2data = {}
        self.connect(self, SIGNAL("selected(int)"), self.slotItemSelected)

    def insertItem(self, text, index):
        QListBox.insertItem(self, text)
        self.data2key[self.count() - 1] = index
        self.key2data[index] = self.count() - 1
    
    def currentKey(self):
        return self.data2key[self.currentItem()]
    
    def setCurrentItem(self, index):
        if self.key2data.has_key(index):
            QListBox.setCurrentItem(self, self.key2data[index])
  
    def slotItemSelected(self, index):
        rec = self.currentKey()
        val = self.currentItem()
        self.emit( PYSIGNAL("recSelected"),(rec, val) )

    def removeItem(self, index):
        del self.data2key[self.currentItem()]
        del self.key2data[index]
        QListBox.removeItem(self, index)
        
__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.3 $
    Last edited          : $Date: 2002/06/17 14:06:13 $
    
    CVS Log:         
    $Log: guilistbox.py,v $
    Revision 1.3  2002/06/17 14:06:13  boud
    Interlinear texts are back + pychecker checks

    Revision 1.2  2002/05/24 14:01:29  boud
    Converted most files to new coding standards + new config standard.

    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.3  2001/01/08 20:55:07  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
