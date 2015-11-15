# Form implementation generated from reading ui file 'frmlogin.ui'
#
# Created: Mon Nov 13 22:02:43 2000
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


from qt import *


class Login(QDialog):
    
    def __init__(self, parent = None, name = None, modal = 0, fl = 0):
        QDialog.__init__(self, parent, name, modal, fl)

        if name == None:
            self.setName('frmLogin')

        self.resize(418,182)
        self.setCaption(self.tr('Log on to Kura'))
        self.setSizeGripEnabled(0)
        self.setSizePolicy(QSizePolicy(1,1,self.sizePolicy().hasHeightForWidth()))
        frmLoginLayout = QVBoxLayout(self)
        frmLoginLayout.setSpacing(6)
        frmLoginLayout.setMargin(11)

        Layout6 = QGridLayout()
        Layout6.setSpacing(6)
        Layout6.setMargin(0)

        self.txtUsername = QLineEdit(self,'txtUsername')

        Layout6.addWidget(self.txtUsername,0,1)

        self.lblDatabase = QLabel(self,'lblDatabase')
        self.lblDatabase.setText(self.tr('&Database'))

        Layout6.addWidget(self.lblDatabase,2,0)

        self.lblUsername = QLabel(self,'lblUsername')
        self.lblUsername.setText(self.tr('&Username'))

        Layout6.addWidget(self.lblUsername,0,0)

        self.txtHost = QLineEdit(self,'txtHost')

        Layout6.addWidget(self.txtHost,3,1)

        self.txtPassword = QLineEdit(self,'txtPassword')

        Layout6.addWidget(self.txtPassword,1,1)

        self.lblHost = QLabel(self,'lblHost')
        self.lblHost.setText(self.tr('&Host'))

        Layout6.addWidget(self.lblHost,3,0)

        self.txtDatabase = QLineEdit(self,'txtDatabase')

        Layout6.addWidget(self.txtDatabase,2,1)

        self.lblPassword = QLabel(self,'lblPassword')
        self.lblPassword.setText(self.tr('&Password'))

        Layout6.addWidget(self.lblPassword,1,0)
        frmLoginLayout.addLayout(Layout6)

        Layout1 = QHBoxLayout()
        Layout1.setSpacing(6)
        Layout1.setMargin(0)
        spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(spacer)

        self.buttonOk = QPushButton(self,'buttonOk')
        self.buttonOk.setText(self.tr('&OK'))
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,'buttonCancel')
        self.buttonCancel.setText(self.tr('&Cancel'))
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)
        frmLoginLayout.addLayout(Layout1)

        self.connect(self.buttonOk,SIGNAL('clicked()'),self,SLOT('accept()'))
        self.connect(self.buttonCancel,SIGNAL('clicked()'),self,SLOT('reject()'))

        self.setTabOrder(self.txtUsername,self.txtPassword)
        self.setTabOrder(self.txtPassword,self.txtDatabase)
        self.setTabOrder(self.txtDatabase,self.txtHost)
        self.setTabOrder(self.txtHost,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)

        self.lblDatabase.setBuddy(self.txtDatabase)
        self.lblUsername.setBuddy(self.txtUsername)
        self.lblHost.setBuddy(self.txtHost)
        self.lblPassword.setBuddy(self.txtPassword)
