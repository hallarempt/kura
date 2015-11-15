import sys, string, types, time

from qt import *
from qtcanvas import *
from kuragui.guiconfig import guiConf
from kuralib import kuraapp

True = 1
False = 0

from dbobj.dbexceptions import dbRecordNotFoundException

class CanvasException(Exception):

    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

    def __repr(self):
        return self.error

    def __str(self):
        return self.error
    

class KuraIlItem(QCanvasText):

    def __init__(self, text, canvas):

        if text == None:
            self.__text = "<None>"
        elif type(text) not in [types.StringType, types.UnicodeType]:
            self.__text = str(text)
        else:
            self.__text = text
        QCanvasText.__init__(self, QString(self.__text), canvas)
        self.setFont(canvas.normalfont)

    def move(self, p):
        c = self.canvas()
        r = self.boundingRect()
        x = p.x()
        y = p.y()
        if c.currentLineHeight < r.height():
            c.currentLineHeight = r.height()

        if x + c.lineSpacing + r.width() > c.maxLineWidth:
            x = c.leftMargin
            y = y + c.lineSpacing + c.currentLineHeight
            c.currentLineHeight = r.height()
        
        QCanvasText.move(self, x, y)
        QCanvasText.show(self)

        return QPoint(x + r.width() + c.elementSpacing, y)
    
    def __repr__(self):
        r = self.boundingRect()
        return "%s, x %i, y %i, w %i, h %i (%s)" % \
               (str(self.__class__), r.x(), r.y(), r.width(), r.height(), self.__text)


class KuraIlTagItem(KuraIlItem):
    
    def __init__(self, tag, record, canvas):
        KuraIlItem.__init__(self, record.getTag(tag).getDescription(), canvas)
        self.__tag = tag
        self.__record = record.getTag(tag)

    def setText(self, text):
        self.__record.description = (unicode(text))
        if self.__record.getPrimaryKey() == None:
            self.__record.insert()
        else:
            self.__record.update()
        KuraIlItem.setText(self, text)

    def getRecord(self):
        return self.__record

class KuraIlCanvasTextItem(KuraIlItem):

    def __init__(self, text, canvas):
        KuraIlItem.__init__(self, text, canvas)

    
class KuraIlCanvasTextTagItem(KuraIlTagItem):
    pass

class KuraIlCanvasTextTitleItem(KuraIlCanvasTextItem):
    
    def __init__(self, record, canvas):
        KuraIlCanvasTextItem.__init__(self, record.title, canvas)
        self.__record = record
        self.setFont(self.canvas().titlefont)

    def setText(self, text):
        self.__record.title = unicode(text)
        if self.__record.getPrimaryKey() == None:
            self.__record.insert()
        else:
            self.__record.update()

        KuraIlCanvasTextItem.setText(self, text)

    def getRecord(self):
        return self.__record
    
    def move(self, p):
        QCanvasText.move(self, p.x(), p.y())
        QCanvasText.show(self)
        r = self.boundingRect()
        return QPoint(self.canvas().leftMargin,
                      r.height() + self.canvas().lineSpacing)


class KuraIlCanvasTextDescriptionItem(KuraIlCanvasTextItem):
    
    def __init__(self, record, canvas):
        KuraIlCanvasTextItem.__init__(self, record.description, canvas)
        self.__record = record

    def getRecord(self):
        return self.__record

    def setText(self, text):
        self.__record.description = unicode(text)
        if self.__record.getPrimaryKey() == None:
            self.__record.insert()
        else:
            self.__record.update()

        KuraIlCanvasTextItem.setText(self, text)
        
    def move(self, p):
        x = p.x()
        y = p.y()
        r = self.boundingRect()
        c = self.canvas()
        
        QCanvasText.move(self, c.leftMargin, y)
        QCanvasText.show(self)

        return QPoint(c.leftMargin,
                      y + r.height() + c.lineSpacing)


class KuraIlCanvasStreamItem(KuraIlItem):
    
    def __init__(self, record, canvas):
        KuraIlItem.__init__(self, record.seqnr, canvas)
        self.__record = record
        self.setFont(canvas.boldfont)

    def setText(self, text):
        try:
            i = int(str(text))
        except:
            print "Could not convert %s to int" % unicode(text)
            return
        KuraIlItem.setText(self, str(i))
        self.__record.seqnr = i
        if self.__record.getPrimaryKey() == None:
            self.__record.insert()
        else:
            self.__record.update()



    def getRecord(self):
        return self.__record


    def move(self, p):
        c = self.canvas()
        
        x = 10
        y = p.y() + c.lineSpacing + c.currentLineHeight
        c.currentLineHeight = 0
        
        QCanvasText.move(self, x, y)
        QCanvasText.show(self)

        return QPoint(c.leftMargin, y)
    

class KuraIlCanvasStreamTagItem(KuraIlTagItem):

    def __init__(self, tag, record, canvas):
        KuraIlTagItem.__init__(self, tag, record, canvas)
        self.setFont(canvas.italicfont)
        self.__record = record

    def move(self, p):
       
        c = self.canvas()

        x = c.leftMargin + c.elementSpacing

        y = p.y() + c.currentLineHeight + c.lineSpacing

        
        c.currentLineHeight = 0
        
        QCanvasText.move(self, x, y)
        QCanvasText.show(self)

        return QPoint(c.leftMargin, y + c.lineSpacing)



class KuraIlCanvasElementItem(KuraIlItem):
    
    def __init__(self, record, canvas):
        KuraIlItem.__init__(self, record.text
                             + "\n"
                             + record.translation(),
                             canvas)
        self.__record = record
    
    def setText(self, text):
        
        text = unicode(text)
        
        if text.find("\n") > 0:
            t = unicode(text).split("\n")
        elif text.find(" ") > 0:
            t = unicode(text).split(" ")
        else:
            t = [text]
            
        if len(t) > 1:
            text, tag = (t[0],  " ".join(t[1:]))
        else:
            text, tag = (text, None)

        self.__record.text = unicode(t[0])
        
        if self.__record.getPrimaryKey() == None:
            self.__record.insert()
        else:
            self.__record.update()
       
        if tag:
            self.__record.setGlosse(tag)
        else:
            tag = self.__record.translation(False)
                
        KuraIlItem.setText(self, text + "\n" + tag)
        
       
    def getRecord(self):
        return self.__record


class KuraIlCanvasElementTagItem(KuraIlTagItem):
    pass


class kuraIlCanvas(QCanvas):

    def __init__(self, parent=0, name=0 ):
        QCanvas.__init__(self, parent, name)

        self.cursor = QCanvasRectangle(self)
        self.scol = QCanvasLine(self)
        self.items = []
        self.currentItem = -1

        self.lineHeight=QFontMetrics(guiConf.textfont).height()
        self.lineSpacing=QFontMetrics(QFont(guiConf.textfont)).lineSpacing() + 5
        self.lineSetSpacing = 5
        self.elementSpacing = 8

        self.leftMargin = 50
        self.rightMargin = 20
        self.topMargin = 10
        self.maxLineWidth = 500
        
        self.normalfont = QFont(guiConf.textfont.family(),
                                guiConf.textfont.pointSize(),
                                QFont.Normal, False)
        self.italicfont = QFont(guiConf.textfont.family(),
                                guiConf.textfont.pointSize(),
                                QFont.Normal, False)
        self.boldfont = QFont(guiConf.textfont.family(),
                              guiConf.textfont.pointSize(),
                              QFont.Bold, False)
        self.bolditalicfont = QFont(guiConf.textfont.family(),
                                    guiConf.textfont.pointSize(),
                                    QFont.Bold, False)
        self.titlefont = QFont(guiConf.textfont.family(),
                             guiConf.textfont.pointSize() * 2,
                             QFont.Bold, False)
        


    def redisplay(self, start = 0):
        self.currentLineHeight = 0
        if type(start) != types.IntType:
            try:
                start = self.items.index(start)
            except ValueError:
                print "ValueError:", start, "not in items"
                start = 0
        if start == 0:
            p = QPoint(self.leftMargin, self.topMargin)
        else:
            p = previousItem.boundingRect().bottomRight()

        for item in self.items[start:]:
            p = item.move(p)
            
        y = self.items[-1].y() + self.currentLineHeight + self.lineSpacing
        self.scol.setPoints(self.leftMargin - 5, 0,
                            self.leftMargin - 5, y)
        self.scol.show()


    def handleStream(self, stream):
        item = KuraIlCanvasStreamItem(stream, self)
        self.items.append(item)

        for element in stream.getElements():
            self.items.append(KuraIlCanvasElementItem(element, self))

        item = KuraIlCanvasStreamTagItem("TR", stream, self)
        self.items.append(item)


    def handleText(self, text):
        # Title object
        item = KuraIlCanvasTextTitleItem(text, self)
        self.items.append(item)

        item = KuraIlCanvasTextDescriptionItem(text, self)
        self.items.append(item)

        for stream in text.getStreams():
            self.handleStream(stream)


    def setText(self, lngText):

        self.lngText = lngText
        self.handleText(lngText)
        self.redisplay(0)
        y = self.items[-1].y() + self.currentLineHeight + self.lineSpacing

        self.resize(self.maxLineWidth + self.leftMargin + self.rightMargin,
                    y + 400)
        


        self.currentItem = 0
        self.setCursor()
        self.update()


    def setCursor(self, pos = None):
        if pos == None:
            try:
                i = self.items[self.currentItem]
            except IndexError:
                return
        else:
            try:
                i = self.collisions(pos)[0]
                if i not in self.items:
                    raise IndexError, "Wrong one"
                self.currentItem = self.items.index(i)
            except IndexError, e:
                try:
                    return self.items[self.currentItem]
                except:
                    return
        
        r = i.boundingRect()
        self.cursor.move(r.x() -2, r.y() -2)
        self.cursor.setSize(r.width() + 4,
                            r.height() + 4)
        self.cursor.setZ(-1.0)
        self.cursor.setPen(QPen(QColor(Qt.gray), 2, Qt.DashLine))
        self.cursor.show()
        self.update()

        return i

    def getCurrentItem(self):
        if len(self.items) < 1:
            return None
        else:
            if self.currentItem < 0:
                return self.items[0]
            elif self.currentItem > len(self.items) - 1:
                return self.items[-1]
            else:
                return self.items[self.currentItem]

    def nextItem(self):
        self.currentItem += 1
        if self.currentItem >= len(self.items):
            self.currentItem = len(self.items)
        self.setCursor()
        return self.getCurrentItem()

    def previousItem(self):
        self.currentItem -= 1
        if self.currentItem < 0:
            self.currentItem = 0
        self.setCursor()
        return self.getCurrentItem()

    def firstItem(self):
        self.currentItem = 0
        self.setCursor()
        return self.getCurrentItem()


    def lastItem(self):
        self.currentItem = len(self.items) - 1
        self.setCursor()
        return self.getCurrentItem()


    def deleteItem(self):
        if  self.currentItem > -1 and self.currentItem < len(self.items):
            item = self.getCurrentItem()
            item.setCanvas(None)
            r = item.getRecord()
            if r.getPrimaryKey() != None:
                r.delete(True)
            del self.items[self.currentItem]
            self.redisplay(0)
            self.setCursor()
            return item
        else:
            return self.getCurrentItem()


    def setItemText(self, item, text):
        item.setText(text)
        
    
    def up(self):
        y = self.getCurrentItem().y()
        i = self.currentItem
        while i > 0:
            i -= 1
            if self.items[i].y() != y:
                break
        self.currentItem = i
        self.setCursor()
        return self.getCurrentItem()


    def down(self):
        y = self.getCurrentItem().y()
        i = self.currentItem
        while i < len(self.items) - 1:
            i += 1
            if self.items[i].y() != y:
                break
        self.currentItem = i
        self.setCursor()
        return self.getCurrentItem()


    def insertItem(self, item):
        if self.currentItem == len(self.items) - 1:
            self.items.append(item)
        else:
            self.items.insert(self.currentItem + 1, item)
        self.currentItem = self.currentItem + 1
        self.renumber()
        self.redisplay(0)
        self.setCursor()


    def renumber(self):
        strm_pknr = -1
        strm_seqnr = 0
        elmt_seqnr = 0
        for i in self.items:
            if i.__class__ == KuraIlCanvasStreamItem:
                i.setText(str(strm_seqnr))
                r = i.getRecord()
                r.seqnr = strm_seqnr
                r.textnr = self.lngText.textnr
                if r.getPrimaryKey() == None:
                    r.insert()
                strm_pknr = r.getPrimaryKey()
                strm_seqnr += 1
                elmt_seqnr = 0
            elif i.__class__ == KuraIlCanvasElementItem:
                r = i.getRecord()
                r.seqnr = elmt_seqnr
                r.textnr = self.lngText.textnr
                r.streamnr = strm_pknr
                if r.getPrimaryKey() == None:
                    r.insert()
                elmt_seqnr += 1
            
        
    def insertElement(self, record):
        if not self.items[self.currentItem].__class__ == KuraIlCanvasElementItem:
            i = self.currentItem            
            while i >= 0:
                if self.items[i].__class__ == KuraIlCanvasStreamItem:
                    break
                if self.items[i].__class__ == KuraIlCanvasStreamTagItem:
                    i = -1
                    break
                i -= 1
            if i == -1:
                raise CanvasException("NoStreamDefinedError")
        
        item = KuraIlCanvasElementItem(record, self)
        self.insertItem(item)
        return item


    def insertStream(self, record):
        item = KuraIlCanvasStreamItem(record, self)
        self.insertItem(item)
        return item

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.21 $"""[11:-2]
