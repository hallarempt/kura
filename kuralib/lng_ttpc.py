from dbobj.dbobj import dbRecord

class lng_tagtypecode(dbRecord):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_tagtypecode", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_tagtypecode", args)

      
from dbobj.dbobj import dbTable
   
class lng_tagtypecodes(dbTable):
  """
    Collection class for all tagtypecode data.
  """
  def __init__(self, app):
    dbTable.__init__(self, app, "lng_tagtypecode", lng_tagtypecode)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
