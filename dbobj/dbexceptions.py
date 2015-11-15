class dbError(Exception):
  def __init__(self, errorMessage):
    Exception.__init__(self)
    self.errorMessage=errorMessage

  def __repr__(self):
    return self.errorMessage

  def __str__(self):
    return self.errorMessage

class dbRecordNotFoundException(dbError):
  def __init__(self, tableName, queryRec ):
    dbError.__init__(self, "No such record in table %s" % tableName)
    self.queryRec=queryRec 

class dbTooManyRowsException(dbError):
  def __init__(self, tableName, queryRec ):
    dbError.__init__(self, "More than one record in table %s" % tableName)
    self.queryRec=queryRec 
    
class dbRepositoryError(dbError):
  def __init__(self, error, tableName):
    dbError.__init__(self, error % tableName)
    self.tableName=tableName

class dbModuleError(dbError):
  def __init__(self, error):
    dbError.__init__(self, error) 

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.3 $
    Last edited          : $Date: 2002/11/16 12:36:56 $
 ***************************************************************************/
"""
