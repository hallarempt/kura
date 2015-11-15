from qt             import *

from dbobj.dbobj    import dbError

from frmlexchooser  import frmLexChooser
from kuragui.comboproxy import ComboProxy

from resource       import *
from kuralib import kuraapp
from kuragui.guiconfig import guiConf


from dlglexrelation import nullifyEmptyQString
from dlglexrelation import ListViewProxy


class dlgLexChooser(frmLexChooser):

  def __init__(self, parent, parentRecord):
  
    frmLexChooser.__init__(self, parent=parent
                               , name="dlgLexChooser"
                               , modal=TRUE)
    
    self.txtForm.setFont(guiConf.widgetfont)
    self.txtPhoneticForm.setFont(guiConf.widgetfont)
    self.txtGlosse.setFont(guiConf.widgetfont)
    self.cmbLanguage.setFont(guiConf.widgetfont)
    self.lsvSource.setFont(guiConf.widgetfont)
    
    self.parentRecord=parentRecord
    
    self.cmbLanguageProxy=ComboProxy(self.cmbLanguage,
                                     kuraapp.app.getObjects("lng_language"),
                                     currentKey=parentRecord.languagenr)
    self.lsvSourceProxy=ListViewProxy(listView=self.lsvSource,
                                      tableName="lng_lex",
                                      headers=["form", "glosse", "language"])
    self.connect(self.buttonCancel, SIGNAL("clicked()"), self.reject)
    self.connect(self.lsvSourceProxy,
                 PYSIGNAL("sigItemSelected"),
                 self.slotItemChosen)
    self.connect(self.bnFilter, SIGNAL("clicked()"), self.refreshSource)
    self.connect(self.buttonOk, SIGNAL("clicked()"), self.accept)
    self.connect(self.buttonCancel, SIGNAL("clicked()"), self.reject)
    self.connect(self.buttonHelp, SIGNAL("clicked()"), self.slotHelp)
    
  def slotHelp(self):
    QMessageBox.about(self, "Picking a lexeme to go with a morpheme",
"""
A lot of morphemes have a direct representation in the lexicon. You won't
find a plural suffix in the lexicon, but the name of an object will have
an entry. This dialog is used to pick the lexical entry that's the same
as the morpheme you're editing. (Of course, one day, Kura will be able to
do the groundwork for you, leaving you to dither over the more specific items.)

You might also want to pick a lexical item from another language, for instance,
in the case of loanwords.
"""    )
    
  
  def refreshSource(self):
    rows = kuraapp.app.getObjects("lng_lex",
                                  form = nullifyEmptyQString(self.txtForm.text()),
                                  phonetic_form = nullifyEmptyQString(self.txtPhoneticForm.text()),
                                  glosse = nullifyEmptyQString(self.txtGlosse.text()),
                                  languagenr = self.cmbLanguageProxy.currentKey())
    #
    # Get record from child languages
    #
    if self.chkChildrenIncluded.isChecked()==TRUE:
      languageRec=kuraapp.app.createObject("lng_language",
                                           languagenr=self.cmbLanguageProxy.currentKey())
      childLanguages=languageRec.getChildLanguages()
      for language in childLanguages:
        rows = rows + kuraapp.app.getObjects("lng_lex",
                                             form = nullifyEmptyQString(self.txtForm.text()),
                                             phonetic_form =
                                             nullifyEmptyQString(self.txtPhoneticForm.text()),
                                             glosse = nullifyEmptyQString(self.txtGlosse.text()),
                                             languagenr = language.languagenr)
    self.lsvSourceProxy.refreshRows(rows, [])

  def slotItemChosen(self, item, record):
    self.accept()

  def accept(self):
    try:
      self.masterRecord=self.lsvSourceProxy.currentRecord()
      frmLexChooser.accept(self)
    except:
      frmLexChooser.reject(self)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.6 $"""[11:-2]


