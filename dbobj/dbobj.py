"""

 Data-object base classes

  dbError:   fieldname+ error description
  dbRecord:  columns + values: offers insert, update, delete.
             Provides generic data validation.
  dbTable:   collection of dbRecords: offers select (based on a 
             dbRecord).

"""

import sys, string

from dbtypes import *
from dbexceptions import dbError

class dbRecord:
  """
    Object containing the values of a row in the database.
    Can insert, update and delete itself. Can be used as a
    search template for the dbTable class.

    Args:
      db     = database connection
      table  = table name
      fields = dictionary of name, value pairs
  """
  def __init__(self, app, table, fields={}):
    self.table=table
    self.app=app
    self.sql=self.app.sql
    self.tableDef=self.app.tables[table]
    self.errFields=[]
    self.fieldOrder=self.tableDef.fieldOrder

    for field in self.tableDef.fieldOrder:
        setattr(self,
                field,
                self.__convertFieldValue(field, fields.get(field)))



  def __convertFieldValue(self, field, value):
    if value==None:
      return None
    if (    self.tableDef.fields[field].datatype==INTEGER 
         or self.tableDef.fields[field].datatype == BOOLEAN
       ):
      try:
        return int(value)
      except TypeError:
        return value
      except ValueError:
        return value
    else:
      try:
        return unicode(value, "utf8") 
      except UnicodeError:
        #
        # This value probably contains latin1 characters - these are
        # automatically converted to Unicode. If the user messes with
        # this record and saves it,
        # it's upgraded to Unicode.
        sys.stderr.write( "UnicodeError with value %s for field %s will be automatically converted to Unicode.\n" % (value, field))
        return unicode(value, "latin-1")
      except TypeError:
        return value

  

  def __iter__(self):
    self.current = -1
    return self


  def updateUser(self):
    if self.tableDef.fields.has_key("usernr"):
      self.usernr = self.app.fieldDefaults["usernr"]
      rows = self.app.getObjects("lng_user",
                                 fields = {"usernr": self.usernr})
      self.user = rows[0].name


  def next(self):
    """ the next fielddef/field value tuple of this record, following
    the table definition field order."""
    self.current += 1
    if self.current >= len(self.fieldOrder):
      raise StopIteration
    else:
      return (self.tableDef.fields[self.fieldOrder[self.current]],
              self[self.fieldOrder[self.current]])


  def __getitem__(self, key):
    return self.getFieldValue(key)


  def __repr__(self):
    return repr(self.getFields())


  def __checkNull(self):
    """
      Check whether all not-null fields are filled.
    """
    for (fieldname, field) in self.tableDef.fields.items():
      if not field.nullable and not field.autoincrement:
        if getattr(self, fieldname) == None:
          self.errFields.append("Field " + fieldname + " must be entered")

    
  def __checkParents(self):
    """
      Referential integrity check for parents
    """
    for lookuptable in self.tableDef.lookuptables:
      relation=self.app.relations[lookuptable]
      key=relation.keys
      keyval=self.getFieldValue(key.local)
      if keyval <> None and keyval <> 0 and keyval <> "":
        if self.app.getObjects(relation.rtable, fields={key.foreign:keyval})==[]:
          self.errFields.append(relation.name + " does not exist")


  def __checkLength(self):
    """
      Check if there are fields with values that are
      too long.
    """
    for (fieldname, fieldDef) in self.tableDef.fields.items():
      if fieldDef.owner:

        val = getattr(self, fieldname)
        if val != None:
          if fieldDef.datatype==VARCHAR:
            try:
              val = unicode(val)
            except:
              continue
            if len(val) > fieldDef.length:
              self.errFields.append(dbError( "Value [%s]for field %s too long, max %s." 
                                              % (val, fieldname, fieldDef.length)
                                            )
                                   )
    
  def __verify(self):
    """
      Verify whether the record is OK for the database
    """
    self.errFields=[]
    self.__checkNull()
    self.__checkLength()
    self.__checkParents()
    if len(self.errFields) == 0:
      return TRUE
    else:
      return FALSE


  def insert(self, checkIntegrity=TRUE):
    """
      Add the record to the database
    """
    if checkIntegrity:
      if  self.__verify() :
        return self.sql.insert(self.table, self)
      else:
        raise dbError("Error inserting into " + self.app.getTableLable(self.table)
                      + "\n" + string.join(self.errFields,"\n"))
    else:
      return self.sql.insert(self.table, self)

      
  def __deleteOK(self):
    """
      Check whether the current record has children before deleting it
    """
    for childDef in self.tableDef.childtables.values():
      if self.hasChildren(childDef.childTable):
        return FALSE
      else:
        return TRUE
    return TRUE


  def deleteChildren(self, childtable):
    childRows=self.getChildren(childtable)
    if len(childRows) > 0:
      for child in childRows:
        child.delete(delChildren=TRUE)


  def delete(self, delChildren=FALSE):
    """
      Delete the current record from the database.
      
      If delChildren , records in all child tables
      will be deleted too, else, if there are child records,
      the record won't be deleted.
    """
    if delChildren:
      for childtable in self.tableDef.childtables.keys():
        self.deleteChildren(childtable)
    if self.__deleteOK():
      self.sql.delete(self.table, self)
    else:
      raise dbError("Can't delete %s from %s: child records found." %
                    (self.getPrimaryKey(), self.app.getTableLable(self.table)))

    
  def update(self):
    """
      Verify the record and if OK, update it in the database
    """

    if self.__verify():
      self.sql.update(table=self.table, queryRec=self)
    else:
      raise dbError("Can't update record in table %s: errors: %s." 
                      % (self.app.getTableLable(self.table), unicode(self.errFields))
                   )
    
    
  def getChildren(self, childtable, orderBy = None):
    """
      Return child records of this table.
    """
    pk=self.getPrimaryKey()
    if (pk==None or pk==0 or pk==""): 
      return []
    else:
      childdef=self.tableDef.getChildDef(childtable)
      return self.app.getObjects(childtable,
                                 fields={childdef.keys.foreign:pk},
                                 orderBy = orderBy)


  def hasChildren(self, childTable):
    children=self.getChildren(childTable)
    if len(children)>0: 
      return TRUE
    else:
      return FALSE


  def createChild(self, childtable, relation):
    """
    Complicated...
    
    master table a (pkA=1, fld='yyy' ....)
    detail table b (pkB= , fk=, fldA=, ...)
    
    relation: b_a (keys=[dbPair(local=pkB, foreign=pkA)]
                  ,descriptors=[dbPair(local='fldA', foreign=fld)]
                  ,rtable=a 
                  ,ralias... 
                  ) 
                  
                  We try to construct a record of table b, knowing only the tablename
                  and the right relation """
    
    masterkey=self.getPrimaryKey()
    if masterkey==None:
      raise dbError("Error: No primary key yet. Can't create child record.")
    rec=self.app.createObject(childtable, fields={relation.keys.local: masterkey})
    return rec

  
  def picklist(self, fieldName):
    """
      Return a list of rows for a certain relation.
    """

    relationDef=self.tableDef.fields[fieldName].relation
    if relationDef <> None:
      lookupDef=self.app.relations[relationDef]
      return self.app.getObjects(lookupDef.rtable)
    else:
      return [] # not a foreign key


  def getFields(self):
    """
      Return a dictionary of field-value pairs. 
    """
    fields={}
    for field in self.fieldOrder:
      fields[field]=getattr(self, field)
    return fields


  def getOwnerFields(self):
    """
      Return a dictionary of field-value pairs
      for the fields this record is the owner of.
    """
    fields={}
    for field in self.fieldOrder:
      if self.tableDef.fields[field].owner:
        fields[field] = getattr(self, field)
    return fields
        
  def getFieldValue(self, field):
    """
      return the value of a field in the record.
    """
    value = getattr(self, field)

    if value==None:
      return None
    if (    self.tableDef.fields[field].datatype==INTEGER 
         or self.tableDef.fields[field].datatype == BOOLEAN
       ):
      try:
        return int(value)
      except TypeError:
        sys.stderr.write("Value should be integer: " + value)
        return value
      except ValueError:
        return value
    else:
      try:
        
        return unicode(value, "utf8") 
      except UnicodeError:
        #
        # This value probably contains latin1 characters - these are
        # automatically converted to Unicode. If the user messes with
        # this record and saves it,
        # it's upgraded to Unicode.
        sys.stderr.write( "UnicodeError with value %s for field %s will be automatically converted to Unicode.\n" % (value, field))
        return unicode(value, "latin-1")
      except TypeError:
        return value

      
  def getFieldValueAsString(self, field):
    value=getattr(self, field)  
    if value==None:
      return "#"
    try:
      return unicode(value)
    except:
      return unicode(value, "latin-1")


  def getFieldDefinition(self, fieldName):
    """
       Returns the field definition as stored
       in the repository.
    """
    return self.tableDef.fields[fieldName]

    
  def setFieldValue(self, field, value):
    setattr(self, field, value)


  def getPrimaryKey(self):
    return self.getFieldValue(self.tableDef.primarykey)

  def setPrimaryKey(self, pk):
    self.setFieldValue(self.tableDef.primarykey, pk)



  def getDescriptorColumnName(self, field):
    """
      Returns the fieldname of the local field that describes
      the field. E.g.: 'user' describes 'usernr'; 'usernr' is a foreign
      key, 'user' the descriptive column, which is filled with
      the 'name' field from the user table.
    """
    relation=self.app.relations[self.tableDef.fields[field].relation]
    return relation.descriptors.local

    
  def getForeignDescriptorColumnName(self, field):
    relation=self.app.relations[self.tableDef.fields[field].relation]
    return relation.descriptors.foreign

    
  def getForeignKeyColumnName(self, field):
    relation=self.app.relations[self.tableDef.fields[field].relation]
    return relation.keys.foreign


  def getDescription(self):
    description=""
    for descriptor in self.tableDef.descriptors:
      if self.getFieldValue(descriptor) != None:
        description=description + ", " + self.getFieldValue(descriptor)
    return description[2:]

  def getLink(self):
    return self.getPrimaryKey()

class dbTable:

  def __init__(self, app, table, recObj=dbRecord ):
    self.app=app
    self.sql=app.sql
    self.table=table
    self.recObj=recObj #default dbRecord; object which stores the data
    self.rows=[]
    self.fieldOrder=self.app.tables[self.table].fieldOrder
    
  def __getitem__(self, key):
    return self.rows[key]

  def __repr__(self):
    return unicode(self.rows)

  def __len__(self):
    return len(self.rows)

  def select(self, queryRec, orderBy = None):
    """
      Create a list of dbRecord items that match the
      query defined by queryRec.
    """
    self.rows = self.sql.select(table=self.table,
                                queryRec=queryRec,
                                orderBy = orderBy)
    

  def export(self, queryRec, format):
    raise NotImplementedError("export function for %s not yet implemented." % self.table)


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.23 $
    Last edited          : $Date: 2002/12/28 15:23:50 $
    
 ***************************************************************************/
"""
