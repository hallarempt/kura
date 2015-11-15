# Form implementation generated from reading ui file 'frmlogin.ui'
#
# Created: Mon Dec 23 20:49:56 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class frmLogin(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("frmLogin")

        self.setSizePolicy(QSizePolicy(1,1,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setSizeGripEnabled(0)

        frmLoginLayout = QVBoxLayout(self,11,6,"frmLoginLayout")

        Layout6 = QGridLayout(None,1,1,0,6,"Layout6")

        self.txtUsername = QLineEdit(self,"txtUsername")

        Layout6.addWidget(self.txtUsername,0,1)

        self.lblDatabase = QLabel(self,"lblDatabase")

        Layout6.addWidget(self.lblDatabase,2,0)

        self.lblUsername = QLabel(self,"lblUsername")

        Layout6.addWidget(self.lblUsername,0,0)

        self.txtHost = QLineEdit(self,"txtHost")

        Layout6.addWidget(self.txtHost,3,1)

        self.txtPassword = QLineEdit(self,"txtPassword")
        self.txtPassword.setEchoMode(QLineEdit.Password)

        Layout6.addWidget(self.txtPassword,1,1)

        self.lblHost = QLabel(self,"lblHost")

        Layout6.addWidget(self.lblHost,3,0)

        self.txtDatabase = QLineEdit(self,"txtDatabase")

        Layout6.addWidget(self.txtDatabase,2,1)

        self.lblPassword = QLabel(self,"lblPassword")

        Layout6.addWidget(self.lblPassword,1,0)
        frmLoginLayout.addLayout(Layout6)

        Layout1 = QHBoxLayout(None,0,6,"Layout1")
        spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(spacer)

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)
        frmLoginLayout.addLayout(Layout1)

        self.languageChange()

        self.resize(QSize(418,182).expandedTo(self.minimumSizeHint()))

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))

        self.setTabOrder(self.txtUsername,self.txtPassword)
        self.setTabOrder(self.txtPassword,self.txtDatabase)
        self.setTabOrder(self.txtDatabase,self.txtHost)
        self.setTabOrder(self.txtHost,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)

        self.lblDatabase.setBuddy(self.txtDatabase)
        self.lblUsername.setBuddy(self.txtUsername)
        self.lblHost.setBuddy(self.txtHost)
        self.lblPassword.setBuddy(self.txtPassword)

    def languageChange(self):
        self.setCaption(self.tr("Log on to Kura"))
        self.lblDatabase.setText(self.tr("&Database"))
        self.lblUsername.setText(self.tr("&Username"))
        self.lblHost.setText(self.tr("&Host"))
        self.lblPassword.setText(self.tr("&Password"))
        self.buttonOk.setText(self.tr("&OK"))
        self.buttonCancel.setText(self.tr("&Cancel"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = frmLogin()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
