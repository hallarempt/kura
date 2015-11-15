False = 0

from qttable import QComboTableItem
from qt import QStringList

class GuiComboTableItem(QComboTableItem):
    """
    A light-weight combobox for use in QTable objects that keeps
    a mapping between the string shown in the box and the actual
    data (for instance, database keys) that are used to identify
    the options.
    """
    __listCache = {}

    def __init__(self, parent):
        QComboTableItem.__init__(self, parent, QStringList(), False)
        self.index_to_key = {}
        self.key_to_index = {}
                

    def fillComboBox(self, fieldDef, fieldValue, record):
        """
        Fills the combobox with a picklist. If there has been a
        combobox for the relevant field, a cached set of items is
        taken.

        Every combobox stores a fairly large number pointers to stings
        in a QStringList object, but there's nothing to be done about that.

        @param fieldDef: dbFieldDef object that contains the meta-information
           about this field.
        @param fieldValue: the current value of the field. Used to set
           the current item in the picklist.
        @param record: the current dbRecord object. Used to retrieve the
           picklist.
        
        """
        if self.__listCache.has_key(fieldDef):
            self.items = self.__listCache[fieldDef]
        else:
            self.items = QStringList()
            if fieldDef.nullable:
                self.__insertItem("<None>", None)

            fieldName = fieldDef.name
            descriptor = record.getForeignDescriptorColumnName(fieldName)
                
            fk = record.getForeignKeyColumnName(fieldName)
        
            for row in record.picklist(fieldName):
                self.__insertItem(row.getFieldValue(descriptor),
                                  row.getFieldValue(fk))
            self.__listCache[fieldDef] = self.items

        self.setStringList(self.items)
        self.setCurrentItem(fieldValue)


    def currentKey(self):
        try:
            return self.index_to_key[self.currentItem()]
        except KeyError:
            return None


    def __insertItem(self, text, index):
        self.items.append(text)
        self.index_to_key [self.count() - 1] = index
        self.key_to_index [index] = self.count() - 1
        
__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.4 $"""[11:-2]

__cvslog__="""
    Last edited          : $Date: 2002/06/17 14:06:13 $

    CVS Log:
    $Log: guicombotableitem.py,v $
    Revision 1.4  2002/06/17 14:06:13  boud
    Interlinear texts are back + pychecker checks

    Revision 1.3  2002/05/20 19:34:44  boud
    The guitable now can handle database updates.

    Revision 1.2  2002/05/19 19:49:13  boud
    Split guitable and combobox.

    Revision 1.1  2002/05/19 14:16:28  boud
    ComboTableItem now works perfectly.ZZ

"""
