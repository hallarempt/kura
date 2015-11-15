import string, time

from dbobj.dbexceptions import dbRecordNotFoundException
from dbobj.dbobj import dbRecord, dbTable

import docbook;

class lng_lex(dbRecord):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_lex", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_lex", args)

  def __len__(self):
    return len(self.form)

  def __cmp__(self, other):
    if other == None:
      return -1
    if self.form < other.form:
      return -1
    elif self.form == other.form:
      return 0
    else:
      return 1


  def __hash__(self):
    return id(self)


  def getTag(self, tag):
    try:
      tagRecord=self.app.getObject("lng_lex_tag", lexnr=self.lexnr, tag=tag)
    except dbRecordNotFoundException, error:
      tagRecord=error.queryRec
    return tagRecord
      
  def getLink(self):
    return docbook.lexemelink() % (self.lexnr,
                                   docbook.filter(self.form),
                                   docbook.filter(self.glosse))


  def asDocbook(self):
    return docbook.glossentry() % (self.lexnr,
                                   docbook.filter(self.form),
                                   docbook.filter(self.phonetic_form),
                                   docbook.filter(self.glosse),
                                   docbook.filter(self.description),
                                   docbook.filter(self.alternative_form))
class lng_lexemes(dbTable):
  """
    Collection class for all lexeme data.
  """

  def __init__(self, app):
    dbTable.__init__(self, app=app
                         , table="lng_lex"
                         , recObj=lng_lex
                    )

  def select(self, queryRec, orderBy = None):
    dbTable.select(self, queryRec, orderBy = None)
    self.rows.sort()

  def export(self, query, format, *args):
    """
    Returns a unicode object containing the selected data
    in the specified format. Valid formats are:
    * docbook

    XXX: move formats to constants
    """
    doc = []
    if format == "docbook":
      doc.append(docbook.xmlHeader("appendix"))
      doc.append("<appendix><title>Lexicon</title>")
      self.select(query, "order by language, form, glosse")
      languagenr = -1
      section = -1
      for r in self.rows:
        if languagenr != r.languagenr:
          if languagenr != -1:
            doc.append('</glossdiv>')
            doc.append('</glossary>')
            doc.append('</section>')
            section = -1
          doc.append('<section id="lang_%i"><title>%s</title>\n<glossary>' %
                     (r.languagenr, r.language))
          languagenr = r.languagenr
        if section != r.form[:1]:
          if section != -1:
            doc.append('</glossdiv>')
          doc.append('<glossdiv id="lang_%i_%s"><title>%s</title>' %
                     (r.languagenr, r.form[:1], r.form[:1]))
          section = r.form[:1]
        doc.append(r.asDocbook())
      doc.append("</glossdiv>\n</glossary>")
      doc.append("</section>")
      doc.append("</appendix>")
      return u"\n".join(doc)

    else:
      raise NotImplementedError("Export in format %s not yet implemented" % format)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.16 $"""[11:-2]
