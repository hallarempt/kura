False = 0
True = 1

from qt import *

from kuralib import kuraapp


from kuralib.lng_strm import lng_stream
from kuralib.lng_sttg import lng_stream_tag
from kuralib.lng_elmt import lng_element
from kuralib.lng_eltg import lng_element_tag
from kuralib.lng_text import lng_text
from kuralib.lng_txtg import lng_text_tag

from kuragui.guiconfig import guiConf
from kuragui.guitabdialog import guiTabDialog
from kuragui.guiform import guiForm
from kuragui.constants import *

from kuratextcanvas import KuraTextCanvas
from kuratextselector import kuraTextSelector

from dlgtext import dlgText
from dlgstream import dlgStream
from dlgelement import dlgElement
from dlgtag import dlgTag
from dlgnewtext import dlgNewText

class KuraTextListView(QSplitter):

    def __init__(self, parent, searchRec):
        QSplitter.__init__(self, parent)

        self.textSelector=kuraTextSelector(searchRec,
                                           self)
       
        self.setResizeMode(self.textSelector,
                           QSplitter.KeepSize)

        # listbox connections
        self.connect(self.textSelector,
                     PYSIGNAL("sigRecordSelected"), 
                     self.slotSelectText)
        
        self.connect(self.textSelector,
                     PYSIGNAL("sigFindRecord"), 
                     self.find)

        self.connect(self.textSelector,
                     PYSIGNAL("sigCreateNewItem"), 
                     self.slotNewText)
        
        self.connect(self.textSelector,
                     PYSIGNAL("sigItemDeleted"), 
                     self.slotDeleteText)

        self.initView()
        self.setSizes([guiConf.textselectorwidth])

    def initView(self):
        self.textSelector.setFocus()
        self.textView = KuraTextCanvas(self)
        
        self.connect(self.textView,
                     PYSIGNAL("sigItemOpened"),
                     self.slotItemOpened)

    def getCurrentQuery(self):
        record, lvi = self.textSelector.currentRecord()
        return record
                
    def slotSelectText(self, text, lvi):
        QApplication.setOverrideCursor(Qt.waitCursor)
        self.textView.setTextByNumber(text.getFieldValue("textnr"))
        self.textView.setFocus()
        QApplication.restoreOverrideCursor()
                                                                    
    def __openText(self, item, record):
        self.dlgOpen=dlgText(app=kuraapp.app,
                             parent=self,
                             title='Edit Text',
                             firstTabTitle="Text", record=record,
                             mode= UPDATE,
                             tableDef=kuraapp.app.tables["lng_text"])
        self.connect(self.dlgOpen,
                     PYSIGNAL("sigAcceptData"),
                     self.slotOpenTextAccept)
        self.dlgOpen.show()
        
    def slotOpenTextAccept(self):
        rec = self.dlgOpen.getMasterRecord()
        self.textView.setItemText(rec.title)
        self.textView.update()
 
    def __openStream(self, item, record):
        self.dlgOpen=dlgStream(kuraapp.app, self, 'Edit Stream', "Stream", 
                             record,UPDATE, kuraapp.app.tables["lng_stream"])
        self.connect(self.dlgOpen,
                     PYSIGNAL("sigAcceptData"),
                     self.slotOpenStreamAccept)
        self.dlgOpen.show()
        
    def slotOpenStreamAccept(self):
        rec=self.dlgOpen.getMasterRecord()
        self.textView.update()
        
    def __openElement(self, item, record):
        self.dlgOpen=dlgElement(kuraapp.app, self, 'Edit Element', "Element", 
                                record, UPDATE,
                                kuraapp.app.tables["lng_element"])
        self.connect(self.dlgOpen,
                     PYSIGNAL("sigAcceptData"),
                     self.slotOpenElementAccept)
        self.dlgOpen.show()

        
    def slotOpenElementAccept(self):
        rec = self.dlgOpen.getMasterRecord()
        self.textView.setItemText(rec.text)

    def __openTag(self, item, record, title):
        self.dlgOpen=dlgTag( parent=self
                             , title=title
                             , parentTableName=record.table
                             , record=record
                             )
        self.connect(self.dlgOpen,
                     PYSIGNAL("sigAcceptData"),
                     self.openTagAccept)
        self.dlgOpen.show()
        
    def openTagAccept(self):
        rec=self.dlgOpen.getMasterRecord()
        self.textView.setItemText(rec.getDescription())
        self.textView.update()
        
    def slotItemOpened(self, item):
        record = item.getRecord()
        if isinstance(record, lng_stream):        
             self.__openStream(item, record)
        elif isinstance(record, lng_text):
             self.__openText(item, record)
        elif isinstance(record, lng_element):
             self.__openElement(item, record)
        elif isinstance(record, lng_element_tag):
            self.__openTag(item, record, "Edit word tag " + record.tag)
        elif isinstance(record, lng_stream_tag):
            self.__openTag(item, record, "Edit sentence tag " + record.tag)
        elif isinstance(record, lng_text_tag):
            self.__openTag(item, record, "Edit text tag " + record.tag)

    def refresh(self, searchRec):
        self.setCursor(Qt.waitCursor)
        self.textSelector.refresh(searchRec)
        self.textView.clear()
        self.setCursor(Qt.arrowCursor)    
                
    def find(self):
        if guiConf.useDefaultForSearch == True:
            record=kuraapp.app.createDefaultObject("lng_text")
        else:
            record=kuraapp.app.createObject("lng_text", fields={})

        self.dlgSearch=guiTabDialog(kuraapp.app, self, "Find", "Text",
                                    record, SEARCH,
                                    kuraapp.app.tables["lng_text"],
                                    showChildren=False)
            
        self.connect(self.dlgSearch,
                     PYSIGNAL("sigAcceptData"),
                     self.slotFindAccept)
        self.dlgSearch.show()

    def slotFindAccept(self):
        self.refresh(self.dlgSearch.getMasterRecord() )
     
    def new(self):
        self.textView.clear()
        self.textSelector.slotNewItem()
    
    def slotNewText(self, defaultRec):
        self.dlgNew=dlgNewText(self)
        self.connect(self.dlgNew,
                     PYSIGNAL("sigAcceptData"),
                     self.slotNewTextAccept)
        self.dlgNew.show()
        
    def slotNewTextAccept(self):
        record=kuraapp.app.getObject("lng_text",
                                    textnr=self.dlgNew.recText.textnr)
        self.textSelector.slotAddItem(record)
    
    def open(self):
        try:        
            record, lvi=self.textSelector.currentRecord()
        except TypeError:
            # nothing selected
            return
            
        
        self.dlgOpen=dlgText(kuraapp.app, self, 'Edit Text', "Text", 
                             record, UPDATE, kuraapp.app.tables["lng_text"])
        self.connect(self.dlgOpen,
                     PYSIGNAL("sigAcceptData"),
                     self.slotOpenAccept)
        self.dlgOpen.show()
        
    def slotOpenAccept(self):
        rec, lvi=self.textSelector.currentRecord()
        rec = self.dlgOpen.getMasterRecord()
        self.textSelector.slotUpdateItem(rec, lvi)
        
    def delete(self):
        self.textSelector.slotDeleteItem()
        
    def slotDeleteText(self):
        try:
            self.textview.clear()
        except:
            pass

    def keyPressEvent(self, e):
        if e.key()==Qt.Key_F2:
            if guiConf.textSortCriterion=="filter":
                self.find()


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.21 $"""[11:-2]
