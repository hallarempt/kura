#!/usr/bin/env python

#
# Checkbox control where Y/N is converted to TRUE/False
#
True = 1
False = 0

from qt import QCheckBox

class guiCheckBox(QCheckBox):

    def __init__(self, parent, label, *args):
        apply(QCheckBox.__init__,(self, parent, )+args)
        self.setText(label)
        self.setMaximumHeight(self.sizeHint().height())

    def setChecked(self, value):
        if self.isTristate():
            if value=='J' or value =='j' or value=="1" or value==1:
                QCheckBox.setChecked(self, True)
            elif value is None:
                QCheckBox.setNoChange(self)
            else:
                QCheckBox.setChecked(self, False)
        else:
            if value=='J' or value =='j' or value=="1" or value==1:
                QCheckBox.setChecked(self, True)
            else:
                QCheckBox.setChecked(self, False)

    def isChecked(self):
        if self.isTristate():
            state=QCheckBox.state(self)
            if state == 0:
                return False
            elif state == 2:
                return True
            else:
                return None
        else:
            return QCheckBox.isChecked(self)
        

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.4 $"""[11:-2]

__cvslog__="""
    $Log: guicheckbox.py,v $
    Revision 1.4  2002/10/15 21:07:05  boud
    search, update and delete functionality of file-based backend
    done.

    Revision 1.3  2002/06/17 14:06:13  boud
    Interlinear texts are back + pychecker checks

    Revision 1.2  2002/05/24 14:01:28  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
