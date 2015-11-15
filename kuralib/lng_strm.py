from dbobj.dbobj import dbRecord, dbTable
from dbobj.dbexceptions import dbRecordNotFoundException
from dbobj.dbtypes import *

from string import lstrip, rstrip
import re

True = 1
False = 0

try:
  import kuraapp
  from lng_elmt import lng_element, lng_elements
  from lng_sttg import lng_stream_tag
  import docbook
except ImportError:
  import kuralib.kuraapp
  from kuralib.lng_elmt import lng_element, lng_elements
  from kuralib.lng_sttg import lng_stream_tag
  import kuralib.docbook
  
class lng_stream(dbRecord):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_stream", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_stream", args)
    self.tags=[]
    self.elements=[]
    self.parseSets=[]


  def __hash__(self):
    return id(self)

  def __cmp__(self, other):
    if other == None:
      return -1
    if self.seqnr < other.seqnr:
      return -1
    elif self.seqnr == other.seqnr:
      return 0
    else:
      return 1
   
  def translation(self):
    for tag in self.app.getObjects("lng_stream_tag",
                                   streamnr = self.streamnr):
      if tag.tag=="TR" or tag.tag=="TRS" or tag.tag=="TRANS":
        return tag.getDescription()
    return "-"


  def note(self):
    if (self.tags==[] or self.tags==None):
      self.getTags()

    for tag in self.tags:
      if tag.tag=="NOTE":
        return tag.getDescription()
    
  def getTag(self, tag):
    try:
      tagRecord=self.app.getObject("lng_stream_tag",
                                   streamnr=self.streamnr,
                                   tag=tag)
    except dbRecordNotFoundException, error:
      tagRecord=error.queryRec
    return tagRecord
    
  def getTags(self):
    self.tags = self.getChildren("lng_stream_tag")
    return self.tags
     
  def getElements(self, all = False):
    if self.streamnr <> None:
      els = self.app.getObjects("lng_element",
                                 streamnr = self.streamnr)
      if all:
        return els
      result = []
      for el in els:
        if not el.parent_elementnr:
          result.append(el)
      result.sort()
      return result

  def getLink(self):  
     return """<!--@query = kuraapp.app.getObject("lng_stream" , streamnr=%i)
result = query.asDocbook(asExample=1,simple=1) -->""" % self.streamnr

  def asDocbook(self, asExample = False, simple=True):
    """
    Returns a unicode string containing a stream marked up
    as docbook.

    Streams can be used in running text (asExample == false)
    or in example sentences in the body of the grammar (asExample == true).
    
    In the latter case, you need to encase the result in an
    <example><title></title>stream</example> block. There will be a footnote
    that points to the source text for this example.
    """
    if simple == 1:
      return self.simpleDocBook(asExample)
    elif simple == 2:
      return self.fopDocBook()
    else:
      return self.tableDocBook(asExample)

  def __pad(self, s, l):
    if len(s) == l:
      return s
    if len(s) > l:
      raise "Cannot pad %s to length %i" % (s, l)
    return s + (" " * (l - len(s)))

  def getInterlinearLines(self, elements):
    result = []
    l1 = ""
    l2 = ""
    totlen = 0
    for e in elements:
      t = e.text
      g = e.translation()
      l = max(len(t), len(g))
      totlen = totlen + l
      if totlen > 65:
        result.append(l1)
        result.append(l2)
        result.append("")
        l1 = ""
        l2 = ""
        totlen = l
        
      l1 = l1 + self.__pad(t, l + 1)
      l2 = l2 + self.__pad(g, l + 1)
    result.append(l1)
    result.append(l2)
    return "\n".join(result)

  def fopDocBook(self):
    doc = []
    els = self.getElements()
    doc.append("""<informaltable pgwide="0" frame="none"><tgroup cols="1">
    <tbody><row>""")
    s1 = []
    s2 = []
    for el in els:
      s1.append(el.text)
      s2.append(el.translation())
    doc.append("<entry>%s</entry></row><row>" % "\t".join(s1))
    doc.append("<entry>%s</entry>" % "\t".join(s2))
    
    doc.append("</row><row><entry><emphasis>%s</emphasis></entry></row></tbody></tgroup></informaltable>" % docbook.filter(self.translation()))
    return "\n".join(doc)
  
  def simpleDocBook(self, asExample):
    doc = []
    els = self.getElements()
    if asExample:
      doc.append("""<para><programlisting>%s</programlisting>""" % (self.getInterlinearLines(els)))
    else:
      doc.append("""<para id="stream_%i"><programlisting>%s</programlisting>""" % (self.streamnr,
                                                             self.getInterlinearLines(els)))
    note = self.note()     
    if note:
      doc.append(u"%s<footnote><para>%s</para></footnote>" %
                 (docbook.filter(self.translation()), docbook.filter(note)))
    else:
      doc.append(docbook.filter(self.translation()))
    if asExample:
      doc.append("""<footnote><para><link linkend="text_%i">%s, line %i.</link></para></footnote>""" %
                 (self.textnr,
                  self.title,
                  self.seqnr + 1))
    doc.append("</para>")
    return "\n".join(doc)

  def tableDocBook(self, asExample):
    doc = []
    els = self.getElements()
    if not asExample:
      doc.append(u"""<para id="stream_%i"><informaltable colsep="0" frame="none" rowsep="0">""" % self.streamnr)
    else:
      doc.append(u"""<para><informaltable colsep="0" frame="none" rowsep="0">""")
    doc.append(u"""<tgroup align="left" cols="%i">
    <tbody valign="top">""" % len(els))
    doc.append(u"""<row>""")
    w = 0
    for e in els:
      if e.parent_elementnr == 0:
        w = w + len(e)
        if w > 60:
          doc.append("</row><row>")
          w = 0
        doc.append(e.asDocbook())
    note = self.note()
    if note:
      doc.append(u"</row></tbody></tgroup></informaltable>%s<footnote><para>%s</para></footnote>" %
                 (docbook.filter(self.translation()), docbook.filter(note)))
    else:
      doc.append(u"</row></tbody></tgroup></informaltable>%s" % docbook.filter(self.translation()))
    
    if asExample:
      doc.append("""<footnote><para><link linkend="text_%i">%s, line %i.</link></para></footnote>""" %
                 (self.textnr,
                  self.title,
                  self.seqnr + 1))
    doc.append("</para>")
    return u"\n".join(doc)

class lng_streams(dbTable):
  """
    Collection class for all stream data.
  """
  def __init__(self, app):
    dbTable.__init__(self, app, table="lng_stream", recObj=lng_stream)

  def select(self, queryRec, orderBy = None):
    dbTable.select(self, queryRec, orderBy = None)
    self.rows.sort()

  def insert(self, textnr, languagenr, streamTexts=[]):
    seqnr=0
      
    for streamText in streamTexts:
      if streamText <> "":
        stream=lng_stream( self.app
                         , textnr=textnr
                         , languagenr=languagenr
                         , seqnr=seqnr
                         , text=rstrip(lstrip(streamText))
                         , usernr=kuraapp.app.fieldDefaults["usernr"]
                         )
        stream.insert(checkIntegrity=FALSE)
        stream.splitText()
        seqnr=seqnr + 1

  def export(self, query, format, simple = True):
    doc = []
    if format == "docbook":
      doc.append('')
      self.select(query, "order by textnr, seqnr")
      languagenr = -1
      section = -1
      for r in self.rows:
        doc.append(r.asDocbook(True, simple))

      return u"\n".join(doc)
                      
    else:
      raise NotImplementedError("Export in format %s not yet implemented" % format)


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.24 $"""[11:-2]
