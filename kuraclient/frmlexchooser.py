# Form implementation generated from reading ui file 'frmlexchooser.ui'
#
# Created: Mon Dec 23 20:49:55 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class frmLexChooser(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("frmLexChooser")

        self.setSizeGripEnabled(1)

        frmLexChooserLayout = QGridLayout(self,1,1,11,6,"frmLexChooserLayout")

        self.grpFilter = QGroupBox(self,"grpFilter")
        self.grpFilter.setColumnLayout(0,Qt.Vertical)
        self.grpFilter.layout().setSpacing(6)
        self.grpFilter.layout().setMargin(11)
        grpFilterLayout = QGridLayout(self.grpFilter.layout())
        grpFilterLayout.setAlignment(Qt.AlignTop)

        self.txtForm = QLineEdit(self.grpFilter,"txtForm")

        grpFilterLayout.addWidget(self.txtForm,0,1)

        self.txtPhoneticForm = QLineEdit(self.grpFilter,"txtPhoneticForm")

        grpFilterLayout.addWidget(self.txtPhoneticForm,1,1)

        self.txtGlosse = QLineEdit(self.grpFilter,"txtGlosse")

        grpFilterLayout.addWidget(self.txtGlosse,2,1)

        self.cmbLanguage = QComboBox(0,self.grpFilter,"cmbLanguage")
        self.cmbLanguage.setAutoCompletion(0)

        grpFilterLayout.addWidget(self.cmbLanguage,3,1)

        self.lblForm = QLabel(self.grpFilter,"lblForm")

        grpFilterLayout.addWidget(self.lblForm,0,0)

        self.lblPhoneticForm = QLabel(self.grpFilter,"lblPhoneticForm")

        grpFilterLayout.addWidget(self.lblPhoneticForm,1,0)

        self.lblGlosse = QLabel(self.grpFilter,"lblGlosse")

        grpFilterLayout.addWidget(self.lblGlosse,2,0)

        self.lblLanguage = QLabel(self.grpFilter,"lblLanguage")

        grpFilterLayout.addWidget(self.lblLanguage,3,0)

        self.chkChildrenIncluded = QCheckBox(self.grpFilter,"chkChildrenIncluded")

        grpFilterLayout.addMultiCellWidget(self.chkChildrenIncluded,4,4,0,1)

        self.bnFilter = QPushButton(self.grpFilter,"bnFilter")

        grpFilterLayout.addMultiCellWidget(self.bnFilter,5,5,0,1)

        frmLexChooserLayout.addWidget(self.grpFilter,0,0)

        self.grpLexemes = QGroupBox(self,"grpLexemes")
        self.grpLexemes.setColumnLayout(0,Qt.Vertical)
        self.grpLexemes.layout().setSpacing(6)
        self.grpLexemes.layout().setMargin(11)
        grpLexemesLayout = QGridLayout(self.grpLexemes.layout())
        grpLexemesLayout.setAlignment(Qt.AlignTop)

        self.lblSource = QLabel(self.grpLexemes,"lblSource")

        grpLexemesLayout.addWidget(self.lblSource,1,0)

        self.lsvSource = QListView(self.grpLexemes,"lsvSource")
        self.lsvSource.addColumn(self.tr("Form"))
        self.lsvSource.addColumn(self.tr("Glosse"))
        self.lsvSource.addColumn(self.tr("Language"))

        grpLexemesLayout.addWidget(self.lsvSource,2,0)

        frmLexChooserLayout.addWidget(self.grpLexemes,1,0)

        Layout5 = QVBoxLayout(None,0,6,"Layout5")

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout5.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout5.addWidget(self.buttonCancel)

        self.buttonHelp = QPushButton(self,"buttonHelp")
        self.buttonHelp.setAutoDefault(1)
        Layout5.addWidget(self.buttonHelp)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Layout5.addItem(spacer)

        frmLexChooserLayout.addMultiCellLayout(Layout5,0,1,1,1)

        self.languageChange()

        self.resize(QSize(560,537).expandedTo(self.minimumSizeHint()))

        self.setTabOrder(self.txtForm,self.txtPhoneticForm)
        self.setTabOrder(self.txtPhoneticForm,self.txtGlosse)
        self.setTabOrder(self.txtGlosse,self.cmbLanguage)
        self.setTabOrder(self.cmbLanguage,self.chkChildrenIncluded)
        self.setTabOrder(self.chkChildrenIncluded,self.bnFilter)
        self.setTabOrder(self.bnFilter,self.lsvSource)
        self.setTabOrder(self.lsvSource,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)
        self.setTabOrder(self.buttonCancel,self.buttonHelp)

        self.lblForm.setBuddy(self.txtForm)
        self.lblPhoneticForm.setBuddy(self.txtPhoneticForm)
        self.lblGlosse.setBuddy(self.txtGlosse)
        self.lblLanguage.setBuddy(self.cmbLanguage)

    def languageChange(self):
        self.setCaption(self.tr("Pick a lexeme"))
        self.grpFilter.setTitle(self.tr("Filter"))
        self.lblForm.setText(self.tr("&Form"))
        self.lblPhoneticForm.setText(self.tr("&Phonetic form"))
        self.lblGlosse.setText(self.tr("&Glosse"))
        self.lblLanguage.setText(self.tr("&Language"))
        self.chkChildrenIncluded.setText(self.tr("&Include lexemes from child languages"))
        self.bnFilter.setText(self.tr("&Apply Filter"))
        self.grpLexemes.setTitle(self.tr("Lexemes"))
        self.lblSource.setText(self.tr("Possible lexemes - select one."))
        self.lsvSource.header().setLabel(0,self.tr("Form"))
        self.lsvSource.header().setLabel(1,self.tr("Glosse"))
        self.lsvSource.header().setLabel(2,self.tr("Language"))
        self.buttonOk.setText(self.tr("&OK"))
        self.buttonCancel.setText(self.tr("&Cancel"))
        self.buttonHelp.setText(self.tr("&Help"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = frmLexChooser()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
