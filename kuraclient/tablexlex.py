False = 0
True = 1

from qt import QGridLayout, QWidget, SIGNAL, Qt, QPushButton,\
     PYSIGNAL, QString

from kuragui.guicombobox import guiComboBox
from kuragui.guilabel import guiLabel
from kuragui.guimultilineedit import guiMultiLineEdit
from kuragui.guidetaillist import guiDetailList
from kuragui import constants

from dlglexrelation import dlgLexRelation


from kuralib import kuraapp

class formLexLex(QWidget):

    def __init__(self, parent):

        QWidget.__init__(self, parent)

        self.record = None
        self.lvi = None
    
        self.grdLexLex = QGridLayout(self)
        self.grdLexLex.setSpacing(6)
        self.grdLexLex.setMargin(11)

        self.lblForm = guiLabel(self,'lblValue')
        self.lblForm.setText('Value')

        self.txtForm = guiLabel(self, 'txtValue')
        self.txtForm.setFrameShadow(guiLabel.Sunken)
        self.txtForm.setFrameShape(guiLabel.Panel)

        self.cmbRelation = guiComboBox(self, "lng_lex")
        self.cmbRelation.initComboBox(kuraapp.app,
                                      "lng_lxlxrelcode",
                                      constants.INSERT,
                                      False,
                                      None)

        self.lblRelation = guiLabel(self,'lblRelation')
        self.lblRelation.setText('&Relation type')

        self.lblNote = guiLabel(self,'lblNote')
        self.lblNote.setText('&Note')
        self.lblNote.setAlignment(guiLabel.AlignTop | guiLabel.AlignLeft)

        self.txtNote = guiMultiLineEdit(self,'txtNote')

        self.lblUser = guiLabel(self,'lblUser')
        self.lblUser.setText('User')

        self.txtUser = guiLabel(self,'txtUser')
        self.txtUser.setFrameShadow(guiLabel.Sunken)
        self.txtUser.setFrameShape(guiLabel.Panel)

        self.lblDateStamp = guiLabel(self,'lblDateStamp')
        self.lblDateStamp.setText('Last changed')

        self.txtDatestamp = guiLabel(self,'txtDatestamp')
        self.txtDatestamp.setFrameShape(guiLabel.Panel)
        self.txtDatestamp.setFrameShadow(guiLabel.Sunken)
    
        self.lblRelation.setBuddy(self.cmbRelation)
        self.lblNote.setBuddy(self.txtNote)

        self.bnSave = QPushButton("&Apply", self)
        self.bnZoom = QPushButton("&Zoom", self)
              
        self.grdLexLex.addWidget(self.lblForm,0,0)
        self.grdLexLex.addWidget(self.txtForm,0,1)
        self.grdLexLex.addWidget(self.lblRelation,1,0)
        self.grdLexLex.addWidget(self.cmbRelation,1,1)
        self.grdLexLex.addWidget(self.lblNote,2,0)
        self.grdLexLex.addWidget(self.txtNote,2,1)
        self.grdLexLex.addWidget(self.lblUser,3,0)
        self.grdLexLex.addWidget(self.txtUser,3,1)
        self.grdLexLex.addWidget(self.lblDateStamp,4,0)
        self.grdLexLex.addWidget(self.txtDatestamp,4,1)
        self.grdLexLex.addWidget(self.bnSave, 0, 2)    
        self.grdLexLex.addWidget(self.bnZoom, 1, 2)
    
        self.connect(self.bnSave, SIGNAL("clicked()"), self.save)
        self.connect(self.bnZoom, SIGNAL("clicked()"), self.slotZoom)
    

    
    def slotZoom(self):
        from dlglexeme import dlgLexeme

        self.dlg = dlgLexeme(app = kuraapp.app,
                             parent = self,
                             title = "Lexeme: " + self.record.form_2,
                             firstTabTitle = "",
                             record = kurapp.app.getObject("lng_lex",
                                                           lexnr = self.record.lexnr_2),
                             mode = constants.UPDATE,
                             tableDef = kuraapp.app.getTableDef("lng_lex"))
        self.connect(self.dlg, PYSIGNAL("sigAcceptData"),
                     self.slotZoomAccept())
        self.dlg.show()

    def slotZoomAccept(self):
        rec = self.dlg.getMasterRecord()
        self.txtForm.setText(rec.form)
        self.record.form_2 = rec.form
        self.emit(PYSIGNAL("sigRecordUpdated"),(self.record, self.lvi))

    def setItem(self, record, lvi = None):
        self.setEnabled(True)
        self.record = record
        self.lvi = lvi
        
        self.txtForm.setText(record.form_2)
        self.cmbRelation.setCurrentItem(record.lxlxrelcode)
        self.txtNote.setText(record.note)
        self.txtUser.setText(record.user)
        self.txtDatestamp.setText(record.datestamp)

    def changeItem(self, record, lvi):
        self.clear()
        self.setItem(record, lvi)

    def clear(self):
        self.setEnabled(False)  
        self.record = None
        self.lvi = None
        self.txtForm.setText(QString())
        self.txtNote.setText(QString())
        self.txtUser.setText(QString())
        self.txtDatestamp.setText(QString())

    def newItem(self, parentRecord): 
        self.clear()
        self.setEnabled(True)
        record = kuraapp.app.createDefaultObject("lng_lex_lex",
                                                 lexnr_1 = parentRecord.lexnr,
                                                 form_1 = parentRecord.form)
        self.setItem(record)
        
    def save(self):
        if self.record != None:
            self.record.lxlxrelcode = self.cmbRelation.currentKey()
            self.record.relation = unicode(self.cmbRelation.currentText())
            self.record.note = self.txtNote.text()
            if self.lvi == None:
                try:
                    self.record.insert()
                    self.record = kuraapp.app.getObject("lng_lex_lex",
                                                     lxlxnr = self.record.lxlxgnr)
                    self.emit(PYSIGNAL("sigRecordInserted"),(self.record,))
                except dbError, dberr:
                    QMessageBox.information(self, "Kura Error while inserting",
                                          dberr.error)

            else:
                try:
                    self.record.update()
                    self.emit(PYSIGNAL("sigRecordUpdated"),(self.record,self.lvi))
                except dbError, dberr:
                    QMessageBox.information(self, "Kura Error while updating",
                                            dberr.error)

class tabLexLex(QWidget):

    def __init__(self, parent, app, parentRecord, *args):
        QWidget.__init__(self, parent, *args)

        self.grid = QGridLayout(self)
        self.grid.setSpacing(6)
        self.grid.setMargin(11)

        self.parentRecord = parentRecord

        self.dlsLexLex = guiDetailList(self, app, parentRecord,
                                       "lng_lex_lex")
        self.bnSelectForm = QPushButton('add &Set', self)
        self.frmLexLex = formLexLex(self)

        self.grid.addWidget(self.dlsLexLex, 0, 0)
        self.grid.addWidget(self.bnSelectForm, 0, 1, Qt.AlignTop)
        self.grid.addMultiCellWidget(self.frmLexLex, 1, 1, 0, 1)

        self.connect(self.dlsLexLex, PYSIGNAL("sigRecordSelected"),
                     self.frmLexLex.changeItem)
        self.connect(self.dlsLexLex, PYSIGNAL("sigItemDeleted"),
                     self.frmLexLex.clear)
        self.connect(self.frmLexLex, PYSIGNAL("sigRecordUpdated"),
                     self.dlsLexLex.slotUpdateItem)
        self.connect(self.frmLexLex, PYSIGNAL("sigRecordInserted"),
                     self.dlsLexLex.slotAddItem)
        self.connect(self.bnSelectForm, SIGNAL("clicked()"),
                     self.addSet)
        self.frmLexLex.clear()

    def addSet(self):
        self.dlg=dlgLexRelation(self, self.parentRecord)
        self.connect(self.dlg, PYSIGNAL("sigAcceptData"),
                     self.slotAddSetAccept)
        self.dlg.show()

    def slotAddSetAccept(self):
        self.dlsLexLex.refresh()



__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.8 $"""[11:-2]

__cvslog__="""
    $Log: tablexlex.py,v $
    Revision 1.8  2002/11/06 18:27:44  boud
    Added start of manual, fixed but with lexical relations.

    Revision 1.7  2002/07/30 15:38:41  boud
    ...

    Revision 1.6  2002/07/30 11:34:37  boud
    Fixes, fixes, fixes...

    Revision 1.5  2002/06/17 14:06:11  boud
    Interlinear texts are back + pychecker checks

    Revision 1.4  2002/06/14 13:44:09  boud
    We march on and on and on.

    Revision 1.3  2002/05/24 14:01:27  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
