import sys

from qt import *

from kuralib import kuraapp
from kuralib.lng_lex import *
  
from kuragui.guitabdialog  import guiTabDialog
from kuragui.guilistview   import guiListView
from kuragui.guidetaillist import guiDetailList
from kuragui.constants     import *

from formtags import TagsTab
from tabtextprojects import tabTextProjects

from resource import *

class dlgText(guiTabDialog):

  def __init__(self, app, parent, title, firstTabTitle, 
            record, mode, tableDef, showChildren=FALSE):
            
    guiTabDialog.__init__(self, app=app, parent=parent, title=title
       , firstTabTitle="&Texts", record=record
       , mode=mode, tableDef=tableDef, showChildren=FALSE)

    self.tagstab=TagsTab(parent, app, record, "lng_text_tag")
    guiTabDialog.addChildTab( self, "&Tags"
                         , self.tagstab, record, DETAIL)


    tabproj=tabTextProjects(parent, app, record)
    guiTabDialog.addChildTab(self, "&Projects"
                         , tabproj, record, DETAIL)

  def accept(self):
    try:
      self.tagstab.formTags.save()
    except Exception, e:
      print "Exception committing texts: ", unicode(e)
      pass
    guiTabDialog.accept(self)



__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.4 $"""[11:-2]
