False = 0
True = 1

import string, time
from types import NoneType, StringType, IntType

from qt import *

from dbobj import dbexceptions

from guitabdialog import guiTabDialog
from guiconfig import guiConf
import constants

checkmark = [
"10 12 3 1",
" 	c None",
".	c #000000",
"+	c #A2A2A2",
"       ...",
"      .++.",
"      .+. ",
"     .++. ",
".    .+.  ",
"..  .++.  ",
".+. .+.   ",
".++.++.   ",
" .+++.    ",
"  .++.    ",
"   ..     ",
"    .     "
]

class guiListView(QListView):
    """
    Updated & improved listview component
    
    Show a set of records in a listview.
    
    Supports:
            function   standard binding           Calls
    insert: New()      Insert                     Master-Detail form
    update: Open()     Enter/Return/doubleclick   Master-Detail form
    delete: Delete()   Delete                     messagebox for confirmation
    query : Find()     F2                         Master-only form
             
    """

    def __init__(self, app, tableName,
                 searchRec, dlgForm, dlgSearch,
                 parent, showChildren=False, *args):
        QListView.__init__(self, parent, *args)
        self.checkmark = QPixmap(checkmark)
        self.nocheck=QPixmap([""])
        self.setFont(QFont(guiConf.textfontfamily, guiConf.textfontsize))
        self.setAllColumnsShowFocus(True)
        self.setFocusPolicy(self.StrongFocus)
        self.setShowSortIndicator(True)
        self.showChildren = showChildren
        self.rows = {}
        self.app = app
        self.tableName = tableName
        self.masterLabel = self.app.getTableLable(tableName)
        self.tableDef = self.app.getTableDef(tableName)
        self.searchRec = searchRec
    
        if dlgForm == None:
            self.dlgFormClass = guiTabDialog
        else:
            self.dlgFormClass = dlgForm
        if dlgSearch == None:
            self.dlgSearchClass = guiTabDialog
        else:
            self.dlgSearchClass = dlgSearch
    
        self.headers = []
        self.setHeaders(self.tableDef)
        self.show()
        if self.searchRec <> None:
            self.refresh(self.searchRec)
            self.__currentQuery = self.searchRec

    def closeEvent(self, ev):
        w = []
        for i in range(len(self.headers)):
            w.append("%s,%i" % (self.headers[i], self.columnWidth(i)))
        w = "|".join(w)
        setattr(guiConf, "%s_width" % self.tableDef.name, w)
        QListView.closeEvent(self, ev)


    def dragObject(self):
        record = self.rows[self.currentItem()]
        return QTextDrag(str(record.getLink()), self)
  
    def setHeaders(self, tableDef):
        w = getattr(guiConf, "%s_width" % tableDef.name)
        if w == "":
            for fieldname, fieldDef in tableDef.orderedFieldList():
                if fieldDef.inList:
                    self.headers.append(fieldname)
                    self.addColumn(fieldDef.label, 200)
        else:
            for c in w.split("|"):
                name, width = c.split(",")
                self.headers.append(name)
                self.addColumn(name, int(width))

    def addItem(self, rec):
        """
        Add a record to the listview and the cache.
        """
        lvi = QListViewItem(self)
        lvi.setDragEnabled(True)
        col = 0
        for fieldname in self.headers:
            value = rec.getFieldValue(fieldname)
            if rec.getFieldDefinition(fieldname).datatype == constants.BOOLEAN:
                if rec.getFieldValue(fieldname):
                    lvi.setPixmap(col, self.checkmark)
            else:
                if value == None:
                    value = QString()
                if type(value)==IntType:
                    value=unicode(value)
                lvi.setText(col, QString(value))
            col=col+1
        self.rows[lvi]=rec
        return lvi

    def refresh(self, searchRec):
        """
        Reload the listview
        """
        self.setCursor(Qt.waitCursor)
        QListView.clear(self)
        self.rows = {}
        rows = self.app.getObjects(self.tableName,
                                   fields = searchRec.getFields())
        t = time.time()
        for row in rows:
            self.addItem(row)
        self.setCurrentItem(self.firstChild())
        self.setCursor(Qt.arrowCursor)
##         print "Refreshing listview for %s: %i" % (self.tableName, time.time() -t )
        
    def __createQueryObject(self):
        if guiConf.useDefaultForSearch:
            record=self.app.createDefaultObject(self.tableName)
        else:
            record = self.app.createObject(self.tableName, fields={})
        return record
    
    def find(self):
        record = self.__createQueryObject()
        self.dlgSearch = self.dlgSearchClass(self.app, self,
                                             "Find " + self.masterLabel,
                                             self.masterLabel,
                                             record, constants.SEARCH,
                                             self.tableDef,
                                             showChildren = False)

        self.connect(self.dlgSearch, PYSIGNAL("sigAcceptData"),
                     self.slotFindAccept)
        self.dlgSearch.show()
    
    def slotFindAccept(self):
        self.__currentQuery = self.dlgSearch.getMasterRecord()
        self.refresh(self.__currentQuery)

    def getCurrentQuery(self):
        return getattr(self,"__currentQuery", self.__createQueryObject())
    
    def new(self):
        defaultRec = self.app.createObject(self.tableName, self.__currentQuery.getFields())
        self.dlgNew = self.dlgFormClass(app = self.app,
                                        parent = self,
                                        title = "New " + self.masterLabel,
                                        firstTabTitle = self.masterLabel,
                                        record = defaultRec,
                                        mode = constants.INSERT,
                                        tableDef = self.tableDef,
                                        showChildren = False)

        self.connect(self.dlgNew, PYSIGNAL("sigAcceptNewData"),
                     self.slotNewAccept)
        self.dlgNew.show()

    def slotNewAccept(self, record):
        lvi = self.addItem(record)
        self.ensureItemVisible(lvi)
         
    def open(self):
        try:
            record = self.rows[self.currentItem()]
        except KeyError: 
            # Probably an empty list
            return 
    
        self.dlgOpen = self.dlgFormClass(self.app, self,
                                         'Edit ' + self.masterLabel,
                                         self.masterLabel, record,
                                         constants.UPDATE, self.tableDef,
                                         self.showChildren)
                   
        self.connect(self.dlgOpen, PYSIGNAL("sigAcceptUpdatedData"),
                     self.slotOpenAccept)
    
        self.dlgOpen.show()
    
    def slotOpenAccept(self, record):
        self.rows[self.currentItem()] = record
        col=0
        for (fieldname, field) in self.tableDef.orderedFieldList():
            if field.inList:
                if field.datatype == constants.BOOLEAN:
                    if record.getFieldValue(fieldname):
                        self.currentItem().setPixmap(col, self.checkmark)
                    else:
                        self.currentItem().setPixmap(col, self.nocheck)
                else:
                    self.currentItem().setText(col,
                                               record.getFieldValue(fieldname))
                col=col+1

    def delete(self):
      if QMessageBox.warning(self, "Kura",
                             "Do you want to delete this record?",
                             "Yes", "No", QString(),
                             1, 1) == 0:
          rec = self.rows[self.currentItem()]
          try:
              rec.delete(False)
              del self.rows[self.currentItem()]
              self.takeItem(self.currentItem())
          except dbexceptions.dbError, dberr:
              if QMessageBox.critical(self, "Kura",
                                      "Removing this item would also remove items from other tables. Do you want to continue?", "Yes", "No", QString(),
                                      1, 1) == 0:
                  try:
                      rec.delete(True)
                      del self.rows[self.currentItem()]
                      self.takeItem(self.currentItem())
                  except dbexceptions.dbError, dberr:
                      QMessageBox.information(self,
                                              "Kura Error while deleting",
                                              dberr.errorMessage)


    def contentsMouseDoubleClickEvent(self, e):
      self.open()

    def keyPressEvent(self, e):
      if e.key()==Qt.Key_Enter or e.key()==Qt.Key_Return:
          self.open()
      elif e.key()==Qt.Key_F2:
          self.find()
      elif e.key()==Qt.Key_Delete:
          self.delete()
      elif e.key()==Qt.Key_Insert:
          self.new()
      else:
          QListView.keyPressEvent(self, e)


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.19 $"""[11:-2]

