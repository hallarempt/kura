import sys

from qt import *

from frmpreferences import frmPreferences

from kuralib import kuraapp

from kuragui.guiconfig import guiConf
from kuragui.comboproxy import ComboProxy

from resource import *

class dlgPreferences(frmPreferences):
    """
    Proxy class for the generated frmPreferences.
    """
    def __init__(self, parent):
        frmPreferences.__init__(self, parent=parent, modal=TRUE)

        self.cmbUserProxy = ComboProxy(self.cmbUser,
                                       kuraapp.app.getObjects("lng_user"),
                                       guiConf.usernr, True)
        self.cmbLanguageProxy = ComboProxy(self.cmbLanguage,
                                           kuraapp.app.getObjects("lng_language"),
                                           guiConf.languagenr, True)
        self.cmbProjectProxy = ComboProxy(self.cmbProject,
                                          kuraapp.app.getObjects("lng_project"),
                                          guiConf.projectnr, True)
        
        self.chkUseDefaultForSearch.setChecked(guiConf.useDefaultForSearch)
        self.chkShowValueHint.setChecked(guiConf.ShowValueHint)
        
        self.lblFont.setText(guiConf.textfontfamily)
        self.lblFont.setFont(QFont(guiConf.textfontfamily, guiConf.textfontsize))
        
        self.lblWidgetFont.setText(guiConf.widgetfontfamily)
        self.lblWidgetFont.setFont(QFont(guiConf.widgetfontfamily,
                                         guiConf.widgetfontsize))

        self.rdgDocbookExport.setButton(guiConf.interlinearstyle)
        
        self.connect(self.bnFont, SIGNAL("clicked()"), self.slotGetFont)
        self.connect(self.bnWidgetFont, SIGNAL("clicked()"), self.slotGetWidgetFont)
    
    def savePreferences(self):    
        try:
            guiConf.usernr = self.cmbUserProxy.currentKey()
        except: pass
        try:
            guiConf.languagenr = self.cmbLanguageProxy.currentKey()
        except: pass
        try:
            guiConf.projectnr=self.cmbProjectProxy.currentKey()
        except: pass
        guiConf.useDefaultForSearch = self.chkUseDefaultForSearch.isChecked()
        guiConf.ShowValueHint = self.chkShowValueHint.isChecked()
        guiConf.interlinearstyle = self.rdgDocbookExport.id(self.rdgDocbookExport.selected())
        kuraapp.app.settings(usernr = guiConf.usernr,
                             languagenr = guiConf.languagenr,
                             projectnr = guiConf.projectnr)
        
     
     
    def slotGetFont(self):
        font, OK = QFontDialog.getFont(guiConf.textfont, self)
        if OK:
            self.lblFont.setText(font.family())
            self.lblFont.setFont(font)
            guiConf.textfontfamily = font.family()
            guiConf.textfontsize = font.pointSize()
            guiConf.textfont = font
     
    def slotGetWidgetFont(self):
        font, OK = QFontDialog.getFont(guiConf.widgetfont, self)
        if OK:
            self.lblWidgetFont.setText(font.family())
            self.lblWidgetFont.setFont(font)
            guiConf.widgetfontfamily = font.family()
            guiConf.widgetfontsize = font.pointSize()
            guiConf.widgetfont = font
            QApplication.setFont(font, TRUE)
            

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.9 $"""[11:-2]
