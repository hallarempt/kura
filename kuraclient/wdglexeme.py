# Form implementation generated from reading ui file 'wdglexeme.ui'
#
# Created: Mon Dec 23 20:49:57 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class tabLexeme(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("TabLexeme")


        TabLexemeLayout = QGridLayout(self,1,1,11,6,"TabLexemeLayout")

        self.lblForm = QLabel(self,"lblForm")

        TabLexemeLayout.addMultiCellWidget(self.lblForm,0,0,0,1)

        self.txtForm = QLabel(self,"txtForm")
        self.txtForm.setSizePolicy(QSizePolicy(1,0,0,0,self.txtForm.sizePolicy().hasHeightForWidth()))
        self.txtForm.setFrameShape(QLabel.Panel)
        self.txtForm.setFrameShadow(QLabel.Sunken)

        TabLexemeLayout.addMultiCellWidget(self.txtForm,0,0,2,4)

        self.txtLanguage = QLabel(self,"txtLanguage")
        self.txtLanguage.setSizePolicy(QSizePolicy(1,0,0,0,self.txtLanguage.sizePolicy().hasHeightForWidth()))
        self.txtLanguage.setFrameShape(QLabel.Panel)
        self.txtLanguage.setFrameShadow(QLabel.Sunken)

        TabLexemeLayout.addMultiCellWidget(self.txtLanguage,4,4,2,4)

        self.lblLanguage = QLabel(self,"lblLanguage")

        TabLexemeLayout.addMultiCellWidget(self.lblLanguage,4,4,0,1)

        self.bnZoom = QPushButton(self,"bnZoom")

        TabLexemeLayout.addWidget(self.bnZoom,5,4)

        self.txtPhoneticForm = QLabel(self,"txtPhoneticForm")
        self.txtPhoneticForm.setSizePolicy(QSizePolicy(5,0,0,0,self.txtPhoneticForm.sizePolicy().hasHeightForWidth()))
        self.txtPhoneticForm.setFrameShape(QLabel.Panel)
        self.txtPhoneticForm.setFrameShadow(QLabel.Sunken)
        self.txtPhoneticForm.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        TabLexemeLayout.addMultiCellWidget(self.txtPhoneticForm,2,2,2,4)

        self.lblPhoneticForm = QLabel(self,"lblPhoneticForm")
        self.lblPhoneticForm.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        TabLexemeLayout.addMultiCellWidget(self.lblPhoneticForm,2,2,0,1)

        self.lblGlosse = QLabel(self,"lblGlosse")

        TabLexemeLayout.addMultiCellWidget(self.lblGlosse,1,1,0,1)

        self.txtDescription = QLabel(self,"txtDescription")
        self.txtDescription.setSizePolicy(QSizePolicy(5,7,0,0,self.txtDescription.sizePolicy().hasHeightForWidth()))
        self.txtDescription.setFrameShape(QLabel.Panel)
        self.txtDescription.setFrameShadow(QLabel.Sunken)
        self.txtDescription.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        TabLexemeLayout.addMultiCellWidget(self.txtDescription,3,3,2,4)

        self.lblDescription = QLabel(self,"lblDescription")
        self.lblDescription.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        TabLexemeLayout.addMultiCellWidget(self.lblDescription,3,3,0,1)

        self.txtGlosse = QLabel(self,"txtGlosse")
        self.txtGlosse.setSizePolicy(QSizePolicy(7,0,0,0,self.txtGlosse.sizePolicy().hasHeightForWidth()))
        self.txtGlosse.setFrameShape(QLabel.Panel)
        self.txtGlosse.setFrameShadow(QLabel.Sunken)

        TabLexemeLayout.addMultiCellWidget(self.txtGlosse,1,1,2,4)
        spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        TabLexemeLayout.addItem(spacer,5,0)

        self.bnPick = QPushButton(self,"bnPick")

        TabLexemeLayout.addWidget(self.bnPick,5,3)

        self.bnAdd = QPushButton(self,"bnAdd")

        TabLexemeLayout.addMultiCellWidget(self.bnAdd,5,5,1,2)

        self.languageChange()

        self.resize(QSize(454,297).expandedTo(self.minimumSizeHint()))

    def languageChange(self):
        self.setCaption(self.tr("Form1"))
        self.lblForm.setText(self.tr("Lexeme"))
        self.txtForm.setText(QString.null)
        self.txtLanguage.setText(QString.null)
        self.lblLanguage.setText(self.tr("Language"))
        self.bnZoom.setText(self.tr("&Edit lexeme"))
        self.txtPhoneticForm.setText(QString.null)
        self.lblPhoneticForm.setText(self.tr("Phonetic form"))
        self.lblGlosse.setText(self.tr("Glosse"))
        self.txtDescription.setText(QString.null)
        self.lblDescription.setText(self.tr("Description"))
        self.txtGlosse.setText(QString.null)
        self.bnPick.setText(self.tr("&Select lexeme"))
        self.bnAdd.setText(self.tr("&Add to lexicon"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = tabLexeme()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
