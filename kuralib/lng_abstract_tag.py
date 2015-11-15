from dbobj.dbobj import dbRecord

True=1

class AbstractTag(dbRecord):
  tagDefs={}
  tagTypes={}
  tagDomains={}
  tagReferences={}
  
  def __init__(self, app, table, fields={}):
    dbRecord.__init__(self, app, table, fields)

  def __cache(self, cache, key, tableName, **args):
    if cache.has_key(key):
      return cache[key]
    else:
      rec=self.app.getObject(tableName, fields=args)
      cache[key]=rec
      return rec

  def getDescription(self, showifnone=True):
    # caching
    tagDefinition=self.__cache( AbstractTag.tagDefs,
                                self.tag,
                                "lng_tag",
                                tag=self.tag)
    tagType=self.__cache( AbstractTag.tagTypes,
                          tagDefinition.tagtypecode,
                          "lng_tagtypecode"
                        , tagtypecode=tagDefinition.tagtypecode)
               
    if int(tagType.isdomain):
      if self.value==None:
        desc=None
      else:
        tagDomain=self.__cache( AbstractTag.tagDomains,
                                self.value,
                                "lng_tagdomain",
                                tag=self.tag,
                                domainnr=self.value)
        desc=tagDomain.abbreviation
      
    elif int(tagType.isnote):
      desc=self.note
      
    elif int(tagType.isreference):
      if self.value==None:
        desc=None
      else:
        tagReference=self.__cache( AbstractTag.tagReferences,
                                   self.value
                                 , "lng_reference",
                                   referencenr=self.value)
        desc=tagReference.getDescription()
      
    else:
      desc=self.value

    if desc==None:
      if int(showifnone):
        return ("<%s: None>" % self.tag)
      else:
        return ""
    else:
      return desc

  def getNewDescription(self):
    """
    Get a description for a tag if it has some value
    """
    tagDefinition=self.__cache( AbstractTag.tagDefs,
                                self.tag, "lng_tag",
                                tag=self.tag)
    tagType=self.__cache( AbstractTag.tagTypes,
                          tagDefinition.tagtypecode,
                          "lng_tagtypecode",
                          tagtypecode=tagDefinition.tagtypecode)
                        
    if int(tagType.isdomain):
      if self.value=="" or self.value==None:
        return "<None>"
      tagDomain=self.__cache( AbstractTag.tagDomains,
                              self.value, "lng_tagdomain",
                              tag=self.tag,
                              domainnr=self.value)
      return tagDomain.abbreviation
      
    elif int(tagType.isnote):
      if self.note=="" or self.note==None:
        return "<None>"
      return self.note
      
    elif int(tagType.isreference):
      if self.value=="" or self.value==None:
        return "<None>"
      tagReference=self.__cache( AbstractTag.tagReferences,
                                 tag.value,
                                 "lng_reference",
                                 referencenr=tag.value)
      return tagReference.getDescription()
      
    else:
      if self.value=="" or self.value==None:
        return "<None>"
      return self.value

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.3 $
    Last edited          : $Date: 2002/11/16 12:37:03 $
 ***************************************************************************/
"""
