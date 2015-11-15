from dbobj.dbobj import dbRecord
import docbook

class lng_recording(dbRecord):

    def __init__(self, app, **args):
        if args.has_key("fields"):
            dbRecord.__init__(self, app, "lng_recording", args["fields"])
        else:
            dbRecord.__init__(self, app, "lng_recording", args)

    def asDocbook(self):
        return docbook.recording(self.description) % self.getFields()
    
from dbobj.dbobj import dbTable
   
class lng_recordings(dbTable):
    """
      Collection class for all recording data.
    """
    def __init__(self, app):
        dbTable.__init__(self, app, "lng_recording", lng_recording)

    def export(self, query, format, *arg):
        doc = []
        if format == "docbook":
            doc.append('')
            self.select(query,
                        "order by language, title, url")
            languagenr = -1
            for r in self.rows:
                if languagenr != r.languagenr:
                    if languagenr != -1:
                        doc.append("</tbody></tgroup></table>")
                    doc.append(docbook.recordingHeader() % r.language);
                    languagenr = r.languagenr
                doc.append(r.asDocbook())
            if len(self.rows) > 0:
                doc.append("</tbody>\n</tgroup>\n</table>")
            else:
                doc.append("<para>No recordings.</para>")
            return u"\n".join(doc)
        
        else:
            raise NotImplementedError("Export in format %s not yet implemented" % format)


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.7 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
