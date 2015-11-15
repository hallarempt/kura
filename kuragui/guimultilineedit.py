#!/usr/bin/env python

#
# Multi-row edit control
#
from guiconfig import guiConf
from qt import QMultiLineEdit, QFont



class guiMultiLineEdit(QMultiLineEdit):

    def __init__(self, *args):
        apply(QMultiLineEdit.__init__,(self,)+args)
    
        self.setFont(guiConf.textfont)
        self.setWordWrap(QMultiLineEdit.WidgetWidth)

        
    def text(self):
        return unicode(QMultiLineEdit.text(self))

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.3 $"""[11:-2]

__cvslog__="""
    $Log: guimultilineedit.py,v $
    Revision 1.3  2002/12/23 19:49:13  boud
    Changed font to application font.

    Revision 1.2  2002/05/24 14:01:29  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
