False = 0
True = 1

from kuralib import kuraapp
from qt import QComboBox
from kuragui.guiconfig import guiConf
from kuralib import kuraapp

DOMAIN = 0
VALUE = 1
REFERENCE = 2
NOTE = 3


class kuraCmbTagValues(QComboBox):
    """
    
    kuraCmbTagValues is a combobox that shows all values that have
    been entered for a certain tag in the tag_domain table. Users
    can add new values here, but they will _not_ be autmatically
    added to tag_domain - unless they want to (configuration option!)
    
    Note: make this a what's this text.
    
    @param parent - the QWidget parent of this QWidget
    @param tag    - the tag where the list is based on
    @param        - tagTableName - lng_lex_tag, lng_element_tag etc.
    """
    
    def __init__(self, parent, tagTableName, tag = None, *args):
        QComboBox.__init__(self, parent, *args)
        self.setAutoCompletion(True)
        self.setFont(guiConf.widgetfont)
        self.index_to_key = {}
        self.key_to_index = {}
        self.strlist = []
        self.mode = None
        self.tagTableName = tagTableName
        if tag != None:
            self.slotRefresh(tag)
               

    def clear(self):
        QComboBox.clear(self)
        self.index_to_key = {}
        self.key_to_index = {}
        self.strlist = []
        
    def slotRefresh(self, tag):
        self.clear()

        if tag == None:
            QComboBox.setEnabled(self, False)
        else:
            tagType = kuraapp.app.getObject("lng_tag", tag = tag).getTagTypeCode()

            if int(tagType.isdomain) == True:
                self.mode = DOMAIN
                QComboBox.setEnabled(self, True)
                QComboBox.setEditable(self, False)
                
                rows = kuraapp.app.getObjects("lng_tagdomain", tag = tag)
                for row in rows:
                    self.insertItem(row.description) 
                    index = self.count()-1
                    self.index_to_key[index] = row.domainnr
                    self.key_to_index[row.domainnr]=index

            elif int(tagType.isvalue) == True:
                self.mode = VALUE
                QComboBox.setEnabled(self, True)
                QComboBox.setEditable(self, True)

                self.insertItem("<New Value>")

                if guiConf.ShowValueHint == True:
                    rows = kuraapp.app.getObjects(self.tagTableName,
                                                      tag = tag)
                    self.strlist=["<New Value>"]
                    for row in rows:
                        if row.value not in self.strlist:
                            self.strlist.append(row.value)
                            self.insertItem(row.value)


            elif int(tagType.isreference)==True:
                self.mode = REFERENCE
                QComboBox.setEnabled(self, True)
                QComboBox.setEditable(self, False)

                rows = kuraapp.app.getObjects("lng_reference")
                for row in rows:
                    self.insertItem(row.title + ", " + row.year +
                                        ", " + row.author) 
                    index = self.count() - 1
                    self.index_to_key[index] = row.referencenr
                    self.key_to_index[row.referencenr] = index

            else:
                QComboBox.setEnabled(self, False)
                QComboBox.setEditable(self, False)

    def slotSetCurrentItem(self, value):
        if self.mode == DOMAIN:
            if self.key_to_index.has_key(value)==False:
                return
            else:
                self.setCurrentItem(self.key_to_index[value])

        elif self.mode == VALUE:
            if guiConf.ShowValueHint==True:
                if value in self.strlist:
                    self.setCurrentItem(self.strlist.index(value))
                    self.changeItem(value, self.currentItem())
                else:
                    if self.currentText() == "<New Value>":
                        self.changeItem(value, 0)
                    else:
                        self.insertItem(value, 0)
            else:
                self.changeItem(value, 0)

        elif self.mode == REFERENCE:
            if hasattr(self.key_to_index, value) == False:
                return
            else:
                self.setCurrentItem(self.key_to_index[value])

    def currentKey(self):
        if self.mode == DOMAIN:
            return self.index_to_key[self.currentItem()]
        elif self.mode == VALUE:
            return unicode(self.currentText())
        elif self.mode == REFERENCE:
            return self.index_to_key[self.currentItem()]
        else:
            return None

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.7 $"""[11:-2]

__cvslog__="""
    $Log: kuracmbtagvalues.py,v $
    Revision 1.7  2002/11/12 22:12:44  boud
    Bugfixes -- hope nothing else broke.

    Revision 1.6  2002/11/02 15:51:34  boud
    Removed styles, parse sets, unified tag form, made texts better editable.

    Revision 1.5  2002/07/02 20:55:13  boud
    porting...

    Revision 1.4  2002/06/17 14:06:11  boud
    Interlinear texts are back + pychecker checks

    Revision 1.3  2002/06/14 13:44:08  boud
    We march on and on and on.

    Revision 1.2  2002/05/24 14:01:27  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
