from lng_abstract_tag import AbstractTag

class lng_lex_tag(AbstractTag):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      AbstractTag.__init__(self, app, "lng_lex_tag", args["fields"])
    else:
      AbstractTag.__init__(self, app, "lng_lex_tag", args)

from dbobj.dbobj import dbTable
   
class lng_lex_tags(dbTable):
  """
    Collection class for all lex_tag data.
  """
  def __init__(self, app):
    dbTable.__init__(self, app, "lng_lex_tag", lng_lex_tag)

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
