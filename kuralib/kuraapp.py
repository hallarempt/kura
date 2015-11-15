"""
KuraApp is the class that defines all the various tables that Kura
uses in a repository. It inherits dbAppDef, which means that it has
several convenience functions to query the database.
"""
False = 0
True = 1

import sys, os

from dbobj.sql import dbSql
from dbobj.textdb.textquery import TextQuery

from dbobj.appobj import *
from dbobj.dbtypes import *
from lngapp import setRepository
from lngobj import setObjects

#
# Repository object
#

class KuraApp(dbAppDef):
    """
    KuraApp is a central portal to the database. It manages a repository
    that defines both the data model and the presentation of the data. It
    also manages the connection to the database.
    """
    def __init__(self,):
        self.initialized = False
    
    def init(self, backend, **args):
        dbAppDef.__init__(self, None)
        setRepository(self)
        setObjects(self)
        self.settings()        
        self.sql = globals()[backend](self, **args)
        self.initialized = True

    def isDirty(self):
        try:
            return self.sql.isDirty()
        except:
            return False


    def openFile(self, filename):
        self.sql = TextQuery(self, filename)

    def saveFile(self, filename = None):
        self.sql.saveDatabase(filename)
        
    def settings(self, **args):
        """
        Certain fields can have default values that can be used in
        queries, updates and inserts. This is where those are set.
        """
        self.fieldDefaults=args

    def reconnect(self, hostname, username, database, password):
        self.sql = dbSql(self,
                         username = username,
                         database = database,
                         password = password,
                         hostname = hostname)
    
app = KuraApp()


def initApp(backend, **args):
    sys.stderr.write( "Initializing repository\n")
    app.init(backend = backend, **args)

def initCurrentEnvironment(usernr, languagenr, projectnr):
    app.settings(usernr=usernr,
                 languagenr=languagenr,
                 projectnr=projectnr)



__copyright__="""
/***************************************************************************
        copyright                        : (C) 2002 by Boudewijn Rempt 
                                            see copyright notice for license
        email                            : boud@valdyas.org
        Revision                         : $Revision: 1.18 $
        Last edited                      : $Date: 2002/11/16 12:37:03 $
 ***************************************************************************/
"""
