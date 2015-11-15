from dbobj.dbobj import dbRecord

class lng_user(dbRecord):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_user", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_user", args)


from dbobj.dbobj import dbTable
   
class lng_users(dbTable):
  """
    Collection class for all user data.
  """
  def __init__(self, app):
    dbTable.__init__(self, app, "lng_user", lng_user)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
