False = 0
True = 1

from kuragui.guicombobox import guiComboBox

from kuralib import kuraapp

class kuraCmbTags(guiComboBox):

    def __init__(self, parent, parentTableName, *args):
        guiComboBox.__init__(self, parent, *args)
        self.parent=parent
        self.parentTableName=parentTableName
        self.refresh()
    
    def refresh(self):
        self.clear()    
        searchRec = kuraapp.app.createObject("lng_tag", fields={})
        if self.parentTableName == "lng_lex":
            searchRec.lexeme=True
        elif self.parentTableName=="lng_text":
            searchRec.text=True
        elif self.parentTableName=="lng_stream":
            searchRec.stream=True
        elif self.parentTableName=="lng_element":
            searchRec.element=True
        rows = kuraapp.app.getObjects("lng_tag", searchRec.getFields())
        for row in rows:
            self.insertItem(row.name, row.tag)

    def currentKey(self):
        return unicode(guiComboBox.currentKey(self))


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.4 $"""[11:-2]

__cvslog__="""
    $Log: kuracmbtags.py,v $
    Revision 1.4  2002/11/11 18:19:09  boud
    Fixed a nasty bug that seemingly led to data-loss. Fixed user and
    datestamp functionality.

    Revision 1.3  2002/06/14 13:44:08  boud
    We march on and on and on.

    Revision 1.2  2002/05/24 14:01:27  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
