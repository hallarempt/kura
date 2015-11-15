# Form implementation generated from reading ui file 'frmlexeme.ui'
#
# Created: Mon Dec 23 20:49:55 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class frmlexeme(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("frmlexeme")

        self.setSizeGripEnabled(1)

        frmlexemeLayout = QGridLayout(self,1,1,11,6,"frmlexemeLayout")

        self.lblLexeme = QLabel(self,"lblLexeme")

        frmlexemeLayout.addWidget(self.lblLexeme,0,0)

        Layout5 = QVBoxLayout(None,0,6,"Layout5")

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout5.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout5.addWidget(self.buttonCancel)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Layout5.addItem(spacer)

        frmlexemeLayout.addMultiCellLayout(Layout5,0,1,2,2)

        self.txtLexeme = QLineEdit(self,"txtLexeme")

        frmlexemeLayout.addWidget(self.txtLexeme,0,1)

        self.tbsLexeme = QTabWidget(self,"tbsLexeme")

        self.tabLexeme = QWidget(self.tbsLexeme,"tabLexeme")
        tabLexemeLayout = QGridLayout(self.tabLexeme,1,1,11,6,"tabLexemeLayout")

        self.txtPhoneticform = QLineEdit(self.tabLexeme,"txtPhoneticform")
        self.txtPhoneticform.setMaxLength(50)

        tabLexemeLayout.addWidget(self.txtPhoneticform,0,1)

        self.lblPhoneticform = QLabel(self.tabLexeme,"lblPhoneticform")

        tabLexemeLayout.addWidget(self.lblPhoneticform,0,0)

        self.lblGlosse = QLabel(self.tabLexeme,"lblGlosse")

        tabLexemeLayout.addWidget(self.lblGlosse,1,0)

        self.txtGlosse = QLineEdit(self.tabLexeme,"txtGlosse")
        self.txtGlosse.setMaxLength(255)

        tabLexemeLayout.addWidget(self.txtGlosse,1,1)

        self.lblDescription = QLabel(self.tabLexeme,"lblDescription")

        tabLexemeLayout.addWidget(self.lblDescription,2,0)

        self.txtDescription = QMultiLineEdit(self.tabLexeme,"txtDescription")

        tabLexemeLayout.addWidget(self.txtDescription,2,1)

        self.lblLanguage = QLabel(self.tabLexeme,"lblLanguage")

        tabLexemeLayout.addWidget(self.lblLanguage,3,0)

        self.cmbLanguage = QComboBox(0,self.tabLexeme,"cmbLanguage")

        tabLexemeLayout.addWidget(self.cmbLanguage,3,1)

        self.lblUser = QLabel(self.tabLexeme,"lblUser")

        tabLexemeLayout.addWidget(self.lblUser,4,0)

        self.txtUser = QLabel(self.tabLexeme,"txtUser")
        self.txtUser.setFrameShape(QLabel.Panel)
        self.txtUser.setFrameShadow(QLabel.Sunken)

        tabLexemeLayout.addWidget(self.txtUser,4,1)

        self.lblDatestamp = QLabel(self.tabLexeme,"lblDatestamp")

        tabLexemeLayout.addWidget(self.lblDatestamp,5,0)

        self.txtDatestamp = QLabel(self.tabLexeme,"txtDatestamp")
        self.txtDatestamp.setFrameShape(QLabel.Panel)
        self.txtDatestamp.setFrameShadow(QLabel.Sunken)

        tabLexemeLayout.addWidget(self.txtDatestamp,5,1)
        self.tbsLexeme.insertTab(self.tabLexeme,"")

        self.tabTags = QWidget(self.tbsLexeme,"tabTags")
        tabTagsLayout = QGridLayout(self.tabTags,1,1,11,6,"tabTagsLayout")

        self.lblTag = QLabel(self.tabTags,"lblTag")

        tabTagsLayout.addWidget(self.lblTag,1,0)

        self.lblValue = QLabel(self.tabTags,"lblValue")

        tabTagsLayout.addWidget(self.lblValue,2,0)

        self.lblNone = QLabel(self.tabTags,"lblNone")
        self.lblNone.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        tabTagsLayout.addWidget(self.lblNone,3,0)

        self.lstTags = QListBox(self.tabTags,"lstTags")

        tabTagsLayout.addMultiCellWidget(self.lstTags,0,0,0,1)

        self.txtNone = QMultiLineEdit(self.tabTags,"txtNone")

        tabTagsLayout.addWidget(self.txtNone,3,1)

        self.txtTagDate = QLabel(self.tabTags,"txtTagDate")

        tabTagsLayout.addWidget(self.txtTagDate,5,0)

        self.lblTagUser = QLabel(self.tabTags,"lblTagUser")

        tabTagsLayout.addWidget(self.lblTagUser,4,0)

        self.txtTagUser = QLabel(self.tabTags,"txtTagUser")
        self.txtTagUser.setFrameShape(QLabel.Panel)
        self.txtTagUser.setFrameShadow(QLabel.Sunken)

        tabTagsLayout.addWidget(self.txtTagUser,4,1)

        self.txtTagDatestamp = QLabel(self.tabTags,"txtTagDatestamp")
        self.txtTagDatestamp.setFrameShape(QLabel.Panel)
        self.txtTagDatestamp.setFrameShadow(QLabel.Sunken)

        tabTagsLayout.addWidget(self.txtTagDatestamp,5,1)

        self.cmbTag = QComboBox(0,self.tabTags,"cmbTag")
        self.cmbTag.setEditable(1)
        self.cmbTag.setDuplicatesEnabled(0)

        tabTagsLayout.addWidget(self.cmbTag,1,1)

        self.cmbValue = QComboBox(0,self.tabTags,"cmbValue")
        self.cmbValue.setSizePolicy(QSizePolicy(3,0,0,0,self.cmbValue.sizePolicy().hasHeightForWidth()))
        self.cmbValue.setEditable(1)

        tabTagsLayout.addWidget(self.cmbValue,2,1)
        self.tbsLexeme.insertTab(self.tabTags,"")

        self.tabFlections = QWidget(self.tbsLexeme,"tabFlections")
        tabFlectionsLayout = QGridLayout(self.tabFlections,1,1,11,6,"tabFlectionsLayout")

        self.lblLexlexuser = QLabel(self.tabFlections,"lblLexlexuser")

        tabFlectionsLayout.addWidget(self.lblLexlexuser,3,0)

        self.lblLexlexDatestamp = QLabel(self.tabFlections,"lblLexlexDatestamp")

        tabFlectionsLayout.addWidget(self.lblLexlexDatestamp,4,0)

        self.txtLexlexuser = QLabel(self.tabFlections,"txtLexlexuser")
        self.txtLexlexuser.setFrameShape(QLabel.Panel)
        self.txtLexlexuser.setFrameShadow(QLabel.Sunken)

        tabFlectionsLayout.addWidget(self.txtLexlexuser,3,1)

        self.txtLexlexDatestamp = QLabel(self.tabFlections,"txtLexlexDatestamp")
        self.txtLexlexDatestamp.setFrameShape(QLabel.Panel)
        self.txtLexlexDatestamp.setFrameShadow(QLabel.Sunken)

        tabFlectionsLayout.addWidget(self.txtLexlexDatestamp,4,1)

        self.lstRelatedForms = QListBox(self.tabFlections,"lstRelatedForms")

        tabFlectionsLayout.addMultiCellWidget(self.lstRelatedForms,0,0,0,2)

        self.cmbRelationcode = QComboBox(0,self.tabFlections,"cmbRelationcode")
        self.cmbRelationcode.setSizePolicy(QSizePolicy(7,0,0,0,self.cmbRelationcode.sizePolicy().hasHeightForWidth()))

        tabFlectionsLayout.addWidget(self.cmbRelationcode,1,1)

        self.lblRelation = QLabel(self.tabFlections,"lblRelation")

        tabFlectionsLayout.addWidget(self.lblRelation,1,0)

        self.lblRelatedLexeme = QLabel(self.tabFlections,"lblRelatedLexeme")

        tabFlectionsLayout.addWidget(self.lblRelatedLexeme,2,0)

        self.txtRelatedlexeme = QLabel(self.tabFlections,"txtRelatedlexeme")
        self.txtRelatedlexeme.setFrameShape(QLabel.Panel)
        self.txtRelatedlexeme.setFrameShadow(QLabel.Sunken)

        tabFlectionsLayout.addWidget(self.txtRelatedlexeme,2,1)

        self.bnGetLexeme = QPushButton(self.tabFlections,"bnGetLexeme")

        tabFlectionsLayout.addWidget(self.bnGetLexeme,2,2)
        self.tbsLexeme.insertTab(self.tabFlections,"")

        self.tabCorpus = QWidget(self.tbsLexeme,"tabCorpus")
        tabCorpusLayout = QGridLayout(self.tabCorpus,1,1,11,6,"tabCorpusLayout")

        self.htmlCorpus = QTextView(self.tabCorpus,"htmlCorpus")

        tabCorpusLayout.addWidget(self.htmlCorpus,0,0)
        self.tbsLexeme.insertTab(self.tabCorpus,"")

        self.tabPreview = QWidget(self.tbsLexeme,"tabPreview")
        tabPreviewLayout = QGridLayout(self.tabPreview,1,1,11,6,"tabPreviewLayout")

        self.htmlPreview = QTextBrowser(self.tabPreview,"htmlPreview")

        tabPreviewLayout.addWidget(self.htmlPreview,0,0)
        self.tbsLexeme.insertTab(self.tabPreview,"")

        frmlexemeLayout.addMultiCellWidget(self.tbsLexeme,1,1,0,1)

        self.languageChange()

        self.resize(QSize(527,445).expandedTo(self.minimumSizeHint()))

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))

        self.setTabOrder(self.buttonOk,self.buttonCancel)

        self.lblLexeme.setBuddy(self.txtLexeme)
        self.lblPhoneticform.setBuddy(self.txtPhoneticform)
        self.lblGlosse.setBuddy(self.txtGlosse)
        self.lblDescription.setBuddy(self.txtDescription)
        self.lblLanguage.setBuddy(self.cmbLanguage)
        self.lblTag.setBuddy(self.cmbTag)
        self.lblRelation.setBuddy(self.cmbRelationcode)

    def languageChange(self):
        self.setCaption(self.tr("Lexical item"))
        self.lblLexeme.setText(self.tr("&Lexeme"))
        self.buttonOk.setText(self.tr("&OK"))
        self.buttonCancel.setText(self.tr("&Cancel"))
        self.lblPhoneticform.setText(self.tr("&Phonetic form"))
        self.lblGlosse.setText(self.tr("&Glosse"))
        self.txtGlosse.setText(QString.null)
        self.lblDescription.setText(self.tr("&Description"))
        self.lblLanguage.setText(self.tr("&Language"))
        self.lblUser.setText(self.tr("User"))
        self.txtUser.setText(QString.null)
        self.lblDatestamp.setText(self.tr("Last changed"))
        self.txtDatestamp.setText(QString.null)
        self.tbsLexeme.changeTab(self.tabLexeme,self.tr("&Lexeme"))
        self.lblTag.setText(self.tr("Tag"))
        self.lblValue.setText(self.tr("&Value"))
        self.lblNone.setText(self.tr("&Note"))
        self.txtTagDate.setText(self.tr("Last changed"))
        self.lblTagUser.setText(self.tr("User"))
        self.txtTagUser.setText(QString.null)
        self.txtTagDatestamp.setText(QString.null)
        self.tbsLexeme.changeTab(self.tabTags,self.tr("&Tags"))
        self.lblLexlexuser.setText(self.tr("User"))
        self.lblLexlexDatestamp.setText(self.tr("Last changed"))
        self.txtLexlexuser.setText(QString.null)
        self.txtLexlexDatestamp.setText(QString.null)
        self.lstRelatedForms.clear()
        self.lstRelatedForms.insertItem(self.tr("New Item"))
        self.lblRelation.setText(self.tr("&Relation type"))
        self.lblRelatedLexeme.setText(self.tr("Related lexeme"))
        self.txtRelatedlexeme.setText(QString.null)
        self.bnGetLexeme.setText(self.tr("&Select Lexeme"))
        self.tbsLexeme.changeTab(self.tabFlections,self.tr("&Related Forms"))
        self.tbsLexeme.changeTab(self.tabCorpus,self.tr("&Corpus"))
        self.tbsLexeme.changeTab(self.tabPreview,self.tr("&Preview"))

    def reselectValues(self,a0):
        print "frmlexeme.reselectValues(tag): Not implemented yet"


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = frmlexeme()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
