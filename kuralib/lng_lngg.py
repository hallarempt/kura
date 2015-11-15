from dbobj.dbobj import dbRecord
from string import join

class lng_language(dbRecord):

  def __init__(self, app, **args):
    if args.has_key("fields"):
      dbRecord.__init__(self, app, "lng_language", args["fields"])
    else:
      dbRecord.__init__(self, app, "lng_language", args)

  def getChildLanguages(self):
    """
       Get the entire tree of languages.
    """
    languages=[]
    rows=self.app.getObjects("lng_language", parent_languagenr=self.languagenr)
    languages=rows
    for language in rows:
      children=language.getChildLanguages()
      if children!=None:
        languages=languages + children
    return languages

from dbobj.dbobj import dbTable
   
class lng_languages(dbTable):
  """
    Collection class for all language data.
  """
  def __init__(self, app):
    dbTable.__init__(self, app, "lng_language", lng_language)



__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.3 $
    Last edited          : $Date: 2002/11/16 13:43:59 $
 ***************************************************************************/
"""
