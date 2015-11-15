from qt import QAction, SIGNAL, PYSIGNAL, QAccel

class guiAction (QAction):
  def __init__(self, parent, accelerator = None):
    QAction.__init__(self, parent)
    self.name=None
    self.dlgSearch=None
    self.dlgForm=None
    self.connect(self, SIGNAL("activated()"), self.slotActivatedName)
    if accelerator:
      QAction.setAccel(self, QAccel.stringToKey(accelerator))
  
  def setName(self, name):
    self.name=name

  def setSearchForm(self, form):
    self.dlgSearch=form
    
  def setForm(self, form):
    self.dlgForm=form
  
  def slotActivatedName(self):
    self.emit( PYSIGNAL("activatedName"),(self.name,) )
  

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/10/28 16:00:40 $
    
    CVS Log:         
    $Log: guiaction.py,v $
    Revision 1.2  2002/10/28 16:00:40  boud
    Begun coding open/save/switch of backends

    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:49  boud
    Manu changes.

    Revision 1.3  2001/01/08 20:55:06  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
