True = 1

import string

from qt import *
from dbobj import dbexceptions

import constants

from guiconfig import guiConf

class guiDetailList(QListView):

    def __init__(self, parent, app, parentRecord, childTable):
         QListView.__init__(self, parent)
         self.setFont(guiConf.widgetfont)
         self.setAllColumnsShowFocus(True)
         self.setFocusPolicy(self.StrongFocus)
         self.setShowSortIndicator(True)

         self.rows = {} 

         self.app = app

         self.parentRecord = parentRecord
         self.tableName = childTable
         self.tableDef = self.app.getTableDef(childTable)

         self.headers = []
         self.setHeaders(self.tableDef)
    
         self.connect(self, SIGNAL("returnPressed(QListViewItem *)"),
                      self.slotItemSelected)
         self.connect(self, SIGNAL("clicked(QListViewItem *)"),
                      self.slotItemSelected)
         self.connect(self, SIGNAL("doubleClicked(QListViewItem *)"),
                     self.slotItemSelected)
    
         self.refresh()
    
    def setHeaders(self, tableDef):
        w = getattr(guiConf, "%s_formlist_width" % tableDef.name)
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


    def closeEvent(self, ev):
        w = []
        for i in range(len(self.headers)):
            w.append("%s,%i" % (self.headers[i], self.columnWidth(i)))
        w = "|".join(w)
        setattr(guiConf, "%s_formlist_width" % self.tableDef.name, w)
        QListView.closeEvent(self, ev)



    def refresh(self):
        self.setCursor(Qt.waitCursor)
        QListView.clear(self)
        self.rows = {}
        rows = self.parentRecord.getChildren(self.tableName)
        for row in rows:
            self.slotAddItem(row)
        self.setCursor(Qt.arrowCursor)

    
    def slotAddItem(self, rec):
        """
        Add a record to the listview and the cache.
        """
        lvi = QListViewItem(self)
        col = 0
        for fieldname in self.headers:
            try:
                lvi.setText(col, rec.getFieldValue(fieldname))
            except:
                lvi.setText(col, str(rec.getFieldValue(fieldname)))
            col += 1   
        self.rows[lvi] = rec

    def slotItemSelected(self, lvi):
        if lvi != None:
            record = self.rows[lvi]
            self.emit(PYSIGNAL("sigRecordSelected"),(record,lvi))

    def slotDeleteItem(self):
        if QMessageBox.warning(self,
                               "Kura",
                               "Do you want to delete this record?",
                               "Yes",
                               "No", QString(), 1, 1) == 0:
            rec = self.rows[self.currentItem()]
            try:
                rec.delete()
                del self.rows[self.currentItem()]
                self.takeItem(self.currentItem())
            except dbexceptions.dbError, dberr:
                QMessageBox.information(self, "Kura Error while deleting",
                                        dberr.errorMessage)

            self.emit(PYSIGNAL("sigItemDeleted"),())      

    def slotNewItem(self):
        self.emit(PYSIGNAL("sigCreateNewItem"),(self.parentRecord,))

    def slotUpdateItem(self, rec, lvi):
        col = 0
        for fieldname in self.headers:
            try:
                lvi.setText(col, rec.getFieldValue(fieldname))
            except:
                lvi.setText(col, str(rec.getFieldValue(fieldname)))
            col += 1   
        self.rows[lvi] = rec
    
  
    def keyPressEvent(self, e):
        if e.key()==Qt.Key_Enter or e.key()==Qt.Key_Return:
            self.slotItemSelected(self.currentItem())
        elif e.key()==Qt.Key_Delete:
            self.slotDeleteItem()
        elif e.key()==Qt.Key_Insert:
            self.slotNewItem()
        else:
            QListView.keyPressEvent(self, e)


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.9 $
    Last edited          : $Date: 2002/11/12 22:12:46 $
 ***************************************************************************/
"""
