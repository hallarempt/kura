import sys

True = 1
False = 0

from qt import QObject, SIGNAL, SLOT, QApplication,\
     QDialog, QComboBox, PYSIGNAL
try:
    from kuralib import kuraapp
except:
    sys.path.append("..")
    from kuralib import kuraapp

from kuragui.guiconfig import guiConf

True=1
False=0

class ComboProxy(QObject):
    """
    This class proxies for a standard QComboBox to provide 
    a picklist filled from the database. This class does
    not use the record.picklist functionality, since it
    is intended for situations where there isn't a record.
    """
    def __init__(self, comboBox, table, currentKey=None, nullAllowed=False):
        QObject.__init__(self)
        self.comboBox=comboBox
        
        self.key_to_index={}
        self.index_to_key={}
    
        if nullAllowed:
            self.comboBox.insertItem("<None>")
            self.key_to_index[None]=self.comboBox.count()-1
            self.index_to_key[self.comboBox.count()-1]=None

        for row in table:
            self.comboBox.insertItem(row.getDescription())
            primaryKey = row.getPrimaryKey()
            self.key_to_index[primaryKey] = self.comboBox.count()-1
            self.index_to_key[self.comboBox.count()-1] = primaryKey
         
        if currentKey!=None:
            self.setCurrentItem(currentKey)

        self.connect(self.comboBox, SIGNAL("activated (int)"),
                     self.slotItemSelected)
        self.comboBox.setAutoCompletion(True)
   
    def currentText(self):
        return unicode(self.comboBox.currentText())
    
    def currentKey(self):
        try:
            return self.index_to_key[self.comboBox.currentItem()]
        except KeyError:
            return None

    def setCurrentItem(self, key):
        if self.key_to_index.has_key(key):
            self.comboBox.setCurrentItem(self.key_to_index[key])

    def slotItemSelected(self, index):
        try:
            rec=self.index_to_key[index]
            self.emit(PYSIGNAL("recSelected"),(rec, index))
        except KeyError:
            pass


def main(args):
    qapp=QApplication(sys.argv)
    kuraapp.initApp(str(guiConf.username),
                    str(guiConf.database),
                    str(guiConf.password),
                    str(guiConf.hostname))
    
    kuraapp.initCurrentEnvironment(1, 1, 1)
        
    mainwin = QDialog()
    combobox = QComboBox(mainwin)
    comboproxy = ComboProxy(combobox,
                            kuraapp.app.getObjects("lng_user"),
                            guiConf.usernr)
    mainwin.show()
    qapp.connect(qapp, SIGNAL('lastWindowClosed()'), qapp, SLOT('quit()'))
    qapp.exec_loop()
    

if __name__ == "__main__":
    main(sys.argv)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.4 $
    Last edited          : $Date: 2002/11/02 15:51:41 $
 ***************************************************************************/
"""
