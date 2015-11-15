import sys
from qt import *

from dbobj.dbexceptions import *

from kuralib import kuraapp
from kuragui.guiconfig import guiConf
from kuragui.comboproxy import ComboProxy
from resource       import True, False
from wiznewtext     import wizNewText

class RegExpParser(QObject):
  def __init__(self, recText
                   , streamRegExp
                   , elementRegExp
                   , morphemeRegExp
                   , lookuplex=False
                   , lookupelmt=False):
                   
    QObject.__init__(self)
    
    self.rawtext=""
    self.recText=recText
    self.streamRegExp=streamRegExp
    self.elementRegExp=elementRegExp
    self.morphemeRegExp=morphemeRegExp
    self.lookuplex=lookuplex
    self.lookupelmt=lookupelmt
    self.text=""

  def lookupElements(self, e):
    e.tags=[]

    if self.lookuplex:
      lexemes=kuraapp.app.getObjects("lng_lex",
                                    languagenr=e.languagenr,
                                    form=e.text)
      if len(lexemes) > 0:
        e.lexnr=lexemes[0].lexnr
        e.lexeme=lexemes[0].getFieldValue("form")

    if self.lookupelmt:
       els=kuraapp.app.getObjects("lng_element",
                                 languagenr=e.languagenr,
                                 text=e.text)
       if len(els) > 0:
         for tag in els[0].getTags():
           e.tags.append(kuraapp.app.createDefaultObject("lng_element_tag",
                                                tag=tag.tag,
                                                value=tag.value,
                                                note=tag.note,
                                                description=tag.description))
  def feed(self, text):
    self.text=self.text + text
    
  def parse(self):
    #
    # FIXME: this should a. be extracted to a generic parser module
    #                    b. the regexpes should come from the element type defs
    #                    c. the element type should not be hardcoded
    #
    # For now, it works, though. Version 1.1, anyone?
    # I dream of pluggable parsers for all kinds of grammars, that produce
    # the requisite DOM of Kura objects. TODO, TODO, immer TODO.
    #
    import re
    streams=re.split(self.streamRegExp, self.text.strip())
    self.emit(PYSIGNAL("sigNumberOfStreams"), (len(streams),))
    for stream in streams:
      stream=stream.strip()
      if stream=="" or stream=="\n":
        continue
        
      s=kuraapp.app.createDefaultObject("lng_stream", text=stream
                                      , seqnr=len(self.recText.streams)
                                      , languagenr=self.recText.languagenr)
      self.recText.streams.append(s)
      s.elements=[]
      
      for element in re.split(self.elementRegExp, s.text):
        element=element.strip()
        if element=="" or element=="\n":
          continue
        e=kuraapp.app.createDefaultObject( "lng_element"
                                        , seqnr=len(s.elements)
                                        , languagenr=self.recText.languagenr
                                        , elementtypecode="FORM")
        s.elements.append(e)
        e.subelements=[]
        e.tags=[]

         
        sub_els=re.split(self.morphemeRegExp, element)
        if len(sub_els) < 2:
          e.text=element
        else:
          e.text=""
          for element in sub_els:
            se=kuraapp.app.createDefaultObject("lng_element", text=element
                                             , languagenr=e.languagenr
                                             , seqnr=len(e.subelements)
                                             , elementtypecode="MORPHEME")
            se.tags=[]
            e.subelements.append(se)
            e.text=e.text + se.text
            self.lookupElements(se)
        #
        # The text of the element has been cleaned of eventual
        # morpheme split markers.
        #
        self.lookupElements(e)
      self.emit(PYSIGNAL("sigStreamDone"), (len(self.recText.streams), ))

class ParseTreeProxy(QObject):
  def __init__(self, lsv):
    self.lsv=lsv
    
  def __mapItem(self, record, item):
    self.item_to_record[item]=record
    self.record_to_item[record]=item
    
  def addTags(self, record, item):
    p=None
    for tag in record.tags:
      if p==None:
        tag_item=QListViewItem(item)
      else:
        tag_item=QListViewItem(item, p)
      p=tag_item
      tag_item.setText(0, tag.tag)
      tag_item.setText(1, tag.getNewDescription())
      self.__mapItem(tag, tag_item)
      
  def refresh(self, recText):
    self.lsv.clear()
    self.item_to_record={}
    self.record_to_item={}
    
    textitem=QListViewItem(self.lsv)
    textitem.setText(0, "TEXT")
    textitem.setText(1, recText.title)
    self.__mapItem(recText, textitem)

    ps=None
    for stream in recText.streams:
      if ps==None:
        stream_item=QListViewItem(textitem)
      else:
        stream_item=QListViewItem(textitem, ps)
      ps=stream_item
      stream_item.setText(0, "STREAM")
      stream_item.setText(1, stream.text)
      self.__mapItem(stream, stream_item)
      pe=None
      
      for element in stream.elements:
        if pe==None:
          element_item=QListViewItem(stream_item)
        else:
          element_item=QListViewItem(stream_item, pe)
        pe=element_item
        element_item.setText(0, element.elementtypecode)
        element_item.setText(1, element.text)
        element_item.setText(2, element.lexeme)
        self.__mapItem(element, element_item)
        self.addTags(element, element_item)
        pss=None
        
        for sub_element in element.subelements:
          if pss==None:
            sub_element_item=QListViewItem(element_item)
          else:
            sub_element_item=QListViewItem(element_item, pss)
          pss=sub_element_item
          sub_element_item.setText(0, sub_element.elementtypecode)
          sub_element_item.setText(1, sub_element.text)
          sub_element_item.setText(2, sub_element.lexeme)
          self.__mapItem(sub_element, sub_element_item)
          self.addTags(sub_element, sub_element_item)
   

class dlgNewText(wizNewText):

  def __init__(self, parent=None):
    wizNewText.__init__(self, parent, name="dlgNewText", modal=True)

    self.txtTitle.setFont(guiConf.widgetfont)
    self.txtDescription.setFont(guiConf.widgetfont)
    self.txtUrl.setFont(guiConf.widgetfont)
    
    self.cmbLanguage.setFont(guiConf.widgetfont)
    self.cmbRecording.setFont(guiConf.widgetfont)
    self.cmbScan.setFont(guiConf.widgetfont)
    
    self.txtStreamRegExp.setFont(guiConf.widgetfont)
    self.txtStreamRegExp.setText(guiConf.streamRegExp)
    
    self.txtElementRegExp.setFont(guiConf.widgetfont)
    self.txtElementRegExp.setText(guiConf.elementRegExp)
    
    self.txtMorphemeRegExp.setFont(guiConf.widgetfont)
    self.txtMorphemeRegExp.setText(guiConf.morphemeRegExp)
    
    self.txtRawText.setFont(guiConf.widgetfont)
    self.lsvParseTree.setFont(guiConf.widgetfont)
    self.lsvParseTree.setSorting(-1, False)
    self.lsvParseTree.setRootIsDecorated(True)
    self.lsvParseTreeProxy=ParseTreeProxy(self.lsvParseTree)
    
    self.lsbProjects.setFont(guiConf.widgetfont)

    self.recText=kuraapp.app.createDefaultObject("lng_text")
    self.recText.streams=[]

    self.cmbLanguageProxy=ComboProxy(self.cmbLanguage,
                                     kuraapp.app.getObjects("lng_language"),
                                     self.recText.languagenr, False)
    self.cmbRecordingProxy=ComboProxy(self.cmbRecording, 
                                      kuraapp.app.getObjects("lng_recording"),
                                      self.recText.recordingnr,  True)
    self.cmbScanProxy=ComboProxy(self.cmbScan,
                                 kuraapp.app.getObjects("lng_scan"),
                                 self.recText.scannr, True)
  
    self.connect(self.bnLoad, SIGNAL("clicked()"), self.slotOpenText)
    

  def accept(self):
    try:
      self.recText.insert()
      textnr=self.recText.textnr
      for project in self.recText.projects:
        p=kuraapp.app.createDefaultObject("lng_proj_text",
                                         projectnr=project.projectnr,
                                         textnr=textnr)
        p.insert()
      for stream in self.recText.streams:
        stream.textnr=textnr
        stream.insert()
        streamnr=stream.streamnr
        for element in stream.elements:
          element.streamnr=stream.streamnr
          element.insert()
          elementnr=element.elementnr
          for tag in element.tags:
            tag.elementnr=elementnr
            tag.insert()
          for sub_element in element.subelements:
            sub_element.parent_elementnr=elementnr
            sub_element.streamnr=streamnr
            sub_element.insert()
            sub_elementnr=sub_element.elementnr
            for tag in element.tags:
              tag.elementnr=sub_elementnr
              tag.insert()
    except dbError, error:
      QMessageBox.information(self, "Error inserting text"
                                  , error.errorMessage
                                  )
    else:
      self.emit(PYSIGNAL("sigAcceptData"),())
      wizNewText.accept(self)
  
  def slotOpenText(self):
    fileName = QFileDialog.getOpenFileName(QString.null, QString.null, self)
    if not fileName.isEmpty():
      text=unicode(open(unicode(fileName)).read())
      self.txtRawText.setText(text)
  
  def next(self):
    currentPage=self.currentPage().name()
    if  currentPage=="pageRecord":
      if (    self.txtTitle.text().isEmpty()
           or self.txtDescription.text().isEmpty()
           or self.cmbLanguageProxy.currentKey == None
          ):
        QMessageBox.warning(self, "Kura", "Please enter at least a title, a language and a description.")
      else:
        self.recText.title=unicode(self.txtTitle.text())
        self.recText.description=unicode(self.txtDescription.text())
        self.recText.url=unicode(self.txtUrl.text())
        self.recText.languagenr=self.cmbLanguageProxy.currentKey()
        self.recText.language=self.cmbLanguageProxy.currentText()
        self.recText.scannr=self.cmbScanProxy.currentKey()
        self.recText.scan=self.cmbScanProxy.currentText()
        self.recText.recordingnr=self.cmbRecordingProxy.currentKey()
        self.recText.recording=self.cmbRecordingProxy.currentText()
        self.recText.transcription_date=unicode(self.txtTranscriptionDate.text())
        
        wizNewText.next(self)
        
    elif currentPage=="pageParsing":
      guiConf.streamRegExp=unicode(self.txtStreamRegExp.text())
      guiConf.elementRegExp=unicode(self.txtElementRegExp.text())
      guiConf.morphemeRegExp=unicode(self.txtMorphemeRegExp.text())
      wizNewText.next(self)      

    elif currentPage=="pageText":
      self.recText.streams=[]
      if self.txtRawText.text().isEmpty():
        # Move forward to projects, we don't have a text.
        self.__fillProject()
        wizNewText.next(self)
        wizNewText.next(self)
      else:
        self.recText.raw_text=unicode(self.txtRawText.text())
        if self.recText.raw_text[:5]=="<?xml":
          self.parseXMLText(self.recText.raw_text)
        else:
          parser=RegExpParser( self.recText
                             , unicode(self.txtStreamRegExp.text())
                             , unicode(self.txtElementRegExp.text())
                             , unicode(self.txtMorphemeRegExp.text())
                             , lookuplex=self.chkLexLookup.isChecked()
                             , lookupelmt=self.chkElmtLookup.isChecked()
                             )
          self.connect(parser, PYSIGNAL("sigNumberOfStreams"), self.progressParsing.setTotalSteps)
          self.connect(parser, PYSIGNAL("sigStreamDone"), self.progressParsing.setProgress)
          parser.feed(unicode(self.txtRawText.text()))
          parser.parse()
          self.recText=parser.recText
          
          # FIXME: once xml parsing works, dedent this.
          self.lsvParseTreeProxy.refresh(self.recText)
          wizNewText.next(self)
        
    elif currentPage=="pageParseTree":
      self.__fillProject()
      wizNewText.next(self)
      
    elif currentPage=="pageProjects":
      self.recText.projects=[]
      for i in range(self.lsbProjects.count()):
        if self.lsbProjects.isSelected(i):
         self.recText.projects.append(self.projects[i])
      wizNewText.next(self)
      self.setFinishEnabled(self.currentPage(), True)


  def __fillProject(self):
    self.projects=[]
    self.lsbProjects.clear()
    for row in kuraapp.app.getObjects("lng_project"):
      self.lsbProjects.insertItem(row.description)
      self.projects.append(row)
        

  
  def back(self):
    wizNewText.back(self)
        
  def help(self): pass

  def parseXMLText(self, text):
    QMessageBox.information(self, "Kura", "Not implemented yet.")
                                                                  
if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = dlgNewText()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.8 $"""[11:-2]
