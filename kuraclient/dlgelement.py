import sys

from qt import *

from kuralib import kuraapp
from kuralib.lng_lex import *
  
from kuragui.guitabdialog  import guiTabDialog
from kuragui.guilistview   import guiListView
from kuragui.guidetaillist import guiDetailList
from kuragui.guicombobox   import guiComboBox
from kuragui.constants     import *
from kuragui.guilineedit   import guiLineEdit
from kuragui.guiconfig import guiConf

from formtags import TagsTab
from wdglexeme             import tabLexeme
from dlglexeme             import dlgLexeme
from dlglexchooser         import dlgLexChooser
from resource import *

from dbobj.dbexceptions import dbError

class tabElementSplit(QWidget): 

  def __init__(self, parent, parentRecord):
    QWidget.__init__(self, parent)
    self.parentRecord=parentRecord
    
    wdgElementLayout = QGridLayout(self)
    wdgElementLayout.setSpacing(6)
    wdgElementLayout.setMargin(11)

    self.lblElement = QLabel(self,'lblElement')
    self.lblElement.setText("Separate the morphemes with a dot.")
    wdgElementLayout.addWidget(self.lblElement,0,0)
    
    self.txtElement = guiLineEdit(self)
    self.txtElement.setFont(guiConf.widgetfont)
    self.txtElement.setText(parentRecord.getFieldValue("text"))
    wdgElementLayout.addWidget(self.txtElement,0,1)
    
    self.lblSubType=QLabel(self)
    self.lblSubType.setText("Type")
    wdgElementLayout.addWidget(self.lblSubType, 1, 0)
    
    self.cmbSubType=guiComboBox(self)
    wdgElementLayout.addWidget(self.cmbSubType, 1, 1)
    self.cmbSubType.fillComboBox(self.parentRecord, "elementtypecode", INSERT)
    
    self.lblSeparate = QLabel(self,'lblSeparate')
    self.lblSeparate.setText(
      'Nota Bene: all current morpheme data for this element will be deleted.')
    self.lblSeparate.setAlignment(QLabel.WordBreak | 
                                  QLabel.AlignVCenter | 
                                  QLabel.AlignLeft)
    wdgElementLayout.addWidget(self.lblSeparate,2,0)
    
    self.bnSeparate = QPushButton(self,'bnSeparate')
    self.bnSeparate.setText('Create morphemes')
    self.connect(self.bnSeparate, SIGNAL("clicked()")
                                , self.slotSplitElement)
    wdgElementLayout.addWidget(self.bnSeparate,2,1)
    
    self.lsvChildElements = QListView(self,'lsvChildElements')
    self.lsvChildElements.setFont(guiConf.widgetfont)
    self.lsvChildElements.setSorting(-1, FALSE)
    self.lsvChildElements.setRootIsDecorated(TRUE)
    self.lsvChildElements.setShowSortIndicator(FALSE)
    self.lsvChildElements.setTreeStepSize(40)
    self.lsvChildElements.addColumn("Element")
    self.lsvChildElements.setColumnWidthMode(0, QListView.Maximum)
    
    self.connect(self.lsvChildElements, SIGNAL("returnPressed(QListViewItem *)")
                                      , self.slotItemSelected)
    self.connect(self.lsvChildElements, SIGNAL("doubleClicked(QListViewItem *)")
                                     , self.slotItemSelected)
    
    wdgElementLayout.addMultiCellWidget(self.lsvChildElements,3,3,0,1)
    self.refresh()

  def refresh(self):
    self.item_to_record={}
    self.record_to_item={}
    self.lsvChildElements.clear()
    self.addChildren(self.lsvChildElements, self.parentRecord.elementnr)
  
  def addChildren(self, parent, elementnr):
    if elementnr == None:
      return
    previous=None
    for elmt in kuraapp.app.getObjects("lng_element"
                                       , parent_elementnr = elementnr):
      if previous==None:
        item=QListViewItem(parent)
      else:
        item=QListViewItem(parent, previous)
      item.setText(0, elmt.getFieldValue("text"))
      previous=item
      self.item_to_record[item]=elmt
      self.record_to_item[elmt]=item
      self.addChildren(item, elmt.elementnr)
          
  def slotSplitElement(self):
      
    if self.lsvChildElements.childCount() > 0:
      if QMessageBox.warning(self, "Kura"
         , "This element already has sub-elements. Do you want to delete them?"
         , "Yes", "No"
         ) == 1:
        return
    try:        
      self.parentRecord.deleteChildren("lng_element")
    except dbError, dberr:
      QMessageBox.information(self
            , "Error while deleting"
            , dberr.errorMessage)

    els=unicode(self.txtElement.text()).split(".")
            
    if len(els) > 1:
      seqnr=0
      for element in els:
        record=kuraapp.app.createObject("lng_element"
                                , streamnr=self.parentRecord.streamnr
                                , seqnr=seqnr
                                , parent_elementnr=self.parentRecord.elementnr
                                , text=element
                                , languagenr=self.parentRecord.languagenr
                                , elementtypecode=self.cmbSubType.currentKey()
                                , usernr=guiConf.usernr
                                )
        record.insert()
        seqnr+=1
    self.refresh() 
  
  def slotItemSelected(self, item):
    self.dlgOpen = dlgElement(kuraapp.app,
                              self,
                              'Edit Morpheme', "Morpheme", 
                              self.item_to_record[item],
                              UPDATE,
                              kuraapp.app.tables["lng_element"])
    self.connect(self.dlgOpen, PYSIGNAL("sigAcceptData")
                             , self.slotOpenAccept)
    self.dlgOpen.show()

  def slotOpenAccept(self):
    rec = self.dlgOpen.getMasterRecord()
    item = self.record_to_item[rec]
    item.setText(0, rec.text)

class tabElementLexeme(tabLexeme): 
  
  def __init__(self, parent, parentRecord):
    tabLexeme.__init__(self, parent)
    self.parentRecord=parentRecord
    if self.parentRecord.lexnr != None:
      self.lexeme=kuraapp.app.getObject( "lng_lex"
                                      , lexnr=self.parentRecord.lexnr
                                      )
      self.__setValues(self.lexeme)
    else:
      self.lexeme = None
      
    self.connect(self.bnZoom, SIGNAL("clicked()"), self.__zoom)
    self.connect(self.bnPick, SIGNAL("clicked()"), self.__pick)
    self.connect(self.bnAdd, SIGNAL("clicked()"), self.__add)

  def __setValues(self, lexeme):
    self.txtForm.setFont(guiConf.widgetfont)
    self.txtPhoneticForm.setFont(guiConf.widgetfont)
    self.txtGlosse.setFont(guiConf.widgetfont)
    self.txtDescription.setFont(guiConf.widgetfont)
    self.txtLanguage.setFont(guiConf.widgetfont)

    self.txtForm.setText(lexeme.getFieldValue("form"))
    self.txtPhoneticForm.setText(lexeme.getFieldValue("phonetic_form"))
    self.txtGlosse.setText(lexeme.getFieldValue("glosse"))
    self.txtDescription.setText(lexeme.getFieldValue("description"))
    self.txtLanguage.setText(lexeme.getFieldValue("language"))

  def __zoom(self):
    if self.lexeme:
      self.dlgZoom=dlgLexeme(kuraapp.app, self, 'Edit lexical item', "Lexeme", 
                             self.lexeme,  UPDATE, self.lexeme.tableDef)
      
      self.connect(self.dlgZoom, PYSIGNAL("sigAcceptData")
                   , self.slotZoomAccept)
      self.dlgZoom.show()
      
  def slotZoomAccept(self):
    self.lexeme=self.dlgZoom.getMasterRecord()
    self.parentRecord.lexnr=self.lexeme.lexnr
    self.__setValues(self.lexeme)
   
  def __pick(self):
    #
    # This is a modal dialog
    #
    dlgPick=dlgLexChooser(self, self.parentRecord)
    dlgPick.txtForm.setText(self.parentRecord.getFieldValue("text"))
    dlgPick.refreshSource()
    if dlgPick.exec_loop()==1:
      self.lexeme=dlgPick.masterRecord
      self.parentRecord.lexnr=self.lexeme.lexnr
      self.parentRecord.lexeme=self.lexeme.glosse
      self.__setValues(self.lexeme)


  def __add(self):
    if QMessageBox.warning(self, "Kura"
                           , "Do you want to add this element to the lexicon?"
                           , "Yes", "No", "Cancel"
                           , 2, 3
                           ) == 0:
      
      self.lexeme=kuraapp.app.createObject("lng_lex"
                                           , languagenr=self.parentRecord.languagenr
                                           , form=self.parentRecord.text
                                           , usernr=guiConf.usernr
                                           , phonetic_form=self.parentRecord.getPhoneticTranscription()
                                           , glosse=self.parentRecord.getGlosse()
                                           , description=self.parentRecord.getDescription()
                                           )

      if self.lexeme.glosse is None:
        self.lexeme.glosse="<empty>"
        
      self.lexeme.insert()
      self.parentRecord.lexnr=self.lexeme.lexnr
      self.__setValues(self.lexeme)

class dlgElement(guiTabDialog):

  def __init__(self, app, parent, title, firstTabTitle, 
            record, mode, tableDef, showChildren=FALSE):
            
    guiTabDialog.__init__( self
                         , app=app
                         , parent=parent
                         , title=title
                         , firstTabTitle="&Elements"
                         , record=record
                         , mode=mode
                         , tableDef=tableDef
                         , showChildren=FALSE
                         , addBottomSpring=TRUE)

    self.tagstab=TagsTab(self, app, record, "lng_element_tag")
    guiTabDialog.addChildTab( self
                            , "&Tags"
                            , self.tagstab
                            , record
                            , DETAIL)

    guiTabDialog.addChildTab(self
                            , "&Related Lexeme"
                            , tabElementLexeme(self, record)
                            , record
                            , DETAIL)
                            
    guiTabDialog.addChildTab( self
                            , "&Morphemes"
                            , tabElementSplit(self, record)
                            , record
                            , DETAIL)
  def accept(self):
    try:
      self.tagstab.formTags.save()
    except Exception, e:
      QMessageBox.critical(self, "Error saving tags",  unicode(e))
    guiTabDialog.accept(self)
    

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.10 $"""[11:-2]
