from qt import *
from kuragui.guiconfig import guiConf
from kuralib import kuraapp
from dbobj.dbexceptions  import dbError

True = 1
False = 0

class kuraTextSelector(QListView):
  def __init__(self, searchRec, *args):
    apply(QListView.__init__,(self,) + args)
    self.setFont(guiConf.widgetfont)
    self.refresh(searchRec)
    self.connect(self, SIGNAL("returnPressed(QListViewItem *)")
                     , self.slotItemSelected)
    self.connect(self, SIGNAL("clicked(QListViewItem *)")
                     , self.slotItemSelected)
    self.connect(self, SIGNAL("doubleClicked(QListViewItem *)")
                     , self.slotItemSelected)
    

    self.clear()
    self.rows={}
    self.parents={}
      
    self.setRootIsDecorated(True)
    self.setShowSortIndicator(False)
    self.setSorting(-1)
    self.setTreeStepSize(40)
    self.addColumn("Language")
    self.setColumnWidthMode(0, QListView.Maximum)
    self.refresh(searchRec)
    self.setFocus()
    self.setCurrentItem(self.firstChild())

  def resizeEvent(self, ev):
    guiConf.textselectorwidth = ev.size().width()
    QListView.resizeEvent(self, ev)

  def dragObject(self):
    record, lvi = self.currentRecord()
    return QTextDrag(str(record.getLink()), self)

  def refresh(self, searchRec):
    self.setCursor(Qt.waitCursor)
    self.clear()
    self.rows={}
    self.parents={}
    for language in kuraapp.app.getObjects("lng_language"):
      parent=QListViewItem(self, language.getFieldValue("language"))
      self.parents[parent]=language
      for text in kuraapp.app.getObjects("lng_text",
                                         languagenr=language.languagenr):
        item=QListViewItem(parent, text.getFieldValue("title"))
        item.setDragEnabled(True)
        self.rows[item]=text

    self.setCursor(Qt.arrowCursor)
     
  def slotItemSelected(self, item):
    if item == None:
      return
    if self.rows.has_key(item):
      self.emit(PYSIGNAL("sigRecordSelected"), (self.rows[item], item))
         
  def slotAddItem(self, rec):
    parent = self.currentItem().parent()
    if parent == None:
      parent = self.currentItem()

    lvi = QListViewItem(parent, rec.getFieldValue("title"))
    self.rows[lvi]=rec
    self.ensureItemVisible(lvi)

  def slotDeleteItem(self):
    if QMessageBox.warning(self
                  , "Kura"
                  , "Are you sure you want to irretrievably delete this text?"
                  , "Yes"
                  , "No"
                  ,QString()
                  , 1
                  , 1
                  )==0:
      rec = self.rows[self.currentItem()]
      try:
        rec.delete(True)
        del self.rows[self.currentItem()]
        item=self.currentItem()
        parent=item.parent()
        if parent==None:
          parent=self
        parent.takeItem(item)
      except dbError, dberr:
        QMessageBox.information(self, "Kura Error while deleting", dberr.errorMessage)

      self.emit(PYSIGNAL("sigItemDeleted"),())      

  def slotNewItem(self):

    if self.currentItem() in self.parents.keys():
      parent=self.parents[self.currentItem()]
    else:
      parent=self.parents[self.currentItem().parent()]

    rec=kuraapp.app.createDefaultObject("lng_text",
                                          languagenr=parent.languagenr)
    
    self.emit(PYSIGNAL("sigCreateNewItem"),(rec,))  
    

  def slotUpdateItem(self, rec, lvi):
    if self.rows.has_key(lvi):
      self.rows[lvi]=rec
      lvi.setText(0, rec.title)
  
  def keyPressEvent(self, e):
    if e.key()==Qt.Key_Enter or e.key()==Qt.Key_Return:
      self.slotItemSelected(self.currentItem())
    elif e.key()==Qt.Key_F2:
      self.emit(PYSIGNAL("sigFindRecord"),())
    elif e.key()==Qt.Key_Delete:
      self.slotDeleteItem()
    elif e.key()==Qt.Key_Insert:
      self.slotNewItem()
    else:
      QListView.keyPressEvent(self, e)

  def currentRecord(self):
    if self.rows.has_key(self.currentItem()):
      return (self.rows[self.currentItem()], self.currentItem())
    elif self.parents.has_key(self.currentItem()):
       if self.currentItem().childCount() > 0:
         return (self.rows[self.currentItem().firstChild()], self.currentItem())
      


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.11 $"""[11:-2]
