from dbobj.dbobj import dbRecord, dbTable

class lng_tagdomain(dbRecord):

  def __init__( self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_tagdomain", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_tagdomain", args)

  def picklist(self, fieldName):
    """
      Return a list of rows for a certain relation.
    """
    if fieldName=='tag':
      tagRecord=self.app.createObject("lng_tag", fields={})
      return tagRecord.getDomainTags()
    else:
      return dbRecord.picklist(self, fieldName)

class lng_tagdomains(dbTable):
  
  def __init__(self, app):
    dbTable.__init__(self, app, "lng_tagdomain", lng_tagdomain)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.3 $
    Last edited          : $Date: 2002/11/11 18:19:09 $
 ***************************************************************************/
"""
