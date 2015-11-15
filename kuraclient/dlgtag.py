from qt import *

from kuragui.guicombobox      import guiComboBox
from kuragui.guilabel         import guiLabel
from kuragui.guilistbox       import guiListBox
from kuragui.guimultilineedit import guiMultiLineEdit
from kuragui.guilineedit      import guiLineEdit
from kuragui.guidetaillist    import guiDetailList
from kuragui.constants        import *
from kuragui.guidialog        import guiDialog

from kuragui.guiconfig import guiConf

from kuracmbtags              import kuraCmbTags
from kuracmbtagvalues         import kuraCmbTagValues

from resource                 import TRUE, FALSE

from dbobj.dbexceptions       import *

class wdgTag(QWidget):

  def __init__(self, parent, parentTableName, record):
    QWidget.__init__(self, parent)

    self.parentTableName=parentTableName
    self.record=record
    self.tableName=record.table

    if self.record.getPrimaryKey()==None:
      self.mode=INSERT
    else:
      self.mode=UPDATE

    
    self.grdTags = QGridLayout(self)
    self.grdTags.setSpacing(6)
    self.grdTags.setMargin(11)

    self.cmbTags = kuraCmbTags(self, parentTableName)
    self.lblTags = guiLabel(self,'lblTags')
    self.lblTags.setText(self.tr('&Tag'))

    self.lblValue = guiLabel(self,'lblValue')
    self.lblValue.setText(self.tr('&Value'))

    self.cmbTagValues = kuraCmbTagValues(self, self.tableName)

    self.lblNote = guiLabel(self,'lblNote')
    self.lblNote.setText(self.tr('&Note'))
    self.lblNote.setAlignment(guiLabel.AlignTop | guiLabel.AlignLeft)

    self.txtNote = guiMultiLineEdit(self,'txtNote')

    self.lblUser = guiLabel(self,'lblUser')
    self.lblUser.setText(self.tr('User'))

    self.txtUser = guiLabel(self,'txtUser')
    self.txtUser.setFrameShadow(guiLabel.Sunken)
    self.txtUser.setFrameShape(guiLabel.Panel)

    self.lblDateStamp = guiLabel(self,'lblDateStamp')
    self.lblDateStamp.setText(self.tr('Last changed'))

    self.txtDatestamp = guiLabel(self,'txtDatestamp')
    self.txtDatestamp.setFrameShape(guiLabel.Panel)
    self.txtDatestamp.setFrameShadow(guiLabel.Sunken)
    
    self.lblTags.setBuddy(self.cmbTags)
    self.lblValue.setBuddy(self.cmbTagValues)
    self.lblNote.setBuddy(self.txtNote)
    
    self.grdTags.addWidget(self.lblTags,0,0)
    self.grdTags.addWidget(self.cmbTags,0,1)
    self.grdTags.addWidget(self.lblValue,1,0)
    self.grdTags.addWidget(self.cmbTagValues,1,1)
    self.grdTags.addWidget(self.lblNote,2,0)
    self.grdTags.addWidget(self.txtNote,2,1)
    self.grdTags.addWidget(self.lblUser,3,0)
    self.grdTags.addWidget(self.txtUser,3,1)
    self.grdTags.addWidget(self.lblDateStamp,4,0)
    self.grdTags.addWidget(self.txtDatestamp,4,1)

    self.connect(self.cmbTags, PYSIGNAL("recSelected"),self.cmbTagValues.slotRefresh)
    self.cmbTags.setCurrentItem(record.tag)
    self.cmbTagValues.slotRefresh(record.tag)
    if record.value != None:
      self.cmbTagValues.slotSetCurrentItem(record.value)
    self.txtNote.setText(record.note)
    self.txtUser.setText(record.user)
    self.txtDatestamp.setText(str(record.datestamp))

    self.setTabOrder(self.cmbTags,self.cmbTagValues)
    self.setTabOrder(self.cmbTagValues,self.txtNote)

  def save(self):
    """
    FIXME: Refactor and integrate with guidialog. There's duplicated
    code in here.
    """
    if self.record!=None:
      self.record.tag=self.cmbTags.currentKey()
      self.record.tagname=unicode(self.cmbTags.currentText())

      if self.cmbTagValues.isEnabled()==TRUE:
        self.record.value=self.cmbTagValues.currentKey()
        self.record.description=unicode(self.cmbTagValues.currentText())
      else:
        self.record.description=unicode(self.txtNote.text())[:200]
      self.record.note=self.txtNote.text()
     
      if self.mode==INSERT:
        try:
          self.record.insert()
          self.emit(PYSIGNAL("sigRecordInserted"),(self.record,))
          self.mode=UPDATE
        except dbError, dberr:
          QMessageBox.information(self, "Kura Error while inserting", dberr.errorMessage)
      else:
        try:
          self.record.update()
          self.emit(PYSIGNAL("sigRecordUpdated"),(self.record,))
        except dbError, dberr:
          QMessageBox.information(self, "Kura Error while updating", dberr.errorMessage)

class dlgTag(QTabDialog):
  
  def __init__(self, parent, title, parentTableName, record):
    QTabDialog.__init__(self, parent, str(title), TRUE, Qt.WStyle_DialogBorder)
    self.title=title
    self.accepted=FALSE
    self.record=record
    
    self.setApplyButton()
    self.connect(self, SIGNAL("applyButtonPressed()")
                     , self.slotApplyButtonPressed)
    self.setCaption(title)
    self.setCancelButton("&Cancel")
    self.setOkButton()

    self.tabTag=wdgTag(self, parentTableName, self.record)
    QTabDialog.addTab(self, self.tabTag, title)

    try: 
      w=getattr(guiConf, record.table + "_w")
      h=getattr(guiConf, record.table + "_h")
      self.resize(QSize(w, h))
    except:
      self.resize(self.minimumSize())

  def slotAcceptData(self):
    self.tabTag.save()
    self.record=self.tabTag.record
    self.emit(PYSIGNAL("sigAcceptData"), (self.record,))
    return TRUE

  def slotApplyButtonPressed(self):
    self.accepted=self.slotAcceptData()
     
  def accept(self):
    self.saveSize()
    if self.accepted:
      QDialog.accept(self)
    
  def reject(self):
    self.saveSize()
    QDialog.reject(self)
    
  def saveSize(self):
    setattr(guiConf, self.record.table + "_w", self.width())
    setattr(guiConf, self.record.table + "_h", self.height())
  
  def getMasterRecord(self):
    return self.record
    


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.7 $"""[11:-2]
