#!/usr/bin/env python
""" main.py  -  application starter """
#import pychecker.checker
import sys, os, os.path

from qt import QApplication, SIGNAL, SLOT, QPixmap, QWidget, Qt
from kuragui.guiconfig import guiConf
from kurawindow import KuraWindow

if hasattr(sys, 'setappdefaultencoding'):
    sys.setappdefaultencoding('utf-8')
elif sys.getdefaultencoding() != 'utf-8':
    print 'Warning: encoding not set for unicode - see ReadMe file'

class KuraSplash(QWidget):

    def __init__(self):
        QWidget.__init__(self, None, "splash",
                         Qt.WStyle_NoBorder | Qt.WStyle_Customize | Qt.WDestructiveClose)
        self.pixmap = QPixmap(os.path.join(os.environ['KURADIR'], 'kura.jpg'))
        self.setErasePixmap(self.pixmap)
        self.setGeometry(QApplication.desktop().width() / 2 - self.pixmap.width() / 2,
                    QApplication.desktop().height() / 2 - self.pixmap.height() /2,
                    self.pixmap.width(), self.pixmap.height());

        self.show()

    def mousePressEvent(self, ev):
        self.close()
        
def main():
    app = QApplication(sys.argv)
    QApplication.splash = KuraSplash()
    mainwin = KuraWindow()
    mainwin.resize(guiConf.app_w, guiConf.app_h)
    mainwin.move(guiConf.app_x, guiConf.app_y)
    mainwin.show()
    mainwin.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    app.exec_loop()


if __name__ == "__main__":

    
    if len(sys.argv) > 1:
        if sys.argv[1] == '-p':
            import profile
            profile.run('main()')
    else:
        main()



__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.9 $"""[11:-2]
