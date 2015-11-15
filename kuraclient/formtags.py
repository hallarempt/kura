False = 0
True = 1

from qt import *
from dbobj import dbexceptions
from kuragui.guilabel import guiLabel
from kuragui.guimultilineedit import guiMultiLineEdit
from kuragui.guidetaillist    import guiDetailList

from kuracmbtags import kuraCmbTags
from kuracmbtagvalues import kuraCmbTagValues

from kuralib import kuraapp

class FormTags(QWidget):

    def __init__(self, parent, parentTableName, tagTableName):

        QWidget.__init__(self, parent)

        self.parentTableName = parentTableName
        self.tagTableName = tagTableName
        
        self.record = None
        self.lvi = None

        self.grdTags = QGridLayout(self)
        self.grdTags.setSpacing(6)
        self.grdTags.setMargin(11)

        self.cmbTags = kuraCmbTags(self, parentTableName)
        self.lblTags = guiLabel(self,'lblTags')
        self.lblTags.setText(self.tr('&Tag'))

        self.lblValue = guiLabel(self,'lblValue')
        self.lblValue.setText(self.tr('&Value'))

        self.cmbTagValues = kuraCmbTagValues(self, tagTableName)

        self.lblNote = guiLabel(self,'lblNote')
        self.lblNote.setText(self.tr('&Note'))
        self.lblNote.setAlignment(guiLabel.AlignTop | guiLabel.AlignLeft)

        self.txtNote = guiMultiLineEdit(self,'txtNote')

        self.lblDateStamp = guiLabel(self,'lblDateStamp')
        self.lblDateStamp.setText(self.tr('Last changed'))

        self.txtDatestamp = guiLabel(self,'txtDatestamp')
        self.txtDatestamp.setFrameShape(guiLabel.Panel)
        self.txtDatestamp.setFrameShadow(guiLabel.Sunken)

        self.lblTags.setBuddy(self.cmbTags)
        self.lblValue.setBuddy(self.cmbTagValues)
        self.lblNote.setBuddy(self.txtNote)
        self.bnSave = QPushButton("&Save", self)

        self.grdTags.addWidget(self.lblTags,0,0)
        self.grdTags.addWidget(self.cmbTags,0,1)
        self.grdTags.addWidget(self.lblValue,1,0)
        self.grdTags.addWidget(self.cmbTagValues,1,1)
        self.grdTags.addWidget(self.lblNote,2,0)
        self.grdTags.addWidget(self.txtNote,2,1)
        self.grdTags.addWidget(self.lblDateStamp,4,0)
        self.grdTags.addWidget(self.txtDatestamp,4,1)
        self.grdTags.addWidget(self.bnSave, 0, 2)

        self.connect(self.cmbTags, PYSIGNAL("recSelected"),
                     self.cmbTagValues.slotRefresh)
        self.connect(self.bnSave, SIGNAL("clicked()"),
                     self.save)


    def setItem(self, record, lvi = None):
        self.setEnabled(True)
        self.record = record
        self.lvi = lvi
        self.cmbTags.setCurrentItem(record.tag)
        self.cmbTagValues.slotRefresh(record.tag)
        self.cmbTagValues.slotSetCurrentItem(record.value)
        self.txtNote.setText(record.note)
        self.txtDatestamp.setText(str(record.datestamp))

    def changeItem(self, record, lvi):
        self.clear()
        self.setItem(record, lvi)

    def clear(self):
        self.setEnabled(False)  
        self.record = None
        self.lvi = None
        self.cmbTags.refresh()
        self.cmbTagValues.clear()
        self.txtNote.setText(QString())
        self.txtDatestamp.setText(QString())


    def newItem(self, parentRecord): 
        self.clear()
        self.setEnabled(True)

        relation = parentRecord.tableDef.childtables[self.tagTableName]
        newRecord = kuraapp.app.createDefaultObject(self.tagTableName)
        newRecord.setFieldValue(newRecord.getDescriptorColumnName(relation.keys.foreign),
                                parentRecord.getDescription())

        newRecord.setFieldValue(relation.keys.foreign,
                                parentRecord.getFieldValue(relation.keys.local))
        self.setItem(newRecord)
    
    def save(self):
        if self.record == None:
            return
        
        self.record.tag = self.cmbTags.currentKey()
        self.record.tagname = unicode(self.cmbTags.currentText())

        if self.cmbTagValues.isEnabled() == True:
            self.record.value = self.cmbTagValues.currentKey()
            self.record.description = unicode(self.cmbTagValues.currentText())
        else:
            self.record.value = unicode(self.txtNote.text())[:200]
        self.record.note = self.txtNote.text()
     
        if self.record.getPrimaryKey() == None:
            try:
                self.record.insert()
                self.emit(PYSIGNAL("sigRecordInserted"), (self.record,))
            except dbexceptions.dbError, dberr:
                QMessageBox.information(self,
                                        "Kura Error while inserting",
                                        dberr.errorMessage)

        else:
            try:
                self.record.update()
                self.emit(PYSIGNAL("sigRecordUpdated"),(self.record, self.lvi))
            except dbexceptions.dbError, dberr:
                QMessageBox.information(self,
                                        "Kura Error while updating",
                                        dberr.errorMessage)
        self.clear()

class TagsTab(QWidget):

    def __init__(self, parent, app, parentRecord, tagTableName, *args):
        QWidget.__init__(self, parent, *args)
        self.grid = QGridLayout(self)
        self.grid.setSpacing(6)
        self.grid.setMargin(11)
        self.buttongrid = QVBoxLayout()
        
        self.dlsTags = guiDetailList(self, app, parentRecord, tagTableName)
        self.bnAdd = QPushButton("&Add", self)
        self.bnDelete = QPushButton("&Delete", self)
        self.formTags = FormTags(self, parentRecord.table, tagTableName)
    
        self.grid.addWidget(self.dlsTags, 0, 0)
        self.buttongrid.addWidget(self.bnAdd)
        self.buttongrid.addWidget(self.bnDelete)
        self.grid.addLayout(self.buttongrid, 0, 1)
        self.grid.addMultiCellWidget(self.formTags, 1, 1, 0, 1)


        self.connect(self.bnAdd,
                     SIGNAL("clicked()"),
                     self.dlsTags.slotNewItem)
        self.connect(self.bnDelete,
                     SIGNAL("clicked()"),
                     self.dlsTags.slotDeleteItem)
        self.connect(self.dlsTags,
                     PYSIGNAL("sigRecordSelected"),
                     self.formTags.changeItem)
        self.connect(self.dlsTags,
                     PYSIGNAL("sigItemDeleted"),
                     self.formTags.clear)
        self.connect(self.dlsTags,
                     PYSIGNAL("sigCreateNewItem"),
                     self.formTags.newItem)
        self.connect(self.formTags,
                     PYSIGNAL("sigRecordUpdated"),
                     self.dlsTags.slotUpdateItem)
        self.connect(self.formTags,
                     PYSIGNAL("sigRecordInserted"),
                     self.dlsTags.slotAddItem)    
        self.formTags.clear()



__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.11 $"""[11:-2]
