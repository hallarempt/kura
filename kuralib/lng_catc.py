from dbobj.dbobj import dbRecord, dbTable

class lng_categorycode(dbRecord):

  def __init__( self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_categorycode", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_categorycode", args)

class lng_categorycodes(dbTable):
  
  def __init__(self, app):
    dbTable.__init__(self, app, "lng_categorycode", lng_categorycode)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
