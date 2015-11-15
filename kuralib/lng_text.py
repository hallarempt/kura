#!/usr/bin/env python

True = 1
False = 0

try:
    import kuraapp
    from lng_strm import lng_stream, lng_streams
    from lng_txtg import lng_text_tag
    import docbook

except ImportError:
    import kuralib.kuraapp
    from kuralib.lng_strm import lng_stream, lng_streams
    from kuralib.lng_txtg import lng_text_tag
    import kuralib.docbook
  
from dbobj.dbexceptions import dbRecordNotFoundException
from dbobj.dbobj import dbRecord, dbTable
from dbobj.dbtypes import *
import re, string

class lng_text(dbRecord):

    def __init__(self, app, **args):
        if args.has_key("fields"):
            dbRecord.__init__(self, app, "lng_text", args["fields"])
        else:
            dbRecord.__init__(self, app, "lng_text", args)
        self.tags=[]
        self.streams=[]

    def translation(self):
        if self.tags==None:
            self.getTags()
        for tag in self.tags:
            if tag.tagtypecode=="TRNS":
                return tag.getDescription()
        return '-'
      
    def getTags(self):
        self.tags=self.getChildren("lng_text_tag")
        return self.tags
      
    def getTag(self, tag):
        try:
            tagRecord=self.app.getObject("lng_text_tag",
                                         textnr = self.textnr,
                                         tag=tag)
        except dbRecordNotFoundException, error:
            tagRecord=error.queryRec
        return tagRecord

    def removeStreams(self):
        for stream in self.getStreams():
            stream.delete(delChildren=TRUE)

    def getStreams(self):
        self.streams=self.getChildren("lng_stream")
        return self.streams


    def asDocbook(self, simple = True):
        s = [docbook.textHeader(self) % self.getFields()]
        for r in self.getStreams():
            s.append(r.asDocbook(False, simple))
        translation = self.translation()
        if translation != "-":
            s.append("<para>%s</para>") % docbook.filter(translation)
        s.append("</section>")
        return u"\n".join(s)

    def getLink(self):
        return docbook.textlink() % (self.textnr,
                                     docbook.filter(self.title))


class lng_texts(dbTable):
    """
    Collection class for all text data.
    """
    def __init__(self, app):
        dbTable.__init__(self, app, table="lng_text", recObj=lng_text)
        

    def __exportDocbook(self, query, simple):
        doc = []
        self.select(query,
                    "order by language, title, url")
        languagenr = -1
        for r in self.rows:
            if languagenr != r.languagenr:
                if languagenr != -1:
                    doc.append("</section>")
                doc.append("<section><title>%s</title>" % r.language);
                languagenr = r.languagenr
            doc.append(r.asDocbook(simple))
        if len(self.rows) > 0:
            doc.append("</section>")
        else:
            doc.append("<para>No texts.</para>")
        return u"\n".join(doc)

    def export(self, query, format, simple = True):

        if format == "docbook":
            return self.__exportDocbook(query, simple)
        else:
            raise NotImplementedError("Export in format %s not yet implemented" % format)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.9 $"""[11:-2]
