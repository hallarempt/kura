#!/usr/bin/env python

#
# Line edit control
#
from guiconfig import guiConf
from qt import QLineEdit, QFont

True = 1
False = 0

class guiLineEdit(QLineEdit):

    def __init__(self, parent, *args):
        QLineEdit.__init__(self, parent, *args)
        self.setFont(guiConf.textfont)
        self.setMaximumHeight(self.sizeHint().height())

    def text(self):
        txt = QLineEdit.text(self)
        if txt.isEmpty():
            return None
        else:
            return unicode(txt)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.6 $"""[11:-2]

__cvslog__="""
    $Log: guilineedit.py,v $
    Revision 1.6  2002/12/23 19:49:13  boud
    Changed font to application font.

    Revision 1.5  2002/11/12 22:12:46  boud
    Bugfixes -- hope nothing else broke.

    Revision 1.4  2002/06/17 14:06:13  boud
    Interlinear texts are back + pychecker checks

    Revision 1.3  2002/06/14 13:45:14  boud
    We march on and on and on.

    Revision 1.2  2002/05/24 14:01:29  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
