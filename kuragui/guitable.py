#!/usr/bin/env python

"""guitable.py -- an editable view of a database table."""
import sys
sys.setappdefaultencoding("utf-8")
True = 1
False = 0

from guiconfig import guiConf
from guicombotableitem import GuiComboTableItem
from kuralib import kuraapp
from dbobj import dbtypes
from qttable import QTable, QCheckTableItem, QTableItem
from qt import QApplication, SIGNAL, SLOT, Qt, QFont


class GuiTable(QTable):


    def __init__(self, parent, searchForm, editForm, *args):
        QTable.__init__(self, parent, *args)
        self.setSelectionMode(QTable.SingleRow)
        self.setShowGrid(True)
        self.app = kuraapp.app
        self.searchForm = searchForm
        self.editForm = editForm
        self.headers = []
        self.connect(self, SIGNAL("valueChanged(int, int)"), self.commit)
        self.setSorting(True)


    def sortColumn(self, col, ascending, wholeRows):
        QTable.sortColumn(self, col, ascending, True)


    def commit(self, row, col):
        item = self.item(row, col)
        rec = item.record
        if item.__class__ == QTableItem:
            rec.setFieldValue(item.fieldName, item.text())
        elif item.__class__ == GuiComboTableItem:
            rec.setFieldValue(item.fieldName, item.currentKey())
        elif item.__class__ == QCheckTableItem:
            if item.isChecked:
                rec.setFieldValue(item.fieldName, True)
            else:
                rec.setFieldValue(item.fieldName, False)
        rec.update()

        
    def keyPressEvent(self, ev):
        if ev.key() == Qt.Key_Enter or ev.key() == Qt.Key_Return:
            self.editCell(self.currentRow(), self.currentColumn())
        else:
            QTable.keyPressEvent(self, ev)

        
    def clear(self):
        self.setNumRows(0)
        self.setNumCols(0)


    def setHeaders(self, tableDef):
        w = getattr(guiConf, "%s_table_width" % tableDef.name, "")
        if w == "":
            for fieldname, fieldDef in tableDef.orderedFieldList():
                if fieldDef.dialog:
                    self.headers.append(fieldname)
                    self.insertColumns(self.numCols(), 1)
                    self.horizontalHeader().setLabel(self.numCols() - 1,
                                                     fieldDef.label)
                    if fieldDef.readonly:
                        self.setColumnReadOnly(self.numCols() -1, True)

        else:
            for c in w.split("|"):
                name, width = c.split(",")
                self.headers.append(name)
                self.addColumn(name, int(width))


    def refresh(self, searchRec):
        self.tableDef = searchRec.tableDef
        self.setCursor(Qt.waitCursor)
        self.clear()
        self.setHeaders(searchRec.tableDef)
        records = self.app.getObjectsByRec(searchRec)
        self.insertRows(0, len(records))
        r = -1
        for rec in records:
            r += 1
            c = -1
            for fieldname, fieldDef in searchRec.tableDef.orderedFieldList():
                if fieldDef.dialog:
                    value = rec.getFieldValue(fieldname)
                    c += 1
                    # picklist
                    if fieldDef.relation != None:
                        if fieldDef.readonly:
                            descriptor = rec.getDescriptorColumnName(fieldname)
                            self.setText(r, c, rec.getFieldValueAsString(descriptor))
                        else:
                            i = GuiComboTableItem(self)
                            self.setItem(r, c, i)
                            i.fillComboBox(fieldDef, value, rec)
                    # boolean
                    elif fieldDef.datatype == dbtypes.BOOLEAN:
                        self.setItem(r, c, QCheckTableItem(self, ""))
                        self.item(r, c).setChecked(value)
                    else:
                        # plain text
                        self.setItem(r, c, QTableItem(self,
                                                      QTableItem.WhenCurrent,
                                                      unicode(value)))
                    self.item(r,c).fieldName = fieldDef.name
                    self.item(r,c).record = rec
        self.setCursor(Qt.arrowCursor)


    def closeEvent(self, ev):
        w = []
        for i in range(len(self.headers)):
            w.append("%s,%i" % (self.headers[i], self.columnWidth(i)))
        setattr(guiConf, "%s_table_width" % self.tableDef.name, "|".join(w))
        QTable.closeEvent(self, ev)

    def new(self):
        pass


    def delete(self):
        pass


    def open(self, row=0, col=0, button=0, point=None):
        print args


    def find(self):
        pass


def main(args):
    qapp=QApplication(args)
    kuraapp.initApp(str(guiConf.username),
                    str(guiConf.database),
                    str(guiConf.password),
                    str(guiConf.hostname))
    
    kuraapp.initCurrentEnvironment(1,
                                   1,
                                   1)
    app = kuraapp.app
        
    mainwin=GuiTable(None, None, None)
    mainwin.show()
    mainwin.refresh(app.createObject('lng_lex', fields={}))
    qapp.connect(qapp, SIGNAL('lastWindowClosed()'), qapp, SLOT('quit()'))
    qapp.setFont(QFont(guiConf.textfontfamily, guiConf.textfontsize), True)
    qapp.exec_loop()
    


if __name__ == "__main__":
    
    main(sys.argv)


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.17 $"""[11:-2]
