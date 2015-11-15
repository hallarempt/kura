False = 0
True = 1

from qt import QSpacerItem, QSizePolicy

from guidialog import guiDialog
from guidetaillist import guiDetailList
from guiform import guiForm
from guiconfig import guiConf
import constants

class guiTabDialog(guiDialog):
    def __init__(self, app, parent, title, firstTabTitle,
                 record, mode, tableDef, showChildren = False,
                 addBottomSpring = False):
        
        guiDialog.__init__(self, parent, title, mode, tableDef.hint)

        self.firstTabTitle = firstTabTitle
        self.tableDef = tableDef
        self.hint = tableDef.hint
        if record.getPrimaryKey() == None and self.mode != constants.SEARCH:
            self.mode = constants.INSERT
        else:
            self.mode = mode
        self.app = app

        self.setGeometry(getattr(guiConf, tableDef.name + "_x"),
                         getattr(guiConf, tableDef.name + "_y"),
                         getattr(guiConf, tableDef.name + "_w"),
                         getattr(guiConf, tableDef.name + "_h"))
    
        tabForm = guiForm(self, record, self.mode)
        if addBottomSpring:
            tabForm.grdFields.addItem(QSpacerItem(20,20,
                                                  QSizePolicy.Expanding,
                                                  QSizePolicy.Expanding))
        guiDialog.addChildTab(self, firstTabTitle, tabForm, record)
    
        if (showChildren and self.mode == constants.UPDATE):
            for childName, childDef in self.tableDef.childtables.items():
                self.addAutoChildTab(record, childDef.childTable, childDef)
    
    def addAutoChildTab(self,  parentRec, childTable, childDef):
        tab = guiDetailList(parent = self,
                            app = self.app,
                            parentRecord = parentRec,
                            childTable = childTable)
        guiDialog.addChildTab(self, self.app.getTableLable(childTable),
                              tab, parentRec, constants.DETAIL)


    def accept(self):
        self.saveSize()
        guiDialog.accept(self)
    
    def reject(self):
        self.saveSize()
        guiDialog.reject(self)

    def saveSize(self):
        setattr(guiConf, self.tableDef.name + "_x", self.x())
        setattr(guiConf, self.tableDef.name + "_y", self.y())
        setattr(guiConf, self.tableDef.name + "_w", self.width())
        setattr(guiConf, self.tableDef.name + "_h", self.height())


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.10 $"""[11:-2]

