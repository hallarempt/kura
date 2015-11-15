"""

  Assembling sql statements.

  The assembled sql statement is sent to the database together with
  a list of key-value pairs that'll fill in the %s blanks. Incidentally,
  these %s blanks in the generated sql statements are the reason I use
  string.join a lot, instead of creating the statements themselves with
  %s substitution everywhere.

  14/07/2000: added testcase 
  12/07/2000: added createTable method
  10/07/2000: composite primary keys are no longer supported
  22/05/2000: Useful bits of statements get cached.

  TODO: * move db-specific code to specific database adaptor modules
  (e.g. outer joins)
        * replace primary key generator with GUID generator (but that
          would require _big_ primary key fields).
        * Fix inserting of sequential tables.
        
"""
import string

from dbtypes import *
from db      import dbConn

import sys

class dbSql:
  """
    Class to generate dynamic sql statements.
  """
  def __init__(self, app, hostname='', username='', database='', password=''):
    self.dbc=dbConn( host=hostname
                   , user=username
                   , database=database
                   , password=password
                   )

    self.__selectCache={}
    self.__fromCache={}
    self.__whereCache={}
    self.__setCache={}
    self.__app = app
  #
  # Utility functions
  #

  def nullAllowed(self, key, tableDef):
    """
      Check whether all fields are nullable.
    """
    return tableDef.fields[key.local].nullable

  #
  # Clause generation functions
  #

  def __insertList(self, table, queryRec):
    """
      generate the fields and values clause of an insert statement
    """
    tableDef=self.__app.tables[table]
    
    strValues=""
    strFields=""

    for (field, fieldDef) in tableDef.orderedFieldList():
      if (    fieldDef.owner
          and getattr(queryRec, field) <> None
          and getattr(queryRec, field) <> ""):
        # empty cols are not inserted; they are given default values by the db.
        strFields = string.join(( strFields, ", ", field, "\n"),"")
        strValues = string.join(( strValues, ", %s \n"),"")
      
    return string.join(("insert into ", table, "\n", "("
                        , strFields[1:]
                        , ") values ( \n"
                        , strValues[1:]
                        , ")"
                        )
                        ,"")

  def __deleteList(self, table):
    return " delete from %s" % table
    
  def __selectList(self, table):
    """
      Form an SQL select clause, complete with foreign keys.
      Almost as good as a view ;-). 
	  
	  FIXME: database dependent
    """
    if not self.__selectCache.has_key(table):

      strSQL=""
      tableDef=self.__app.tables[table]
      #
      # Own fields
      #
      for (fieldname, field) in tableDef.orderedFieldList():
        if field.owner == 1: # local field
          strSQL=string.join((strSQL, ",  ",
                              tableDef.alias, ".",
                              fieldname, "\n"),"" )
      #
      # related fields
      #
      for rname in tableDef.lookuptables:
        relation=self.__app.relations[rname]
        strSQL=string.join( ( strSQL
                            , ",   "
                            , relation.ralias
                            , "."
                            , relation.descriptors.foreign
                            , " as "
                            , relation.descriptors.local
                            , "\n"
                            ), ""
                            )
      self.__selectCache[table]= "select " + strSQL[1:]

    return self.__selectCache[table]

  def __fromList(self, table):
    """construct an SQL from clause complete with left joins.
       I hope this really is real ANSI syntax for outer joins...

       No, it isn't! And it turns out that the results can differ,
       too.

       Damn and blast!

       FIXME: database-dependent.       
    """
    if not self.__fromCache.has_key(table):
      tableDef=self.__app.tables[table]
      strSQL=" from " + table + " " + tableDef.alias + "\n"
      #
      # Joins
      #
      for rname in tableDef.lookuptables:
        relation=self.__app.relations[rname]
        if self.nullAllowed(relation.keys, tableDef):
          # optional join = outer join
          strSQL=string.join ( ( strSQL
                               , " left join "
                               , relation.rtable
                               , " "
                               , relation.ralias
                               , "\n"
                               , " on "
                               , "\n"
                               , tableDef.alias
                               , "."
                               , relation.keys.local
                               , "="
                               , relation.ralias
                               , "."
                               , relation.keys.foreign
                               , "\n"
                               ),""
                               )

        else: # obligatory join
          strSQL=string.join ( ( strSQL
                               , ", "
                               , relation.rtable
                               , " "
                               , relation.ralias
                               , "\n"
                               ), ""
                               )
      self.__fromCache[table]=strSQL
    return self.__fromCache[table]    

  def __whereList(self, table, queryRec=None):
    """
      Generate a where clause based on the not-null
      fields in a Query rec and the obligatory join
      fields.
      
      Most modern databases optimize 'like' clauses with values without
      wildcards automatically into '=' clauses - doing the optimization
      in Python takes too much time.
    """
    tableDef=self.__app.tables[table]
    strSQL=""
    if not self.__whereCache.has_key(table):
      #
      # joins with obligatory join fields
      #
      for rname in tableDef.lookuptables:
        relation=self.__app.relations[rname]
        if not self.nullAllowed(relation.keys, tableDef):
          strSQL=string.join ( (strSQL
                                , "and "
                                , tableDef.alias
                                , ".", relation.keys.local, "="
                                , relation.ralias
                                , "."
                                , relation.keys.foreign
                                , "\n"
                                ), ""
                              )
      self.__whereCache[table]=strSQL

    strSQL=self.__whereCache[table]
    #
    # query rec
    #
    if queryRec <> None:
      for (fieldname, field) in tableDef.orderedFieldList():
        if (    field.owner 
            and getattr(queryRec, fieldname) <> None
            and getattr(queryRec, fieldname) <> ""):
          strSQL=string.join(( strSQL
                             , "and "
                             , tableDef.alias
                             , "."
                             , fieldname
                             , " like %s "
                             , "\n"
                             ) ,"")
    if strSQL=="":
      return ""
    else:
      return "where " + strSQL[3:]
    
  def __orderBy(self, table):
    """
      Generate an order by clause, but only for SEQ-type tables.
      Otherwise, Python will no doubt be faster in sorting than
      the database. (Or the interface elements themselves...)
    """
    tableDef=self.__app.tables[table]
    if tableDef.tabletype==SEQ:
      strSQL=""
      for (fieldname, field) in tableDef.fields.items():
        if field.sequence:
          strSQL=string.join(( ", ", tableDef.alias, ".", fieldname), "")
          
      if strSQL<>"":
        return "order by " + strSQL[1:]
      else:
        return ""
    else:
      return ""


  def __nextSequence(self, table, tableDef, queryRec):
    """
    Select the next sequential number in a SEQ table, i.e. where
    the records are ordered,
    
    FIXME: for now, the sequence column is hardcoded as seqnr
    """
    strSQL="""select max(seqnr) + 1 as nextval 
              from   %s 
              where  %s=%s""" % ( table
                                , tableDef.sequencebase
                                , queryRec.getFieldValue(tableDef.sequencebase)
                                )
    rs=self.dbc.query(strSQL)
    nextval=rs.rows[0][0]
    if nextval==None:
      return 1
    else:
      return nextval      

  def __updateList(self, table):
    return "update %s \n" % (table)

  def __pkWhere(self, tableDef):
    """
      Generate a where clause with only the primary keys.
      Useful for update and delete. (You can't update a record
      by where'ing for the field values you've just changed,
      and you don't want to accidentally delete a whole table
      by offering dbSql.delete an empty queryRec!)
    """
    return "where " +tableDef.primarykey+"= %s \n"
  
  def __pkValuesList(self, tableDef, queryRec):
    return [queryRec.getFieldValue(tableDef.primarykey)]
    
  def __setList(self, tableDef):
    if not self.__setCache.has_key(tableDef):
      strSQL=""
      for (field, fieldDef) in tableDef.orderedFieldList():
        if fieldDef.owner:
          strSQL=string.join(( strSQL
                             , ", "
                             , field
                             , "= %s \n"
                             ),""
                            )
      self.__setCache[tableDef]="set" + strSQL[1:]
    return self.__setCache[tableDef]
    
  def __valuesList(self, fields, queryRec = None, skipNone = TRUE):
    """
      Return a list with values from queryRec that matches
      the order of fields in the other SQL clauses. Skips
      empty fields by default.
    """
    if queryRec==None:
      return []
    else:
      valuesList=[]
      for (field, fieldDef) in fields:
        if fieldDef.owner:
          if hasattr(queryRec, field):
            val=getattr(queryRec, field)
            if skipNone:
              if val<> None and val <> "":
                if fieldDef.datatype==INTEGER:
                  valuesList.append (int(val))
                else:
                  valuesList.append (val)
            else:
              valuesList.append(val)
      return valuesList
   
  #
  # DML functions
  #
    
  def select(self, table, queryRec, orderBy = None):
    """
    Returns a list contaning dbRecord objects
    """
    tableDef=self.__app.tables[table]
    q = [self.__selectList(table),
         self.__fromList(table),
         self.__whereList(table, queryRec)]
    if orderBy:
      q.append(orderBy)
    else:
      q.append(self.__orderBy(table))
    strSQL="".join(q)
    rows = []
    for row in self.dbc.dictQuery(strSQL,
                                  self.__valuesList(tableDef.orderedFieldList(),
                                                    queryRec)):
      rows.append(queryRec.__class__(app = self.__app,
                                     table = table,
                                     fields = row))
    return rows
    
    
  def insert(self, table, queryRec):
    tableDef=self.__app.tables[table]
    #
    # Get the next value for the sequence key
    #
    if tableDef.tabletype==SEQ:
      if (queryRec.seqnr == None and
          queryRec.getFieldValue(tableDef.sequencebase) != None):
        queryRec.seqnr=self.__nextSequence(table, tableDef)
        
    #
    # Make the SQL string
    #
    strSQL=self.__insertList(table, queryRec)
    #
    # Do the actual insert
    # 
    vl=self.__valuesList(tableDef.orderedFieldList()
                                  , queryRec
                                  )
    self.dbc.do( strSQL
               , vl
               )
    # We don't have to return anything, since we alter the queryRec object
    # in place. It would be strange to have the following:
    #   a=dbRecord()
    #   a=a.insert()
    # I feel.
    
    #
    # FIXME: this is MySQL dependent into the extreme.
    #
    if (   tableDef.tabletype==PKNR 
        or tableDef.tabletype==SEQ 
        or tableDef.tabletype==RECURS
       ):
      if tableDef.fields[tableDef.primarykey].autoincrement:
        queryRec.setFieldValue(tableDef.primarykey,
                               self.dbc.dbCursor.insert_id())


  def update(self, table, queryRec):
    """
      Update records in a table according to the specifications of queryRec

      the try...except is here because MySQL insists upon warning us that
      the update has changed a row, and that causes a bloody exception.
    """
    
    tableDef=self.__app.tables[table]
    strSQL=string.join(( self.__updateList(table)
                       , self.__setList(tableDef)
                       , self.__pkWhere(tableDef)
                       ),"")
    vals= (self.__valuesList( tableDef.orderedFieldList()
                            , queryRec
                            , skipNone=FALSE
                            ) 
          + self.__pkValuesList( tableDef
                               , queryRec
                               )
          )
    try:
      self.dbc.do( strSQL
                 , vals
                 )
    except:
      pass
##      sys.stderr.write( "Exception caught in update " +
##                        unicode(sys.exc_info()[0]) + "\n" )
    
  def delete(self, table, queryRec):  
    """
      Delete records from one table according to the specifications of
      queryRec.
    """
    tableDef=self.__app.tables[table]
    strSQL=string.join(( self.__deleteList(table)
                       , self.__pkWhere(tableDef)
                       ),"\n")
    self.dbc.do( strSQL, self.__pkValuesList(tableDef, queryRec))


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.10 $
    Last edited          : $Date: 2002/10/28 21:34:15 $

 ***************************************************************************/
"""
