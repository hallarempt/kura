False = 0

from kuralib.lng_lex import *
  
from kuragui.guitabdialog import guiTabDialog
from kuragui import constants

from formtags import TagsTab
from tablexlex  import tabLexLex

class dlgLexeme(guiTabDialog):

    def __init__(self, app, parent, title, firstTabTitle, 
                 record, mode, tableDef, showChildren=False):
        guiTabDialog.__init__(self, app=app, parent = parent, title=title,
                              firstTabTitle = "&Lexemes", record = record,
                              mode=mode, tableDef = tableDef,
                              showChildren = False)

        self.tagstab = TagsTab(parent, app, record, "lng_lex_tag")
        guiTabDialog.addChildTab(self, "&Tags",
                                 self.tagstab, record,
                                 constants.DETAIL)


        tabLxLx = tabLexLex(parent, app, record)
        guiTabDialog.addChildTab(self, "&Relations",
                                 tabLxLx, record,
                                 constants.DETAIL)
      
    def accept(self):
        self.tagstab.formTags.save()
        guiTabDialog.accept(self)

     

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.8 $"""[11:-2]
