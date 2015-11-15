from qt import *

from kuragui.guicombobox      import guiComboBox
from kuragui.guilabel         import guiLabel
from kuragui.guilistbox       import guiListBox
from kuragui.guimultilineedit import guiMultiLineEdit
from kuragui.guilineedit      import guiLineEdit
from kuragui.guidetaillist    import guiDetailList
from kuragui.constants        import *
from resource                 import TRUE, FALSE
from kuralib import kuraapp

class formTextProjects(QWidget):

  def __init__(self, parent):

    QWidget.__init__(self, parent)

    self.record=None
    self.lvi=None
    
    self.grdProjects = QGridLayout(self)
    self.grdProjects.setSpacing(6)
    self.grdProjects.setMargin(11)

    self.cmbProjects = guiComboBox(self)
    self.cmbProjects.fillComboBox(self.record, "projectnr",INSERT)
    self.cmbProjects.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum,self.cmbProjects.sizePolicy().hasHeightForWidth()))
    
    self.lblProjects = guiLabel(self,'lblProjects')
    self.lblProjects.setText(self.tr('&Project'))
    self.lblProjects.setSizePolicy(QSizePolicy(1,1,self.lblProjects.sizePolicy().hasHeightForWidth()))

    self.lblProjects.setBuddy(self.cmbProjects)

    self.bnSave=QPushButton("&Apply", self)

    self.grdProjects.addWidget(self.lblProjects,0,0)
    self.grdProjects.addWidget(self.cmbProjects,0,1)
    self.grdProjects.addWidget(self.bnSave, 1, 0)

    
    self.connect(self.bnSave, SIGNAL("clicked()"), self.save)
    
  def setItem(self, record, lvi=None):
    self.setEnabled(TRUE)
    self.record=record
    self.lvi=lvi
    self.cmbProjects.fillComboBox(self.record, "projectnr",INSERT)

  def changeItem(self, record, lvi):
    self.clear()
    self.setItem(record, lvi)
    
  def clear(self):
    self.setEnabled(FALSE)  
    self.record=None
    self.lvi=None
    self.cmbProjects.fillComboBox(self.record, "projectnr",INSERT)
  
  def newItem(self, parentRecord): 
    self.clear()
    self.setEnabled(TRUE)
    record = kuraapp.app.createDefaultObject("lng_proj_text",
                                             textnr=parentRecord.textnr,
                                             text=parentRecord.title)
    self.setItem(record)
    
  def save(self):
    if self.record!=None:
      self.record.projectnr=self.cmbProjects.currentKey()
      self.record.project=unicode(self.cmbProjects.currentText())

      if self.lvi==None:
        try:
          self.record.insert()
          self.emit(PYSIGNAL("sigRecordInserted"),(self.record,))
        except dbError, dberr:
          QMessageBox.information(self, "Kura Error while inserting", dberr.error)

      else:
        try:
          self.record.update()
          self.emit(PYSIGNAL("sigRecordUpdated"),(self.record,self.lvi))
        except dbError, dberr:
          QMessageBox.information(self, "Kura Error while updating", dberr.error)

class tabTextProjects(QWidget):

  def __init__(self, parent, app, parentRecord, *args):
    QWidget.__init__(self, parent)

    self.grid = QGridLayout(self)
    self.grid.setSpacing(6)
    self.grid.setMargin(11)
    
    self.dlsProjects=guiDetailList(self, app, parentRecord, "lng_proj_text")
    self.frmTextProject=formTextProjects(self)
    
    self.grid.addWidget(self.dlsProjects, 0, 0)
    self.grid.addWidget(self.frmTextProject, 1, 0)

    self.connect(self.dlsProjects, PYSIGNAL("sigRecordSelected"), self.frmTextProject.changeItem)
    self.connect(self.dlsProjects, PYSIGNAL("sigItemDeleted"),    self.frmTextProject.clear)
    self.connect(self.dlsProjects, PYSIGNAL("sigCreateNewItem"),  self.frmTextProject.newItem)
    self.connect(self.frmTextProject, PYSIGNAL("sigRecordUpdated"),  self.dlsProjects.slotUpdateItem)
    self.connect(self.frmTextProject, PYSIGNAL("sigRecordInserted"), self.dlsProjects.slotAddItem)    
    self.frmTextProject.clear()

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/06/17 14:06:11 $
    
    CVS Log:         
    $Log: tabtextprojects.py,v $
    Revision 1.2  2002/06/17 14:06:11  boud
    Interlinear texts are back + pychecker checks

    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:47  boud
    Manu changes.

    Revision 1.2  2001/01/08 20:55:06  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
