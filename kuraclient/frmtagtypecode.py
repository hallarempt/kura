# Form implementation generated from reading ui file 'frmtagtypecode.ui'
#
# Created: Mon Dec 23 20:49:57 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class frmtagtypecode(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("frmtagtypecode")

        self.setSizeGripEnabled(1)

        frmtagtypecodeLayout = QGridLayout(self,1,1,11,6,"frmtagtypecodeLayout")

        Layout1 = QHBoxLayout(None,0,6,"Layout1")
        spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(spacer)

        self.buttonApply = QPushButton(self,"buttonApply")
        self.buttonApply.setAutoDefault(1)
        Layout1.addWidget(self.buttonApply)

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)

        frmtagtypecodeLayout.addLayout(Layout1,1,0)

        self.tabTagtype = QTabWidget(self,"tabTagtype")

        self.tab = QWidget(self.tabTagtype,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.txtTypeCode = QLineEdit(self.tab,"txtTypeCode")
        self.txtTypeCode.setMaxLength(5)

        tabLayout.addWidget(self.txtTypeCode,0,1)

        self.lblTypeCode = QLabel(self.tab,"lblTypeCode")

        tabLayout.addWidget(self.lblTypeCode,0,0)

        self.txtDescription = QLineEdit(self.tab,"txtDescription")
        self.txtDescription.setMaxLength(255)

        tabLayout.addWidget(self.txtDescription,1,1)

        self.lblDescription = QLabel(self.tab,"lblDescription")

        tabLayout.addWidget(self.lblDescription,1,0)

        self.grpContext = QButtonGroup(self.tab,"grpContext")
        self.grpContext.setExclusive(1)
        self.grpContext.setColumnLayout(0,Qt.Vertical)
        self.grpContext.layout().setSpacing(6)
        self.grpContext.layout().setMargin(11)
        grpContextLayout = QGridLayout(self.grpContext.layout())
        grpContextLayout.setAlignment(Qt.AlignTop)

        self.rdbValue = QRadioButton(self.grpContext,"rdbValue")

        grpContextLayout.addWidget(self.rdbValue,1,0)

        self.rdbReference = QRadioButton(self.grpContext,"rdbReference")

        grpContextLayout.addWidget(self.rdbReference,3,0)

        self.rdbDomain = QRadioButton(self.grpContext,"rdbDomain")

        grpContextLayout.addWidget(self.rdbDomain,0,0)

        self.rdbNote = QRadioButton(self.grpContext,"rdbNote")

        grpContextLayout.addWidget(self.rdbNote,2,0)

        tabLayout.addMultiCellWidget(self.grpContext,2,2,0,1)
        self.tabTagtype.insertTab(self.tab,"")

        frmtagtypecodeLayout.addWidget(self.tabTagtype,0,0)

        self.languageChange()

        self.resize(QSize(398,293).expandedTo(self.minimumSizeHint()))

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))

        self.setTabOrder(self.txtTypeCode,self.txtDescription)
        self.setTabOrder(self.txtDescription,self.rdbDomain)
        self.setTabOrder(self.rdbDomain,self.rdbValue)
        self.setTabOrder(self.rdbValue,self.rdbNote)
        self.setTabOrder(self.rdbNote,self.rdbReference)
        self.setTabOrder(self.rdbReference,self.buttonApply)
        self.setTabOrder(self.buttonApply,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)
        self.setTabOrder(self.buttonCancel,self.tabTagtype)

        self.lblTypeCode.setBuddy(self.txtTypeCode)
        self.lblDescription.setBuddy(self.txtDescription)

    def languageChange(self):
        self.setCaption(self.tr("Tag type definition"))
        self.buttonApply.setText(self.tr("&Apply"))
        self.buttonOk.setText(self.tr("&OK"))
        self.buttonCancel.setText(self.tr("&Cancel"))
        self.lblTypeCode.setText(self.tr("&Type"))
        self.lblDescription.setText(self.tr("&Description"))
        self.grpContext.setTitle(self.tr("Origin of tag values"))
        self.rdbValue.setText(self.tr("Type a shortish value"))
        self.rdbReference.setText(self.tr("Take value from a picklist of references"))
        self.rdbDomain.setText(self.tr("Take value from a picklist of abbreviations"))
        self.rdbNote.setText(self.tr("Type a longish note"))
        self.tabTagtype.changeTab(self.tab,self.tr("Tag type"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = frmtagtypecode()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
