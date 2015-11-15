False = 0
True = 1

from qt import QObject, SIGNAL, PYSIGNAL, QListViewItem, QMessageBox, QFont

from dbobj import dbexceptions

from frmlexrelation import frmLexRelation

from kuralib import kuraapp

from kuragui.comboproxy import ComboProxy
from kuragui.guiconfig import guiConf


def nullifyEmptyQString(s):
    if s.isEmpty():
         return None
    else:
         return unicode(s)

class ListViewProxy(QObject):

    def __init__(self, listView, tableName, headers):
        QObject.__init__(self)
        self.listView = listView
        self.tableName = tableName
        self.rows={}
        self.headers = headers

        self.connect(self.listView, SIGNAL("doubleClicked(QListViewItem *)"),
                     self.slotItemSelected)


    def slotItemSelected(self):
        self.emit(PYSIGNAL("sigItemSelected"),
                  (self.rows[self.listView.currentItem()],
                  self.listView.currentItem()))


    def slotAddItem(self, rec, otherLvi = None):
        """
        Add a record to the listview and the cache.
        """
        lvi = QListViewItem(self.listView)
        col = 0
        for fieldname in self.headers:
            lvi.setText(col, rec.getFieldValue(fieldname))
            col += 1   
        self.rows[lvi] = rec

        if otherLvi != None:
            self.emit(PYSIGNAL("sigItemAdded"), (rec, otherLvi))


    def currentRecord(self):
        return self.rows[self.listView.currentItem()]


    def slotDeleteItem(self, rec, lvi):
        del self.rows[lvi]
        self.listView.takeItem(lvi)

    def refresh(self, searchRec):
        self.listView.clear()
        self.rows = {}
        rows = kuraapp.app.getObjects(self.tableName,
                                      fields = searchRec.getFields())
        for row in rows:
            self.slotAddItem(row)

    def refreshRows(self, rows, filterRows):
        self.listView.clear()
        self.rows={}
        for row in rows:
            if row.getPrimaryKey() not in filterRows:
                self.slotAddItem(row)

class dlgLexRelation(frmLexRelation):

    def __init__(self, parent, parentRecord):

        frmLexRelation.__init__(self, parent = parent,
                                name = "dlgLexRel", modal = True)
        font = QFont(guiConf.textfontfamily, guiConf.textfontsize)
        self.txtForm.setFont(font)
        self.txtPhoneticForm.setFont(font)
        self.txtGlosse.setFont(font)
        self.cmbLanguage.setFont(font)
        self.lsvChosen.setFont(font)
        self.lsvSource.setFont(font)
        self.cmbRelationCode.setFont(font)
        
        self.parentRecord = parentRecord

        self.cmbLanguageProxy = ComboProxy(comboBox = self.cmbLanguage,
                                           table = kuraapp.app.getObjects("lng_language"),
                                           currentKey = parentRecord.languagenr)
        self.cmbRelationCodeProxy = ComboProxy(comboBox = self.cmbRelationCode,
                                               table = kuraapp.app.getObjects("lng_lxlxrelcode"))
        self.lsvSourceProxy = ListViewProxy(listView = self.lsvSource,
                                            tableName = "lng_lex",
                                            headers = ["form", "glosse", "language"])
        self.lsvChosenProxy = ListViewProxy(listView = self.lsvChosen,
                                            tableName = "lng_lex_lex",
                                            headers = ["form_2","relation"])

        self.connect(self.bnFilter, SIGNAL("clicked()"), self.refreshSource)

        self.connect(self.lsvSourceProxy, PYSIGNAL("sigItemSelected"),
                     self.convertLexemeToLexLex)
        self.connect(self.lsvSourceProxy, PYSIGNAL("sigItemAdded"),
                     self.lsvChosenProxy.slotDeleteItem)
        self.connect(self.lsvChosenProxy, PYSIGNAL("sigItemSelected"),
                     self.convertLexLexToLexeme)
        self.connect(self.lsvChosenProxy, PYSIGNAL("sigItemAdded"),
                     self.lsvSourceProxy.slotDeleteItem)
        self.connect(self.buttonHelp, SIGNAL("clicked()"),
                     self.slotHelp)

    def slotHelp(self):
        QMessageBox.about(self, "Adding sets of lexemes",
  """
  Using this dialog sets of lexemes can be added to the set of lexemes that are
  in some way related to the lexeme you're editing in the dialog box under this 
  one.

  Enter some filter expressions in the box top left - use % for bits you want the
  system to fill in. Then press the filter button. The list bottom left is filled
  with possibles. Choose a default relation type from the drop-down list, and
  double-click on the items you want to add. Double-click on added items to
  remove them.
  """)

    def convertLexemeToLexLex(self, lexRec, lvi):
        lexLexRec = kuraapp.app.createObject("lng_lex_lex",
                                             lexnr_1 = self.parentRecord.lexnr,
                                             form_1 = self.parentRecord.form,
                                             lexnr_2 = lexRec.lexnr,
                                             form_2 = lexRec.form,
                                             lxlxrelcode = self.cmbRelationCodeProxy.currentKey(),
                                             relation = self.cmbRelationCodeProxy.currentText(),
                                             usernr = guiConf.usernr)

        self.lsvChosenProxy.slotAddItem(lexLexRec, lvi)

    def convertLexLexToLexeme(self, lxlxRec, lvi):
        lexemeRec=kuraapp.app.getObject("lng_lex", lexnr = lxlxRec.lexnr_2)
        self.lsvSourceProxy.slotAddItem(lexemeRec, lvi)


    
    def refreshSource(self):
        form = self.txtGlosse.text()
           
        rows = kuraapp.app.getObjects("lng_lex",
                                      form = nullifyEmptyQString(self.txtForm.text()),
                                      phonetic_form = nullifyEmptyQString(self.txtPhoneticForm.text()),
                                      glosse = nullifyEmptyQString(self.txtGlosse.text()),
                                      languagenr = self.cmbLanguageProxy.currentKey())
        #
        # Get record from child languages
        #
        if self.chkChildrenIncluded.isChecked() == True:
            languageRec = kuraapp.app.createObject("lng_language",
                                                   languagenr = self.cmbLanguageProxy.currentKey())
            childLanguages = languageRec.getChildLanguages()
            for language in childLanguages:
                rows = rows + kuraapp.app.getObjects("lng_lex",
                                                     form = nullifyEmptyQString(self.txtForm.text()),
                                                     phonetic_form =
                                                         nullifyEmptyQString(self.txtPhoneticForm.text()),
                                                     glosse = nullifyEmptyQString(self.txtGlosse.text()),
                                                     languagenr = language.languagenr)

        #
        # FIXME: filter already chosen items out!
        #
        self.lsvSourceProxy.refreshRows(rows, [self.parentRecord.getPrimaryKey()])

    def accept(self):
        for rec in self.lsvChosenProxy.rows.values():
            try:
                if rec.lxlxnr == None:
                    rec.insert()
                else:
                    rec.update()
            except dbexceptions.dbError, dberr:
                QMessageBox.information(self, "Kura Error", dberr.errorMessage)
            else:    
                self.emit(PYSIGNAL("sigAcceptData"),())
                frmLexRelation.accept(self)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.5 $"""[11:-2]

__cvslog__="""
    $Log: dlglexrelation.py,v $
    Revision 1.5  2002/11/09 14:54:39  boud
    Added manual target, fixed lots of small bugs, added text to manual.

    Revision 1.4  2002/11/06 18:27:44  boud
    Added start of manual, fixed but with lexical relations.

    Revision 1.3  2002/07/30 11:34:37  boud
    Fixes, fixes, fixes...

    Revision 1.2  2002/05/24 14:01:27  boud
    Converted most files to new coding standards + new config standard.

 ***************************************************************************/
"""
