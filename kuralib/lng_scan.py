from dbobj.dbobj import dbRecord

class lng_scan(dbRecord):

    def __init__(self, app, **args):
        if args.has_key("fields"):
            dbRecord.__init__(self, app, "lng_scan", args["fields"])
        else:
            dbRecord.__init__(self, app, "lng_scan", args)

    def asDocbook(self):
        return docbook.scan(self.description) % self.getFields()

from dbobj.dbobj import dbTable
   
class lng_scans(dbTable):
    """
      Collection class for all scan data.
    """
    def __init__(self, app):
        dbTable.__init__(self, app, "lng_scan", lng_scan)

    def export(self, query, format, *args):
        doc = []
        if format == "docbook":
            doc.append('')
            self.select(query,
                        "order by language, title, url")
            languagenr = -1
            for r in self.rows:
                if languagenr != r.languagenr:
                    if languagenr != -1:
                        doc.append("</tbody>\n</tgroup></table>")
                    doc.append(docbook.scanHeader() % r.language);
                    languagenr = r.languagenr
                doc.append(r.asDocbook())
            if len(self.rows) > 0:
                doc.append("</tbody>\n</tgroup></table>")
            else:
                doc.append("<para>No manuscripts scanned</para>")
            return u"\n".join(doc)
        else:
            raise NotImplementedError("Export in format %s not yet implemented" % format)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.5 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
