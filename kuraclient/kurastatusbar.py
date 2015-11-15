""" A special-purpose statusbar for Kura """

False = 0
True = 1

import os.path

from qt import QStatusBar, QLabel, QSizePolicy, QFont
from kuragui.guiconfig import guiConf
from kuragui import guiconfig
from kuralib import kuraapp

class KuraPanel(QLabel):

    def __init__(self, *args):
        QLabel.__init__(self, *args)
        
        self.setFrameShape(QLabel.Panel)
        self.setSizePolicy(QSizePolicy(1, 0,
                                       self.sizePolicy().hasHeightForWidth()))
        self.setFont(QFont(guiConf.widgetfontfamily, guiConf.widgetfontsize))

    def setText(self, text):
        QLabel.setText(self, " " + text + " " )


class KuraStatusBar(QStatusBar):

    def __init__(self, *args):
        QStatusBar.__init__(self, *args)
        
        self.lblConnection = KuraPanel(self)
        self.addWidget(self.lblConnection, 0, False)
            
##         self.lblUser=KuraPanel(self)
##         self.addWidget(self.lblUser, 0, False)
        
##         self.lblProject=KuraPanel(self)
##         self.addWidget(self.lblProject, 0, False)
        
##         self.lblLanguage=KuraPanel(self)
##         self.addWidget(self.lblLanguage, 0, False)

        self.reset()

    def reset(self):
        if guiConf.backend == guiconfig.FILE:
            self.lblConnection.setText(os.path.join(guiConf.filepath,
                                              guiConf.datastore))
        else:
            self.lblConnection.setText(guiConf.username + "@" +
                                       guiConf.hostname + ":" +
                                       guiConf.database)
##         self.setUserLabel(guiConf.usernr)
##         self.setProjectLabel(guiConf.projectnr)
##         self.setlanguageLabel(guiConf.languagenr)

    def setUserLabel(self, usernr):
        try:
            r = kuraapp.app.getObject("lng_user", usernr = usernr)
            username = r.getFieldValue("name")
        except:
            username="No current user"
        self.lblUser.setText(username)

    
    def setProjectLabel(self, projectnr):
        try:
            r = kuraapp.app.getObject("lng_project", projectnr = projectnr)
            project = r.getFieldValue("description")
        except:
            project="No current project"
        self.lblProject.setText(project)


    def setlanguageLabel(self, languagenr):
        try:
            language="Language: %s" % \
                      kuraapp.app.getObject("lng_language",
                                         languagenr=languagenr).getFieldValue("language")
        except:
            language="No current language"
        self.lblLanguage.setText(language)


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.4 $"""[11:-2]

