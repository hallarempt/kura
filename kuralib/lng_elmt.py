from dbobj.dbobj import dbRecord, dbTable
from dbobj.dbexceptions import *
from dbobj.dbtypes import *
from string import rstrip, lstrip, join

from lng_lex import lng_lex, lng_lexemes
from lng_eltg import lng_element_tag
import docbook
import kuraapp

True = 1
False = 0

class lng_element(dbRecord):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_element", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_element", args)
    self.elements=[]
    self.tags=[]
    self.__cachedTranslation = ""

  def __len__(self):
    return max(len(self.text), len(self.translation()))

  def __cmp__(self, other):
    if other == None:
      return -1
    if self.seqnr < other.seqnr:
      return -1
    elif self.seqnr == other.seqnr:
      return 0
    else:
      return 1


  def __hash__(self):
    return id(self)
  
  def getTags(self):
    self.tags=self.getChildren("lng_element_tag")
    return self.tags

  def getElements(self):
    self.elements=self.getChildren("lng_element")
    return self.elements

  def buildElementTree(self):
    self.getTags()
    for element in self.getElements():
      element.buildElementTree()
   
  def translation(self, cache = True):
    
    if cache and self.__cachedTranslation != "":
      return self.__cachedTranslation

    if (self.tags==[] or self.tags==None):
      self.getTags()

    for tag in self.tags:
      if tag.tag=="TR" or tag.tag=="GL" or tag.tag == "ABBR":
        d = tag.getDescription()
        self.__cachedTranslation = d
        return d

    if self.lexeme <> "" and self.lexeme <> None:
      self.__cachedTranslation = self.lexeme
      return self.lexeme
    else:
      try:
        lexeme = self.app.getObject("lng_lex",
                                    form=self.text.lower(),
                                    languagenr=self.languagenr)
        self.__cachedTranslation = lexeme.glosse
        return lexeme.glosse
      except Exception, e:
        if cache:
          self.__cachedTranslation = "#"

        return "#"

  def note(self):
    if (self.tags==[] or self.tags==None):
      self.getTags()

    for tag in self.tags:
      if tag.tag=="NOTE":
        return tag.getDescription()
    
  def getGlosse(self):
    try:
      glosse = kuraapp.app.getObject("lng_element_tag",
                                     elementnr=self.elementnr,
                                     tag="GL")
      return glosse.value
    except:
      return None


  def setGlosse(self, text):
    try:
      glosse = kuraapp.app.getObject("lng_element_tag",
                                     elementnr = self.elementnr,
                                     tag="GL")
      glosse.value = text
      glosse.description = text
      glosse.update()
    except:
      glosse = kuraapp.app.createDefaultObject("lng_element_tag",
                                               elementnr = self.elementnr,
                                               tag = "GL",
                                               value = text)
      glosse.insert()
      
  def getPhoneticTranscription(self):
    try:
      phonetic_transcription=kuraapp.app.getObject("lng_element_tag", elementnr=self.elementnr
                                                                   , tag="PHON"
                                                                   )
      return phonetic_transcription.value
    except dbRecordNotFoundException, error:
      print "No phonetic transcription"
    except dbTooManyRowsException, error:
      print "Too many phonetic transctions"
    return None

          
  def getTag(self, tag):
    try:
      tagRecord=self.app.getObject("lng_element_tag", elementnr=self.elementnr, tag=tag)
    except dbRecordNotFoundException, error:
      tagRecord=error.queryRec
    return tagRecord


  def elmtLength(self):
    return max( len(self.text), len(self.translation()) )

  def asDocbook(self):
    note = self.note()
    translation = self.translation()
    s = docbook.element(self.lexnr, note) % {"elementnr" : self.elementnr,
                                             "lexnr" : self.lexnr,
                                             "text" : self.text,
                                             "glosse": translation,
                                             "note" : docbook.filter(note)}
    return s
  
  def type(self):
    type=kuraapp.app.getObject("lng_elementtypecode", elementtypecode=self.elementtypecode)
    return type
    
class lng_elements(dbTable):
  """
    Collection class for all element data.
  """
  def __init__(self, app):
    dbTable.__init__(self, app, table="lng_element", recObj=lng_element)

  def select(self, queryRec, orderBy = None):
    dbTable.select(self, queryRec, orderBy = None)
    self.rows.sort()

  def insert(self, streamnr, languagenr, elementTexts=[]):
    seqnr=0
      
    for elementText in elementTexts:
      if elementText <> "":
        element=lng_element( self.app
                           , streamnr=streamnr
                           , seqnr=seqnr
                           , text=rstrip(lstrip(elementText))
                           , usernr=kuraapp.app.fieldDefaults["usernr"]
                           , languagenr=languagenr
                           )
        element.insert(checkIntegrity=FALSE)
        seqnr=seqnr + 1


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.17 $
    Last edited          : $Date: 2002/11/12 22:12:47 $

 ***************************************************************************/
"""
