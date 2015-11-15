#!/usr/bin/python

from qt import *
import sys, os, os.path


from dbobj.dbexceptions import dbRecordNotFoundException

from kurailcanvas import kuraIlCanvas, CanvasException
from kurailcanvasview import kuraIlCanvasView

from kuralib import kuraapp
from kuragui.guiconfig import guiConf

def Icon(pixmap):
    """ Utility function to create an icon from a pixmap."""
    return QIconSet(QPixmap(os.path.join(os.environ["KURADIR"],
                                         "pixmaps", pixmap)))

class KuraEditField(QLineEdit):

    def keyPressEvent(self, e):
        key=e.key()

        if key == Qt.Key_Return:
            self.emit(PYSIGNAL("commit"), ())
        else:
            QLineEdit.keyPressEvent(self, e)


class KuraTextCanvas(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        
        self.text = None
        self.canvas=kuraIlCanvas()
        self.canvasView=kuraIlCanvasView(self.canvas, self)
        self.setMinimumWidth(500)
        self.layout=QVBoxLayout(self)
        
        self.editstriplayout = QHBoxLayout(self.layout)

        self.bnOpen = QToolButton(self)
        self.bnOpen.setIconSet(Icon("cell_edit.png"))
        self.bnOpen.setTextLabel("Open detailed view of current element", 1)
        
        self.bnOK = QToolButton(self)
        self.bnOK.setIconSet(Icon("done.png"))
        self.bnOK.setTextLabel('Commit changes to text', 1)
        
        self.bnDelete = QToolButton(self)
        self.bnDelete.setIconSet(Icon("removecell.png"))
        self.bnDelete.setTextLabel("Remove current selection", 1)
        
        self.bnInsert = QToolButton(self)
        self.bnInsert.setIconSet(Icon("insertcell.png"))
        self.bnInsert.setTextLabel("Insert a new element at the current position", 1)

        self.bnInsertStream = QToolButton(self)
        self.bnInsertStream.setIconSet(Icon("insert_stream.png"))
        self.bnInsertStream.setTextLabel("Insert a new stream at the current position", 1)
       
                                 
        self.bnCancel = QToolButton(self)
        self.bnCancel.setIconSet(Icon("abort.png"))
        self.bnCancel.setTextLabel("Clear changes", 1)
        
        self.editfield = KuraEditField(self)

        self.editstriplayout.addWidget(self.bnInsertStream)
        self.editstriplayout.addWidget(self.bnInsert)
        self.editstriplayout.addWidget(self.bnDelete)
        self.editstriplayout.addWidget(self.bnOpen)

        self.editstriplayout.addWidget(QLabel(" ", self))
        
        self.editstriplayout.addWidget(self.editfield)

        self.editstriplayout.addWidget(self.bnOK)
        self.editstriplayout.addWidget(self.bnCancel)
        
        self.layout.addWidget(self.canvasView)


        self.connect(self.editfield, PYSIGNAL("commit"), self.saveCurrentItem)

        self.connect(self.bnOpen, SIGNAL("clicked()"), self.editCurrentItem)
        self.connect(self.bnInsertStream, SIGNAL("clicked()"),
                     self.insertDefaultStream)
        self.connect(self.bnInsert, SIGNAL("clicked()"),
                     self.insertDefaultElement)
        self.connect(self.bnDelete, SIGNAL("clicked()"),
                     self.deleteCurrentItem)
        self.connect(self.bnOK, SIGNAL("clicked()"),
                     self.saveCurrentItem)
        self.connect(self.bnCancel, SIGNAL("clicked()"),
                     self.restoreCurrentItem)
        
        self.connect(self.canvasView,
                     PYSIGNAL("sigMousePressedOn"),
                     self.editCurrentItem)
        
        self.connect(self.canvasView,
                     PYSIGNAL("sigDoubleClickOn"),
                     self, PYSIGNAL("sigItemOpened"))


                        
                     
                     
    def deleteCurrentItem(self):
        return self.canvas.deleteItem()


    def editCurrentItem(self, item = None):
        if item == None:
            self.currentItem = self.canvas.getCurrentItem()
        else:
            self.currentItem = item
        self.editfield.setText(self.currentItem.text())
        return item


    def saveCurrentItem(self):
        if not self.editfield.text().isEmpty():
            self.currentItem.setText(self.editfield.text())
            self.currentItem = None
            self.editfield.setText(QString())
            self.canvas.update()
            self.canvas.setCursor()
            self.canvasView.setFocus()
        
    def restoreCurrentItem(self):
        self.editfield.setText(QString())
        self.currentItem = None
        self.canvasView.setFocus()

        
    def setTextByNumber(self, textnr):
        """Clear the canvas and set it to a new text.
        """
        self.canvas=kuraIlCanvas()
        try:
            self.text = kuraapp.app.getObject("lng_text", textnr=textnr)
        except dbRecordNotFoundException, errorMessage:
            print "Internal error, record not found:", errorMessage

        self.canvas.setText(self.text)
        self.canvasView.setCanvas(self.canvas)


    def setItemText(self, text):
        """Set the visible text of a certain item to text
        """
        self.currentItem.setText(text)
        self.canvas.update()
        self.canvas.setCursor()
        self.canvasView.setFocus()

    def update(self):
        """Refresh the view
        """
        self.canvas.update()

    def clear(self):
        self.canvas=kuraIlCanvas()
        self.canvasView.setCanvas(self.canvas)

    def previous(self):
        i = self.canvas.previousItem()
        if i != None:
            self.editCurrentItem(i)
        return i

    def next(self):
        i = self.canvas.nextItem()
        if i != None:
            self.editCurrentItem(i)
        return i
    
    def end(self):
        i = self.canvas.lastItem()
        if i != None:
            self.editCurrentItem(i)
        return i

    def up(self):
        i = self.canvas.up()
        if i != None:
            self.editCurrentItem(i)
        return i

    def down(self):
        i = self.canvas.down()
        if i != None:
            self.editCurrentItem(i)
        return i

    def home(self):
        i = self.canvas.firstItem()
        if i != None:
            self.editCurrentItem(i)
        return i

    def delete(self):
        i = self.canvas.deleteItem()
        if i != None:
            self.editCurrentItem(i)
        return i

    def insertDefaultStream(self):
        record = kuraapp.app.createDefaultObject("lng_stream",
                                                 textnr = self.text.textnr,
                                                 text = "#")
        return self.canvas.insertStream(record)

    def insertDefaultElement(self):
        record = kuraapp.app.createDefaultObject("lng_element",
                                                 textnr = self.text.textnr,
                                                 languagenr = self.text.languagenr,
                                                 elementtypecode = "FORM",
                                                 text = "#")
        try:
            return self.canvas.insertElement(record)
        except:
            pass


    def keyPressEvent(self, e):

        key=e.key()
        try:
            if key == Qt.Key_Left:
                i = self.previous()
            elif key == Qt.Key_Right:
                i = self.next()
            elif key == Qt.Key_End:
                i = self.end()
            elif key == Qt.Key_Up:
                i = self.up()
            elif key == Qt.Key_Down:
                i = self.down()
            elif key == Qt.Key_Home:
                i = self.home()
            elif key == Qt.Key_Delete:
                i = self.delete()
            elif key == Qt.Key_Return:
                i = self.editCurrentItem()
                self.editfield.setFocus()
            elif key == Qt.Key_Insert:
                if e.state() == Qt.ControlButton:
                    i = self.insertDefaultStream()
                else:
                    i = self.insertDefaultElement()
            else:
                i = self.canvas.getCurrentItem()
            
            if i is not None:
                self.canvasView.ensureVisible(i)
        except Exception, e:
            QMessageBox.critical(self, "Kura error", str(e))

        
#
# Test code
#

def main():
    kuraapp.initApp(str(guiConf.username),
                  str(guiConf.database),
                  str(guiConf.password),
                  str(guiConf.hostname))
    
    kuraapp.initCurrentEnvironment(guiConf.usernr,
                                 guiConf.languagenr,
                                 guiConf.projectnr)

    app=QApplication(sys.argv)
    view=KuraTextCanvas()
    view.setTextByNumber(1)
    view.show()
    
    app.connect(app, SIGNAL('lastWindowClosed()'), 
                app, SLOT('quit()'))
    app.exec_loop()
    
if __name__=="__main__":
    sys.setappdefaultencoding("utf-8")
    if len(sys.argv)>1:
        if sys.argv[1]=='-p':
            import profile
            profile.run('main()')
    else:
        main()

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.14 $"""[11:-2]
