True = 1
False = 0

from qt import QTabDialog, Qt, PYSIGNAL, SIGNAL, \
     QSize, QDialog, QMessageBox

from dbobj import dbexceptions
import time
from guiconfig import guiConf

import constants

class guiDialog(QTabDialog):

    def __init__(self, parent, title, mode, hint):
        QTabDialog.__init__(self, parent, title, True, Qt.WStyle_DialogBorder)
        self.title = title
        self.setApplyButton()
        self.connect(self, SIGNAL("applyButtonPressed()"),
                     self.slotApplyButtonPressed)
        self.setSizeGripEnabled(True)
        self.setOkButton()
        self.accepted = False
        self.hint = hint
        self.mode = mode
        self.tabs = []
        
        self.setCaption(title)
        self.setCancelButton("&Cancel")
    
        if self.hint != None and self.hint != "":
            self.setHelpButton()
            self.connect(self, SIGNAL("helpButtonPressed()"),
                         self.slotHelp)

        self.resize(self.minimumSize())

    def slotApplyButtonPressed(self):
        self.accepted = self.slotAcceptData()
      
    def accept(self):
        if self.accepted:
            QDialog.accept(self)
    
    def reject(self):
        QDialog.reject(self)
    
    def addChildTab(self, title, tabForm, record, type = constants.MASTER):
        QTabDialog.addTab(self, tabForm, title)
        self.tabs.append((tabForm, record))
    
    def slotAcceptData(self):
        tabForm=self.tabs[0][0]
        rec = self.tabs[0][1]
        for field, fieldDef in tabForm.fieldList:
            if fieldDef.readonly:
                continue
            elif fieldDef.relation <> None: #combobox
                if field == "usernr":
                    rec.updateUser()
                else:
                    rec.setFieldValue(rec.getDescriptorColumnName(field),
                                      tabForm.getFieldText(field))
                    fieldDef.default = tabForm.getFieldValue(field)
                    rec.setFieldValue(field, tabForm.getFieldValue(field))
            else:
                rec.setFieldValue(field, tabForm.getFieldValue(field))
            #print "Type ", type(getattr(rec, field))
        if self.mode == constants.INSERT:
            try:
                rec.insert()
                self.mode = constants.UPDATE
            except dbexceptions.dbError, dberr:
                QMessageBox.information(self, "Kura Error while inserting"
                                        , dberr.errorMessage)
                return False
            self.emit(PYSIGNAL("sigAcceptNewData"), (rec,))

            self.mode = constants.UPDATE
        elif self.mode == constants.UPDATE:
            try:
                rec.update()
            except dbexceptions.dbError, dberr:
                QMessageBox.information(self, "Kura Error while updating"
                                        , dberr.errorMessage)
                return False
            self.emit(PYSIGNAL("sigAcceptUpdatedData"),(rec,))
        self.emit(PYSIGNAL("sigAcceptData"),(rec,))
        return True
    
    def getMasterRecord(self):
        return self.tabs[0][1]
      
    def slotHelp(self):
        QMessageBox.information(self, "About " + 
                                self.firstTabTitle.replace("&",""), self.hint)
        
__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.13 $
    Last edited          : $Date: 2002/12/28 21:44:56 $
 ***************************************************************************/
"""
