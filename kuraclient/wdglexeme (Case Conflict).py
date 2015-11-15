# Form implementation generated from reading ui file 'wdgLexeme.ui'
#
# Created: Tue Oct 29 21:40:51 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class tabLexeme(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if name == None:
            self.setName("TabLexeme")

        self.resize(454,297)
        self.setCaption(self.trUtf8("Form1"))

        TabLexemeLayout = QGridLayout(self,1,1,11,6,"TabLexemeLayout")

        self.lblForm = QLabel(self,"lblForm")
        self.lblForm.setText(self.trUtf8("Lexeme"))

        TabLexemeLayout.addMultiCellWidget(self.lblForm,0,0,0,1)

        self.txtForm = QLabel(self,"txtForm")
        self.txtForm.setText(self.trUtf8(""))
        self.txtForm.setFrameShape(QLabel.Panel)
        self.txtForm.setFrameShadow(QLabel.Sunken)
        self.txtForm.setSizePolicy(QSizePolicy(1,0,0,0,self.txtForm.sizePolicy().hasHeightForWidth()))

        TabLexemeLayout.addMultiCellWidget(self.txtForm,0,0,2,4)

        self.txtLanguage = QLabel(self,"txtLanguage")
        self.txtLanguage.setText(self.trUtf8(""))
        self.txtLanguage.setFrameShape(QLabel.Panel)
        self.txtLanguage.setFrameShadow(QLabel.Sunken)
        self.txtLanguage.setSizePolicy(QSizePolicy(1,0,0,0,self.txtLanguage.sizePolicy().hasHeightForWidth()))

        TabLexemeLayout.addMultiCellWidget(self.txtLanguage,4,4,2,4)

        self.lblLanguage = QLabel(self,"lblLanguage")
        self.lblLanguage.setText(self.trUtf8("Language"))

        TabLexemeLayout.addMultiCellWidget(self.lblLanguage,4,4,0,1)

        self.bnZoom = QPushButton(self,"bnZoom")
        self.bnZoom.setText(self.trUtf8("&Edit lexeme"))

        TabLexemeLayout.addWidget(self.bnZoom,5,4)

        self.txtPhoneticForm = QLabel(self,"txtPhoneticForm")
        self.txtPhoneticForm.setText(self.trUtf8(""))
        self.txtPhoneticForm.setFrameShadow(QLabel.Sunken)
        self.txtPhoneticForm.setFrameShape(QLabel.Panel)
        self.txtPhoneticForm.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)
        self.txtPhoneticForm.setSizePolicy(QSizePolicy(5,0,0,0,self.txtPhoneticForm.sizePolicy().hasHeightForWidth()))

        TabLexemeLayout.addMultiCellWidget(self.txtPhoneticForm,2,2,2,4)

        self.lblPhoneticForm = QLabel(self,"lblPhoneticForm")
        self.lblPhoneticForm.setText(self.trUtf8("Phonetic form"))
        self.lblPhoneticForm.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        TabLexemeLayout.addMultiCellWidget(self.lblPhoneticForm,2,2,0,1)

        self.lblGlosse = QLabel(self,"lblGlosse")
        self.lblGlosse.setText(self.trUtf8("Glosse"))

        TabLexemeLayout.addMultiCellWidget(self.lblGlosse,1,1,0,1)

        self.txtDescription = QLabel(self,"txtDescription")
        self.txtDescription.setText(self.trUtf8(""))
        self.txtDescription.setFrameShape(QLabel.Panel)
        self.txtDescription.setFrameShadow(QLabel.Sunken)
        self.txtDescription.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)
        self.txtDescription.setSizePolicy(QSizePolicy(5,7,0,0,self.txtDescription.sizePolicy().hasHeightForWidth()))

        TabLexemeLayout.addMultiCellWidget(self.txtDescription,3,3,2,4)

        self.lblDescription = QLabel(self,"lblDescription")
        self.lblDescription.setText(self.trUtf8("Description"))
        self.lblDescription.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        TabLexemeLayout.addMultiCellWidget(self.lblDescription,3,3,0,1)

        self.txtGlosse = QLabel(self,"txtGlosse")
        self.txtGlosse.setText(self.trUtf8(""))
        self.txtGlosse.setFrameShape(QLabel.Panel)
        self.txtGlosse.setFrameShadow(QLabel.Sunken)
        self.txtGlosse.setSizePolicy(QSizePolicy(7,0,0,0,self.txtGlosse.sizePolicy().hasHeightForWidth()))

        TabLexemeLayout.addMultiCellWidget(self.txtGlosse,1,1,2,4)
        spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        TabLexemeLayout.addItem(spacer,5,0)

        self.bnPick = QPushButton(self,"bnPick")
        self.bnPick.setText(self.trUtf8("&Select lexeme"))

        TabLexemeLayout.addWidget(self.bnPick,5,3)

        self.bnAdd = QPushButton(self,"bnAdd")
        self.bnAdd.setText(self.trUtf8("&Add to lexicon"))

        TabLexemeLayout.addMultiCellWidget(self.bnAdd,5,5,1,2)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = tabLexeme()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
