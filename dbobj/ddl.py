import string, types

from dbtypes import *
from db      import dbResult, dbConn

class dbDDL:
  """
    Generate DDL statements. Due to the wild differences in
    SQL implementations, this class is very database dependent.
    However, it should be possible to factor out the dependencies
    in a kind of adaptor table...
  """  
  def __init__(self, relations):
    self.relations=relations
    
  def getCreateTableDDL(self, tableDef):
    """
    Returns a create-table script according to the definition in the
    repository.

    FIXME: separate this out: database dependent.
       
    """
    #s="drop table %s;\n" % tableDef.name
    s=""
    for field, fieldDef in tableDef.fieldList:
      # field definitions
      if fieldDef.owner==TRUE:
        s=s+",    %s" % (fieldDef.name)
        if fieldDef.datatype==INTEGER:
          s="%s INTEGER UNSIGNED" % s
          if fieldDef.autoincrement==TRUE:
            s="%s auto_increment" % s
        elif fieldDef.datatype==VARCHAR:
          s="%s varchar(%s)" % (s, unicode(fieldDef.length))
        elif fieldDef.datatype==TEXT:
          s="%s text" % s
        elif fieldDef.datatype==BOOLEAN:
          s="%s numeric(1,0)" %s
        elif fieldDef.datatype==DATETIME:
          s="%s date" %s
   
        if fieldDef.nullable==FALSE:
          s="%s not null" % s

        if fieldDef.default<>"" and fieldDef.default !=None:
          if fieldDef.datatype==VARCHAR or fieldDef.datatype==TEXT:
            s='%s default "%s"' % (s, fieldDef.default)
          else:
            s="%s default %s" % (s, fieldDef.default)

        s=s+"\n" 
        # constraints

        if fieldDef.pk==TRUE:
          s=s + ",\t primary key(%s)\n" % field
                    
        #if fieldDef.relation<>None:
        #  #FIXME: this doesn't do anything for MySQL.
        #  relation=self.relations[fieldDef.relation]
        #  s=s+",\t foreign key fk_%s_%s (%s) references %s(%s);\n" % ( tableDef.alias,
        #                                                          relation.ralias,
        #                                                          field,
        #                                                          relation.rtable,
        #                                                          relation.keys.foreign)
    s="create table %s (\n%s);\n\n"  % (tableDef.name, s[2:])
    index_counter=1
    for index in tableDef.indexes:
      s=s+'alter table %s add index i_%s_%s (' % (tableDef.name, tableDef.alias, unicode(index_counter))
      index_counter=index_counter + 1
      for field in index:
        s=s + field + ","
      s=s[:-1] + ");\n"
      
    index_counter=1      
    for index in tableDef.unique_indexes:
      s=s+'alter table %s add unique index i_%s_%s (' % (tableDef.name, tableDef.alias, unicode(index_counter))
      index_counter=index_counter + 1
      for field in index:
        s=s + field + ","
      s=s[:-1] + ");\n"

    return s
#
# Testcase
#

def main():
  from appobj import *
  from dbtypes import *
  ddl=dbDDL()
  print ddl.getCreateTableDDL(dbTableDef( tabletype=PKNR
                         , name="lng_lex_lex"
                         , alias="lxlx"
                         , lookuptables=["lxlx_user", "lxlx_lex1", "lxlx_lex2"]
                         , primarykey="lxlxnr"
                         , indexes=[("lexnr_1",),("lexnr_2",), ("value",)]
                         , unique_indexes=[("lexnr_1", "lexnr_2")]
                         , descriptors=["form_1", "form_2", "value"]
                         , fields= { 'lxlxnr' : dbFieldDef(name="lxlxnr", pk=TRUE, length=10, datatype=INTEGER, autoincrement=TRUE)
                           ,'lexnr_1': dbFieldDef( name="lexnr_1", datatype=INTEGER
                                                  , length=10
                                                  , relation=dbRelationDef(name="lxlx_lex1"
                                                       , keys=dbPair("lexnr_1", "lexnr")
                                                       , descriptors=dbPair("form_1", "form")
                                                       , rtable="lng_lex"
                                                       , ralias="lex1"
                                                       )
                                                   )
                           , 'form_1'    : dbFieldDef(name="form_1", owner=FALSE )
                           , 'lexnr_2'   : dbFieldDef( name="lexnr_1", datatype=INTEGER
                                             , length=10
                                             , relation=dbRelationDef(name="lxlx_lex2"
                                                   , keys=dbPair("lexnr_2", "lexnr")
                                                   , descriptors=dbPair("form_2", "form")
                                                   , rtable="lng_lex"
                                                   , ralias="lex2"
                                                   )                                             )
                           , 'form_2'    : dbFieldDef( name="form_2", owner=FALSE )
                           , 'value'     : dbFieldDef(name="value")
                           , "usernr"    : dbFieldDef( name="usernr", nullable=FALSE
                                             , length=10
                                             , datatype=INTEGER
                                             , relation=dbRelationDef(name="lxlx_user"
                                                   , keys=dbPair("usernr", "usernr")
                                                   , descriptors=dbPair("user", "name")
                                                   , rtable="lng_user"
                                                   , ralias="user"
                                             ))
                           , "user"      : dbFieldDef(name="user", owner=FALSE )
                           , "datestamp" : dbFieldDef(name="datestamp", datatype=DATETIME, auto=TRUE)
                           })
                    )

 
if __name__=="__main__":
  main()

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.1.1.1 $
    Last edited          : $Date: 2002/03/27 23:48:31 $
    
    CVS Log:         
    $Log: ddl.py,v $
    Revision 1.1.1.1  2002/03/27 23:48:31  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:42  boud
    Manu changes.

    Revision 1.3  2001/01/08 20:55:00  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
