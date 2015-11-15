False = 0
True = 1
import constants
from qt import QComboBox, SIGNAL, PYSIGNAL, QSizePolicy

class guiComboBox(QComboBox):

    def __init__(self, parent, *args):
        QComboBox.__init__(self, False, parent, *args)
        self.setAutoCompletion(True)
        self.index_to_key = {}
        self.key_to_index = {}
        self.connect(self, SIGNAL("activated(int)"), self.slotItemSelected)
        self.setSizePolicy(QSizePolicy(7, 0,
                                       self.sizePolicy().hasHeightForWidth()))
    
    def currentText(self):
        return unicode(QComboBox.currentText(self) )
    
    def insertItem(self, text, index):
        QComboBox.insertItem(self, text)
        self.index_to_key [self.count() - 1] = index
        self.key_to_index [index]=self.count() - 1
    
    def currentKey(self):
        try:
            return self.index_to_key[self.currentItem()]
        except KeyError:
            return None

    def setCurrentItem(self, key):
        if self.key_to_index.has_key(key):
            QComboBox.setCurrentItem(self, self.key_to_index[key])
  
    def slotItemSelected(self, index):
        rec = self.index_to_key[index]
        self.emit(PYSIGNAL("recSelected"),(rec, index))

    def clear(self):
        QComboBox.clear(self)
        self.index_to_key = {}
        self.key_to_index = {}


    def initComboBox(self, app, tableName, mode, nullAllowed, currentKey=None):
        self.clear()
        if mode == constants.SEARCH or nullAllowed:
            self.insertItem("<None>", None)
    
        for row in app.getObjects(tableName):
            self.insertItem(row.getDescription(), row.getPrimaryKey())

        if currentKey!=None:
            self.setCurrentItem(currentKey)

    def fillComboBox(self, record, field, mode):
        self.clear()
        if record == None:
            return
        if mode == constants.SEARCH \
               or record.getFieldDefinition(field).nullable:
            self.insertItem("<None>", None)
        descriptor=record.getForeignDescriptorColumnName(field)
        fk=record.getForeignKeyColumnName(field)
        for row in record.picklist(field):
            self.insertItem(text = row.getFieldValue(descriptor),
                            index = row.getFieldValue(fk))
        self.setCurrentItem(record.getFieldValue(field))

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.5 $
    Last edited          : $Date: 2002/06/17 14:06:13 $
    
    CVS Log:         
    $Log: guicombobox.py,v $
    Revision 1.5  2002/06/17 14:06:13  boud
    Interlinear texts are back + pychecker checks

    Revision 1.4  2002/06/14 13:45:14  boud
    We march on and on and on.

    Revision 1.3  2002/05/24 14:01:29  boud
    Converted most files to new coding standards + new config standard.

    Revision 1.2  2002/05/12 18:38:29  boud
    guitable starts to wrok.

    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.11  2001/02/01 19:29:52  boud
    Made more robust.

    Revision 1.10  2001/01/25 23:04:22  boud
    Made non-modal

    Revision 1.9  2001/01/08 20:55:06  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
