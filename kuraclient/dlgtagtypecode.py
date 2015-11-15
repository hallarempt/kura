True = 1
False = 0

from qt import PYSIGNAL

from kuragui.guilistview import guiListView
from kuragui.guidetaillist import guiDetailList
from kuragui import constants

from frmtagtypecode import frmtagtypecode

class dlgTagTypeCode(frmtagtypecode):

    def __init__(self, app, parent,
                 title, firstTabTitle, record, mode,
                 tableDef, showChildren = False):
        
        frmtagtypecode.__init__(self, parent = parent, modal = True)
        self.record = record
        self.mode = mode
        self.txtTypeCode.setText(self.record.tagtypecode)
        self.txtDescription.setText(self.record.description)
        
        if self.mode == constants.SEARCH:
            self.rdbDomain.setEnabled(False)
            self.rdbValue.setEnabled(False)
            self.rdbNote.setEnabled(False)
            self.rdbReference.setEnabled(False)
        else:
            self.rdbDomain.setChecked(int(self.record.isdomain))
            self.rdbValue.setChecked(int(self.record.isvalue))
            self.rdbNote.setChecked(int(self.record.isnote))
            self.rdbReference.setChecked(int(self.record.isreference))
  
    def apply(self):
        try:
            self.record.tagtypecode = unicode(self.txtTypeCode.text())
            self.record.description = unicode(self.txtDescription.text())
            self.record.isdomain = self.rdbDomain.isChecked()
            self.record.isvalue = self.rdbValue.isChecked()
            self.record.isnote = self.rdbNote.isChecked()
            self.record.isreference = self.rdbReference.isChecked()

            if self.mode == constants.INSERT:
                self.record.insert()
                self.emit(PYSIGNAL("sigAcceptNewData"),(self.record,))
                self.mode == constants.UPDATE
            elif self.mode == constants.UPDATE:
                self.record.update()
                self.emit(PYSIGNAL("sigAcceptData"),(self.record,))
            elif self.mode == constants.SEARCH:
                self.record.isdomain = None
                self.record.isnote = None
                self.record.isvalue = None
                self.record.isreference = None

            return True
        except:
            return False
    
    def accept(self):
        if self.apply() == True:

            frmtagtypecode.accept(self)
    
    def getMasterRecord(self):
        return self.record    
     
__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.3 $"""[11:-2]

__cvslog__="""
    $Log: dlgtagtypecode.py,v $
    Revision 1.3  2002/11/16 12:37:00  boud
    Some fixes (fields=None ipv fields={}), finished documentation.

    Revision 1.2  2002/05/23 18:31:16  boud
    Converted some dialogs.

 ***************************************************************************/
"""
