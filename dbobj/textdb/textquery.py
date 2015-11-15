import string, sys, os.path, cPickle, time

from table import Table

True = 1
False = 0

class TextQuery:
    """
    Class to generate dynamic sql statements.
    """
    def __init__(self, app, dbfile):
        self.__dirty = False
        self.__app = app
        self.dbfile = dbfile
        print "Opening datastore: ", dbfile
        if os.path.exists(self.dbfile):
            try:
                t = time.time()
                self.database = cPickle.loads(open(self.dbfile, "rb").read())
                print "Loading database:", time.time() - t, "seconds"
            except EOFError, e:
                print "Database", self.dbfile, " corrupted."
                sys.exit(1)
        else:
            self.database = self.__createDatabase(app)


    def __createDatabase(self, app):
        db = {}
        for k, v in app.tables.items():
            db[k] = Table(k, v)
        return db


    def saveDatabase(self, fileName = None):
        if fileName:
            self.dbfile = fileName
        f = open(self.dbfile, "w+b")
        t = time.time()
        f.write(cPickle.dumps(self.database, 1))
        self.__dirty = False
        print "Saving database:", time.time() - t, "seconds"


    def isDirty(self):
        return self.__dirty
        

    #
    # DML functions
    #
   
    def select(self, table, queryRec=None, orderBy = None):
        t = time.time()
        rows = []
        resultSet = self.database[table].select(queryRec)
        for row in resultSet:
            rec = queryRec.__class__(app = self.__app,
                                     table = table,
                                     fields = row)
            for rname in self.__app.tables[table].lookuptables:
                relation = self.__app.relations[rname]
                v = rec.getFieldValue(relation.keys.local)
                if v == None or v == "" or v == 0:
                    continue
                rec.setFieldValue(relation.descriptors.local,
                                  self.database[relation.rtable].get(v)[relation.descriptors.foreign])
            rows.append(rec)
##         print "Select %i rows from %s: %i seconds" % (len(rows), table, time.time() - t)

        return rows
            

    def insert(self, table, queryRec, save = False):
        self.__dirty = True
        self.database[table].insert(queryRec)
        if save:
            self.saveDatabase()
            self.__dirty = False


    def update(self, table, queryRec, save = False):
        self.__dirty = True
        self.database[table].update(queryRec)
        if save:
            self.saveDatabase()
            self.__dirty = False
    
    def delete(self, table, queryRec, save = False):
        self.__dirty = True
        self.database[table].delete(queryRec)
        if save:
            self.saveDatabase()
            self.__dirty = False

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.9 $
    Last edited          : $Date: 2002/11/11 18:19:09 $
    
 ***************************************************************************/
"""
