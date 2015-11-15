# Form implementation generated from reading ui file 'frmpreferences.ui'
#
# Created: Mon Dec 23 20:49:56 2002
#      by: The PyQt User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class frmPreferences(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("frmPreferences")

        self.setSizeGripEnabled(0)

        frmPreferencesLayout = QGridLayout(self,1,1,11,6,"frmPreferencesLayout")

        Layout5 = QVBoxLayout(None,0,6,"Layout5")

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout5.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout5.addWidget(self.buttonCancel)
        spacer = QSpacerItem(0,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Layout5.addItem(spacer)

        frmPreferencesLayout.addLayout(Layout5,0,1)

        self.tabPreferences = QTabWidget(self,"tabPreferences")

        self.tab = QWidget(self.tabPreferences,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.lblProject = QLabel(self.tab,"lblProject")
        self.lblProject.setSizePolicy(QSizePolicy(1,1,0,0,self.lblProject.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.lblProject,2,0)

        self.cmbProject = QComboBox(0,self.tab,"cmbProject")
        self.cmbProject.setSizePolicy(QSizePolicy(7,0,0,0,self.cmbProject.sizePolicy().hasHeightForWidth()))

        tabLayout.addMultiCellWidget(self.cmbProject,2,2,1,2)

        self.chkUseDefaultForSearch = QCheckBox(self.tab,"chkUseDefaultForSearch")
        self.chkUseDefaultForSearch.setChecked(0)

        tabLayout.addMultiCellWidget(self.chkUseDefaultForSearch,3,3,0,2)

        self.lblUser = QLabel(self.tab,"lblUser")
        self.lblUser.setSizePolicy(QSizePolicy(1,1,0,0,self.lblUser.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.lblUser,0,0)

        self.lblLanguage = QLabel(self.tab,"lblLanguage")
        self.lblLanguage.setSizePolicy(QSizePolicy(1,1,0,0,self.lblLanguage.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.lblLanguage,1,0)

        self.cmbLanguage = QComboBox(0,self.tab,"cmbLanguage")
        self.cmbLanguage.setSizePolicy(QSizePolicy(7,0,0,0,self.cmbLanguage.sizePolicy().hasHeightForWidth()))

        tabLayout.addMultiCellWidget(self.cmbLanguage,1,1,1,2)

        self.cmbUser = QComboBox(0,self.tab,"cmbUser")
        self.cmbUser.setSizePolicy(QSizePolicy(7,0,0,0,self.cmbUser.sizePolicy().hasHeightForWidth()))

        tabLayout.addMultiCellWidget(self.cmbUser,0,0,1,2)

        self.chkShowValueHint = QCheckBox(self.tab,"chkShowValueHint")

        tabLayout.addMultiCellWidget(self.chkShowValueHint,4,4,0,2)

        self.lblFont = QLabel(self.tab,"lblFont")
        self.lblFont.setFrameShape(QLabel.Panel)
        self.lblFont.setFrameShadow(QLabel.Sunken)

        tabLayout.addWidget(self.lblFont,5,2)

        self.bnFont = QPushButton(self.tab,"bnFont")

        tabLayout.addMultiCellWidget(self.bnFont,5,5,0,1)

        self.bnWidgetFont = QPushButton(self.tab,"bnWidgetFont")

        tabLayout.addMultiCellWidget(self.bnWidgetFont,6,6,0,1)

        self.lblWidgetFont = QLabel(self.tab,"lblWidgetFont")
        self.lblWidgetFont.setFrameShape(QLabel.Panel)
        self.lblWidgetFont.setFrameShadow(QLabel.Sunken)

        tabLayout.addWidget(self.lblWidgetFont,6,2)

        self.rdgDocbookExport = QButtonGroup(self.tab,"rdgDocbookExport")
        self.rdgDocbookExport.setExclusive(1)
        self.rdgDocbookExport.setColumnLayout(0,Qt.Vertical)
        self.rdgDocbookExport.layout().setSpacing(6)
        self.rdgDocbookExport.layout().setMargin(11)
        rdgDocbookExportLayout = QGridLayout(self.rdgDocbookExport.layout())
        rdgDocbookExportLayout.setAlignment(Qt.AlignTop)

        self.rdoComplex = QRadioButton(self.rdgDocbookExport,"rdoComplex")
        self.rdgDocbookExport.insert( self.rdoComplex,1)

        rdgDocbookExportLayout.addWidget(self.rdoComplex,0,0)

        self.rdoSimple = QRadioButton(self.rdgDocbookExport,"rdoSimple")
        self.rdgDocbookExport.insert( self.rdoSimple,0)

        rdgDocbookExportLayout.addWidget(self.rdoSimple,1,0)

        tabLayout.addMultiCellWidget(self.rdgDocbookExport,7,7,0,1)
        self.tabPreferences.insertTab(self.tab,"")

        frmPreferencesLayout.addWidget(self.tabPreferences,0,0)

        self.languageChange()

        self.resize(QSize(530,385).expandedTo(self.minimumSizeHint()))

        self.connect(self.buttonOk,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self,SLOT("reject()"))

        self.setTabOrder(self.cmbUser,self.cmbLanguage)
        self.setTabOrder(self.cmbLanguage,self.cmbProject)
        self.setTabOrder(self.cmbProject,self.chkUseDefaultForSearch)
        self.setTabOrder(self.chkUseDefaultForSearch,self.chkShowValueHint)
        self.setTabOrder(self.chkShowValueHint,self.buttonOk)
        self.setTabOrder(self.buttonOk,self.buttonCancel)
        self.setTabOrder(self.buttonCancel,self.tabPreferences)

        self.lblProject.setBuddy(self.cmbProject)
        self.lblUser.setBuddy(self.cmbUser)
        self.lblLanguage.setBuddy(self.cmbLanguage)

    def languageChange(self):
        self.setCaption(self.tr("Preferences"))
        self.buttonOk.setText(self.tr("&OK"))
        self.buttonCancel.setText(self.tr("&Cancel"))
        self.lblProject.setText(self.tr("Default &Project"))
        self.chkUseDefaultForSearch.setText(self.tr("Use default values in searches."))
        self.lblUser.setText(self.tr("&User"))
        self.lblLanguage.setText(self.tr("Default &Language"))
        self.chkShowValueHint.setText(self.tr("Show existing values for tags (might be slow!)"))
        self.lblFont.setText(QString.null)
        self.bnFont.setText(self.tr("Text &Font"))
        self.bnWidgetFont.setText(self.tr("Application Font"))
        self.lblWidgetFont.setText(QString.null)
        self.rdgDocbookExport.setTitle(self.tr("Docbook interlinear text export"))
        self.rdoComplex.setText(self.tr("Aligned text between <pre> and </pre>"))
        self.rdoSimple.setText(self.tr("In docbook tables"))
        self.tabPreferences.changeTab(self.tab,self.tr("Default values"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = frmPreferences()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
