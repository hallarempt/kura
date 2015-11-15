from dbobj.dbobj import dbRecord
import docbook

class lng_reference(dbRecord):

    def __init__(self, app, **args):
        if args.has_key("fields"):
            dbRecord.__init__(self, app, "lng_reference", args["fields"])
        else:
            dbRecord.__init__(self, app, "lng_reference", args)



    def __cmp__(self, other):
        if other == None:
            return -1
        if self.author < other.author:
            return -1
        elif self.author == other.author:
            if self.year < other.year:
                return -1
            elif self.year == other.year:
                return 0
            else:
                return 1
        else:
            return 1


    def __hash__(self):
        return id(self)
  

    def getLink(self):
        return docbook.reflink() % (self.abbrev,
                                    docbook.filter(self.author.split(",", 1)[0]),
                                    docbook.filter(self.year))


    def asDocbook(self):
        """
        return a unicode object that contains this record
        in docbook markup
        """
        r = []
        if self.main_categorycode == 'BOOK':
            return docbook.book() % {
                'abbrev' : self.abbrev,
                'referencenr' : self.referencenr,
                'author_surname' : self.author.split(",", 1)[0],
                'author_firstname' : self.author.split(",", 1)[1],
                'title' : self.title,
                'subtitle': '',
                'year': self.year,
                'place': self.place,
                'periodical': self.periodical,
                'publisher': self.publisher
                }
        elif self.main_categorycode == 'PERIOD':
            return docbook.periodical() % {
                'abbrev' : self.abbrev,
                'referencenr' : self.referencenr,
                'author_surname' : self.author.split(",", 1)[0],
                'author_firstname' : self.author.split(",", 1)[1],
                'title' : self.title,
                'subtitle': '',
                'issuenum': self.volume,
                'year': self.year,
                'pages': self.pages,
                'place': self.place,
                'periodical': self.periodical,
                'publisher': self.publisher
                }
        else:
            Return ("<!-- Illegal category for %i, %s, %s -->" % (self.referencenr,
                                                                  self.title,
                                                                  self.author))
        return "\n".join(r)


from dbobj.dbobj import dbTable

class lng_references(dbTable):
    """
      Collection class for all reference data.
    """
    def __init__(self, app):
        dbTable.__init__(self, app, "lng_reference", lng_reference)


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
            doc.append(docbook.xmlHeader("bibliography"))
            doc.append("<bibliography>")
            self.select(query, "order by author, year")
            for r in self.rows:
                doc.append(r.asDocbook())
            doc.append("</bibliography>")
            return "\n".join(doc)

        else:
            raise NotImplementedError("Export in format %s not yet implemented" % format)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.10 $"""[11:-2]
