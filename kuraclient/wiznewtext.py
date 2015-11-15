# Form implementation generated from reading ui file 'wiznewtext.ui'
#
# Created: Mon Dec 23 20:49:57 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class wizNewText(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("wizNewText")



        self.pageRecord = QWidget(self,"pageRecord")
        pageRecordLayout = QGridLayout(self.pageRecord,1,1,11,6,"pageRecordLayout")

        self.txtTitle = QLineEdit(self.pageRecord,"txtTitle")
        self.txtTitle.setMaxLength(255)

        pageRecordLayout.addWidget(self.txtTitle,0,3)

        self.txtDescription = QMultiLineEdit(self.pageRecord,"txtDescription")

        pageRecordLayout.addWidget(self.txtDescription,6,3)

        self.txtUrl = QLineEdit(self.pageRecord,"txtUrl")

        pageRecordLayout.addWidget(self.txtUrl,1,3)

        self.cmbLanguage = QComboBox(0,self.pageRecord,"cmbLanguage")

        pageRecordLayout.addWidget(self.cmbLanguage,2,3)

        self.cmbRecording = QComboBox(0,self.pageRecord,"cmbRecording")

        pageRecordLayout.addWidget(self.cmbRecording,3,3)

        self.cmbScan = QComboBox(0,self.pageRecord,"cmbScan")

        pageRecordLayout.addWidget(self.cmbScan,4,3)

        self.txtTranscriptionDate = QLineEdit(self.pageRecord,"txtTranscriptionDate")
        self.txtTranscriptionDate.setMaxLength(12)

        pageRecordLayout.addWidget(self.txtTranscriptionDate,5,3)

        self.lblDataHelp = QLabel(self.pageRecord,"lblDataHelp")
        self.lblDataHelp.setMaximumSize(QSize(175,32767))
        self.lblDataHelp.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        pageRecordLayout.addMultiCellWidget(self.lblDataHelp,0,6,0,0)

        self.lblUrl = QLabel(self.pageRecord,"lblUrl")
        self.lblUrl.setSizePolicy(QSizePolicy(5,5,0,0,self.lblUrl.sizePolicy().hasHeightForWidth()))

        pageRecordLayout.addWidget(self.lblUrl,1,2)

        self.lblLanguage = QLabel(self.pageRecord,"lblLanguage")

        pageRecordLayout.addWidget(self.lblLanguage,2,2)

        self.lblScan = QLabel(self.pageRecord,"lblScan")

        pageRecordLayout.addWidget(self.lblScan,4,2)

        self.lblRecording = QLabel(self.pageRecord,"lblRecording")

        pageRecordLayout.addWidget(self.lblRecording,3,2)

        self.lblTitle = QLabel(self.pageRecord,"lblTitle")

        pageRecordLayout.addWidget(self.lblTitle,0,2)

        self.lblDescription = QLabel(self.pageRecord,"lblDescription")
        self.lblDescription.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        pageRecordLayout.addWidget(self.lblDescription,6,2)

        self.lblTranscriptionDate = QLabel(self.pageRecord,"lblTranscriptionDate")

        pageRecordLayout.addWidget(self.lblTranscriptionDate,5,2)

        self.Line1 = QFrame(self.pageRecord,"Line1")
        self.Line1.setFrameShape(QFrame.VLine)
        self.Line1.setFrameShadow(QFrame.Sunken)
        self.Line1.setFrameShape(QFrame.VLine)

        pageRecordLayout.addMultiCellWidget(self.Line1,0,6,1,1)
        self.addPage(self.pageRecord,"")

        self.pageParsing = QWidget(self,"pageParsing")
        pageParsingLayout = QGridLayout(self.pageParsing,1,1,11,6,"pageParsingLayout")

        self.txtStreamRegExp = QLineEdit(self.pageParsing,"txtStreamRegExp")

        pageParsingLayout.addWidget(self.txtStreamRegExp,1,4)

        self.txtMorphemeRegExp = QLineEdit(self.pageParsing,"txtMorphemeRegExp")

        pageParsingLayout.addWidget(self.txtMorphemeRegExp,3,4)

        self.txtElementRegExp = QLineEdit(self.pageParsing,"txtElementRegExp")

        pageParsingLayout.addWidget(self.txtElementRegExp,2,4)

        self.lblParseHelp = QLabel(self.pageParsing,"lblParseHelp")
        self.lblParseHelp.setMaximumSize(QSize(175,32767))
        self.lblParseHelp.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        pageParsingLayout.addMultiCellWidget(self.lblParseHelp,0,7,0,0)

        self.Line2 = QFrame(self.pageParsing,"Line2")
        self.Line2.setFrameShape(QFrame.VLine)
        self.Line2.setFrameShadow(QFrame.Sunken)
        self.Line2.setFrameShape(QFrame.VLine)

        pageParsingLayout.addMultiCellWidget(self.Line2,0,7,1,2)

        self.chkLexLookup = QCheckBox(self.pageParsing,"chkLexLookup")
        self.chkLexLookup.setChecked(1)

        pageParsingLayout.addMultiCellWidget(self.chkLexLookup,5,5,3,4)

        self.chkElmtLookup = QCheckBox(self.pageParsing,"chkElmtLookup")
        self.chkElmtLookup.setChecked(1)

        pageParsingLayout.addMultiCellWidget(self.chkElmtLookup,4,4,3,4)

        self.grpParser = QGroupBox(self.pageParsing,"grpParser")
        self.grpParser.setColumnLayout(0,Qt.Vertical)
        self.grpParser.layout().setSpacing(6)
        self.grpParser.layout().setMargin(11)
        grpParserLayout = QGridLayout(self.grpParser.layout())
        grpParserLayout.setAlignment(Qt.AlignTop)

        self.rdbRegExp = QRadioButton(self.grpParser,"rdbRegExp")
        self.rdbRegExp.setChecked(1)

        grpParserLayout.addWidget(self.rdbRegExp,0,0)

        self.rdbXML = QRadioButton(self.grpParser,"rdbXML")
        self.rdbXML.setEnabled(0)

        grpParserLayout.addWidget(self.rdbXML,1,0)

        pageParsingLayout.addMultiCellWidget(self.grpParser,0,0,3,4)

        self.lblStreamRegExp = QLabel(self.pageParsing,"lblStreamRegExp")

        pageParsingLayout.addWidget(self.lblStreamRegExp,1,3)

        self.lblElementRegexp = QLabel(self.pageParsing,"lblElementRegexp")

        pageParsingLayout.addWidget(self.lblElementRegexp,2,3)

        self.lblMorphemeRegExp = QLabel(self.pageParsing,"lblMorphemeRegExp")

        pageParsingLayout.addWidget(self.lblMorphemeRegExp,3,3)
        self.addPage(self.pageParsing,"")

        self.pageText = QWidget(self,"pageText")
        pageTextLayout = QGridLayout(self.pageText,1,1,11,6,"pageTextLayout")

        self.bnLoad = QPushButton(self.pageText,"bnLoad")

        pageTextLayout.addWidget(self.bnLoad,0,1)

        self.lblTextHelp = QLabel(self.pageText,"lblTextHelp")
        self.lblTextHelp.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        pageTextLayout.addWidget(self.lblTextHelp,0,0)

        self.progressParsing = QProgressBar(self.pageText,"progressParsing")
        self.progressParsing.setFrameShape(QProgressBar.Panel)

        pageTextLayout.addMultiCellWidget(self.progressParsing,2,2,0,1)

        self.txtRawText = QMultiLineEdit(self.pageText,"txtRawText")

        pageTextLayout.addMultiCellWidget(self.txtRawText,1,1,0,1)
        self.addPage(self.pageText,"")

        self.pageParseTree = QWidget(self,"pageParseTree")
        pageParseTreeLayout = QGridLayout(self.pageParseTree,1,1,11,6,"pageParseTreeLayout")

        self.lsvParseTree = QListView(self.pageParseTree,"lsvParseTree")
        self.lsvParseTree.addColumn(self.tr("Type"))
        self.lsvParseTree.addColumn(self.tr("Text"))
        self.lsvParseTree.addColumn(self.tr("Lexeme"))
        self.lsvParseTree.setRootIsDecorated(1)

        pageParseTreeLayout.addWidget(self.lsvParseTree,0,2)

        self.lblParseTreeHelp = QLabel(self.pageParseTree,"lblParseTreeHelp")
        self.lblParseTreeHelp.setMaximumSize(QSize(175,32767))
        self.lblParseTreeHelp.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        pageParseTreeLayout.addWidget(self.lblParseTreeHelp,0,0)

        self.Line4 = QFrame(self.pageParseTree,"Line4")
        self.Line4.setFrameShape(QFrame.VLine)
        self.Line4.setFrameShadow(QFrame.Sunken)
        self.Line4.setFrameShape(QFrame.VLine)

        pageParseTreeLayout.addWidget(self.Line4,0,1)
        self.addPage(self.pageParseTree,"")

        self.pageProjects = QWidget(self,"pageProjects")
        pageProjectsLayout = QGridLayout(self.pageProjects,1,1,11,6,"pageProjectsLayout")

        self.lsbProjects = QListBox(self.pageProjects,"lsbProjects")
        self.lsbProjects.setSelectionMode(QListBox.Extended)

        pageProjectsLayout.addWidget(self.lsbProjects,0,2)

        self.lblProjectChooser = QLabel(self.pageProjects,"lblProjectChooser")
        self.lblProjectChooser.setMaximumSize(QSize(175,32767))
        self.lblProjectChooser.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        pageProjectsLayout.addWidget(self.lblProjectChooser,0,0)

        self.Line6 = QFrame(self.pageProjects,"Line6")
        self.Line6.setFrameShape(QFrame.VLine)
        self.Line6.setFrameShadow(QFrame.Sunken)
        self.Line6.setFrameShape(QFrame.VLine)

        pageProjectsLayout.addWidget(self.Line6,0,1)
        self.addPage(self.pageProjects,"")

        self.pageReady = QWidget(self,"pageReady")
        pageReadyLayout = QGridLayout(self.pageReady,1,1,11,6,"pageReadyLayout")

        self.lblDone = QLabel(self.pageReady,"lblDone")
        lblDone_font = QFont(self.lblDone.font())
        lblDone_font.setPointSize(24)
        lblDone_font.setBold(1)
        lblDone_font.setItalic(1)
        self.lblDone.setFont(lblDone_font)
        self.lblDone.setAlignment(QLabel.AlignCenter)

        pageReadyLayout.addWidget(self.lblDone,0,0)

        self.lblDoneHelp = QLabel(self.pageReady,"lblDoneHelp")
        self.lblDoneHelp.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        pageReadyLayout.addWidget(self.lblDoneHelp,1,0)
        self.addPage(self.pageReady,"")

        self.languageChange()

        self.resize(QSize(649,416).expandedTo(self.minimumSizeHint()))

        self.setTabOrder(self.txtTitle,self.txtUrl)
        self.setTabOrder(self.txtUrl,self.cmbLanguage)
        self.setTabOrder(self.cmbLanguage,self.cmbRecording)
        self.setTabOrder(self.cmbRecording,self.cmbScan)
        self.setTabOrder(self.cmbScan,self.txtTranscriptionDate)
        self.setTabOrder(self.txtTranscriptionDate,self.txtDescription)
        self.setTabOrder(self.txtDescription,self.rdbRegExp)
        self.setTabOrder(self.rdbRegExp,self.rdbXML)
        self.setTabOrder(self.rdbXML,self.txtStreamRegExp)
        self.setTabOrder(self.txtStreamRegExp,self.txtElementRegExp)
        self.setTabOrder(self.txtElementRegExp,self.txtMorphemeRegExp)
        self.setTabOrder(self.txtMorphemeRegExp,self.chkElmtLookup)
        self.setTabOrder(self.chkElmtLookup,self.chkLexLookup)
        self.setTabOrder(self.chkLexLookup,self.bnLoad)
        self.setTabOrder(self.bnLoad,self.txtRawText)
        self.setTabOrder(self.txtRawText,self.lsvParseTree)
        self.setTabOrder(self.lsvParseTree,self.lsbProjects)

        self.lblUrl.setBuddy(self.txtUrl)
        self.lblLanguage.setBuddy(self.cmbLanguage)
        self.lblScan.setBuddy(self.cmbScan)
        self.lblRecording.setBuddy(self.cmbRecording)
        self.lblTitle.setBuddy(self.txtTitle)
        self.lblDescription.setBuddy(self.txtDescription)

    def languageChange(self):
        self.setCaption(self.tr("Create a new text"))
        QWhatsThis.add(self.txtTranscriptionDate,self.tr("This is the date the text was first transcribed."))
        self.lblDataHelp.setText(self.tr("Enter the basic descriptive data for this text: the title, a freeform description, links to sound recordings and manuscript scans, the basic language of the text and the date the text was transcribed.\n"
"\n"
"The URL can be a link to a website connected with the text. \n"
"\n"
"The language is the basic language of the text: individual phrases and words can be marked to be in another language."))
        self.lblUrl.setText(self.tr("&URL"))
        self.lblLanguage.setText(self.tr("&Language"))
        self.lblScan.setText(self.tr("&Scan"))
        self.lblRecording.setText(self.tr("&Recording"))
        self.lblTitle.setText(self.tr("&Title"))
        self.lblDescription.setText(self.tr("&Description"))
        self.lblTranscriptionDate.setText(self.tr("Date"))
        self.setTitle(self.pageRecord,self.tr("Basic data"))
        self.txtStreamRegExp.setText(self.tr("[.!?\\12]"))
        self.txtMorphemeRegExp.setText(self.tr("[.]"))
        self.txtElementRegExp.setText(self.tr("[ ,:;]"))
        self.lblParseHelp.setText(self.tr("New textual data can be entered in one of two ways: by parsing plain text using regular expressions that look for punctuation of special marks.\n"
"\n"
"Regular expressions can parse a text on three levels: phrases, words and morphemes. \n"
"\n"
"After parsing, the texts must be tagged. \n"
"\n"
"If you want to parse XML text, you must currently use\n"
"the command line."))
        self.chkLexLookup.setText(self.tr("Lookup words and morphemes in the lexicon."))
        self.chkElmtLookup.setText(self.tr("Lookup words and morphemes in other texts"))
        self.grpParser.setTitle(self.tr("Parser"))
        self.rdbRegExp.setText(self.tr("Parse using regular expressions"))
        self.rdbXML.setText(self.tr("Parse XML-markup text"))
        self.lblStreamRegExp.setText(self.tr("Stream regular expression"))
        self.lblElementRegexp.setText(self.tr("Word regular expression"))
        self.lblMorphemeRegExp.setText(self.tr("Morpheme regular expression"))
        self.setTitle(self.pageParsing,self.tr("Determine parsing"))
        self.bnLoad.setText(self.tr("Load from File"))
        self.lblTextHelp.setText(self.tr("Either paste a text (plain text in utf-8 Unicode encoding), or open a text with the Load from File button."))
        self.setTitle(self.pageText,self.tr("Enter the prepared text"))
        self.lsvParseTree.header().setLabel(0,self.tr("Type"))
        self.lsvParseTree.header().setLabel(1,self.tr("Text"))
        self.lsvParseTree.header().setLabel(2,self.tr("Lexeme"))
        self.lblParseTreeHelp.setText(self.tr("You can check the result of the parsing in this treeview. It shows the streams, words and morphemes, and lexemes and morphemes found by these items.\n"
"\n"
"If you want to make corrections, please edit the prepared text and parse again."))
        self.setTitle(self.pageParseTree,self.tr("Check parse tree"))
        self.lblProjectChooser.setText(self.tr("Pick all projects this text is relevant to. You can make an extended selection by pressing CTRL and clicking on a project."))
        self.setTitle(self.pageProjects,self.tr("Choose projects"))
        self.lblDone.setText(self.tr("Done!"))
        self.lblDoneHelp.setText(self.tr("The new text has been parsed; you can now press Finish, and it will be entered in the Kura database. From that moment you can edit and analyze it in the Kura desktop client."))
        self.setTitle(self.pageReady,self.tr("Ready"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = wizNewText()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
