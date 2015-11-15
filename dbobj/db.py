"""
  Object oriented database interface. Alter the definition
  of api to switch to another DB-API II compliant database
  interface.
  
 Database  
  
  DB:           db-api II compliant module
  
  dbConn:       connection, executing sql statemens
  dbResult:     result from action on the database
  dbSql:        assembling sql statement 
  
 Data
  
  dbFieldErr:   fieldname + error description
  dbRecord:     columns + values: offers insert, update, delete.
                   Provides generic data validation.
  dbTable:      coleection of dbRecords: offers select (based on a dbRecord).
  
 Application definition
  
  dbFieldDef:   field property definitions (length, nullable, etc.)
                   Provides  generic data validation information.
  dbRecDef:     record definition (list of dbFieldDefs)
  dbTableDef:   table property definitions (table type,
                   related tables, prefixes)
  

 Application objects

   recObj:      object for every entity, containing a record definition
                   which consists of field definitions. Provides
                   application intelligence and specific data validation.
   tableObj:    collection object for every entity. Collects actual data
                   in dbRecord objects and is based on dbTable for generic
                   select functionality.

   appObj:       collection of tableObjs, definining the entire
                   application. The user interface accesses the appObj.
                   (Perhaps I should make appObj optionally a Corba
                   server?)

 TODO 

  * object oriented error mechanism
  * calculating sequence values
  * return values in batches
"""

api="MySQLdb"

try:
  DB=__import__(api)
except ImportError:
  print "Importing db api failed"

# constants

TRUE  = 1
FALSE = 0

#

# Database access classes
#
from dbexceptions import *

class dbConn:
  """
    Generic connection object.
  """
  def __init__(self, host='',user='',database='',password=''):
    if host==None:
      host = 'localhost'
    if user==None:
      user = 'username'
    if database=='' or database==None:
      print "A databasename is required. None was given, trying kura"
      database = "kura"
    if password==None:
      password = ''

    self.dbConnection=DB.connect( host=host
                                , user=user
                                , db=database
                                , passwd=password
                                )
    self.dbCursor=self.dbConnection.cursor()
    try:
      self.dbDictCursor=self.dbConnection.cursor(DB.DictCursor)
    except:
      self.dbDictCursor=self.dbConnection.cursor(DB.cursors.DictCursor)
    
  def do (self, query, paramlist={}):
    """
      Execute SQL that doesn't return a resultset
    """

    try:
      self.dbCursor.execute(query, paramlist)

    except Exception, e:
      raise dbModuleError("MySQL error: " +
                         unicode(e))
      
    
  def query (self, query, paramlist={}):
    """
      Execute a query - TODO: add a version that returns results in batches instead
                          of all in one.
      Returns a resultset.
    """
    try:
      self.dbCursor.execute(query, paramlist)
    finally:
      
      return { "rowcount":    self.dbCursor.rowcount
             , "description": self.dbCursor.description
             , "rows":        self.dbCursor.fetchall()
             }

  def dictQuery(self, query, paramlist=()):
    self.dbDictCursor.execute(query, tuple(paramlist))
    return self.dbDictCursor.fetchallDict()
      
__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.8 $
    Last edited          : $Date: 2002/12/20 15:39:36 $
    
    CVS Log:         
    $Log: db.py,v $
    Revision 1.8  2002/12/20 15:39:36  boud
    ...

    Revision 1.7  2002/12/06 07:24:08  boud
    ...

    Revision 1.6  2002/07/31 09:20:19  boud
    Added docbook export to streams.

    Revision 1.5  2002/07/02 20:55:12  boud
    porting...

    Revision 1.4  2002/06/17 14:06:09  boud
    Interlinear texts are back + pychecker checks

    Revision 1.3  2002/05/01 07:38:33  boud
    Started on table integration.

    Revision 1.2  2002/04/06 12:39:27  boud
    Building unittests for dbObj

    Revision 1.1.1.1  2002/03/27 23:48:31  boud
    Kura for Qt 3

    Revision 1.3  2002/03/02 14:05:26  boudewijn
    ...

    Revision 1.2  2002/01/22 21:03:42  boud
    Manu changes.

    Revision 1.6  2001/02/01 19:53:25  boud
    Made more robust in connecting

    Revision 1.5  2001/01/31 20:04:13  boud
    Added exception handling.

    Revision 1.4  2001/01/15 20:21:06  boud
    Added import/export filters, bugfixes.

    Revision 1.3  2001/01/08 20:55:00  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
