#!/usr/bin/env python
"""
  Unittests for dbobj
"""

# temporary constants
HOSTNAME = 'localhost'
DATABASE = 'andal'
DATABASE2 = 'kura'
USERNAME = 'boud'
PASSWORD = ''

TABLENAME = "table"
CHILDTABLENAME = "childtable"

import unittest, sys, string, codecs, time
from appobj import *
from dbobj import dbTable
from dbtypes import *
from db import dbConn
from sql import dbSql
from dbexceptions import dbModuleError
from textdb.table import Table

class dummyRecordClass(dbRecord):
    
    def __init__(self, app, **args):
        if args.has_key("fields"):
            dbRecord.__init__(self, app, TABLENAME, args["fields"])
        else:
            dbRecord.__init__(self, app, TABLENAME, args)



class dummyTableClass(dbTable):
    
    def __init__(self, app):
        dbTable.__init__(self, app=app, table=TABLENAME, recObj=dummyRecordClass)



def createChildTableObject(self):
    return dbTableDef(PKNR, CHILDTABLENAME, "pk",
                      {"pk": self.pkField,
                       "description": self.descriptionField,
                       "uniq": self.uniqueField,
                       "sequence": self.sequenceField},
                      ["description"], {},
                      ["lookuptable"],
                      ["pk", "description", "uniq", "sequence"],
                      ["uniq"], ["description"], "test table",
                      "A table for testing",
                      "A hint", "sequence")



def createParentTableObject(self):
    return dbTableDef(PKNR, "test", "pk",
                      {"pk": self.pkField,
                       "description": self.descriptionField,
                       "uniq": self.uniqueField,
                       "sequence": self.sequenceField},
                      ["description"],
                      {"childTable": self.childTable},
                      ["lookuptable"],
                      ["pk", "description", "uniq", "sequence"],
                      ["uniq"], ["description"], "test table",
                      "A table for testing", "A hint", "sequence")
        

class AppObjTestCase(unittest.TestCase):



    def setUp(self):
        self.dbc = dbConn(HOSTNAME, USERNAME, DATABASE, PASSWORD)

        try:
            self.dbc.do(DROP);
        except dbModuleError, dme:
            pass #print "Error dropping test table ", dme
            
        self.dbc.do(CREATE);

        self.sql = dbSql(HOSTNAME, USERNAME, DATABASE, PASSWORD)

        self.pkField = dbFieldDef(name="pk", pk=TRUE)
        self.descriptionField = dbFieldDef(name="description")
        self.uniqueField = dbFieldDef(name="uniq")
        self.sequenceField = dbFieldDef(name="sequence", sequence = TRUE)
        self.childTable = createChildTableObject(self)
        self.table = createParentTableObject(self)
        
        self.objects = {TABLENAME: dbAppObj(dummyRecordClass,
                                            dummyTableClass,
                                            "Table Label"),}
        

        
    def tearDown(self):
        try:
            self.dbc.do(DROP);
        except dbModuleError, dme:
            print "Error dropping test table ", dme

    def __prepareApp(self):
        app = dbAppDef(self.sql)
        app.addDef(childtable = self.childTable)
        app.addDef(table = self.table)
        app.objects = self.objects
        app.fieldDefaults = {"description": "A description"}
        return app


    def testInstantiation(self):
        app = dbAppDef(self.sql)


    def DONOTtestReconnect(self):
        app = dbAppDef(self.sql)
        app.reconnect(HOSTNAME, USERNAME, DATABASE2, PASSWORD)
        assert app.sql != self.sql, "Reconnecting failed"


    def testGetLabel(self):
        app = self.__prepareApp()
        assert app.getLabel(CHILDTABLENAME) == CHILDTABLENAME, \
               "Wrong label for child: " + app.getLabel(CHILDTABLENAME)
        assert app.getLabel(TABLENAME) == "Table Label", \
               "Wrong label for parent " + app.getLabel(TABLENAME)

    def testGetTableDef(self):
        app = self.__prepareApp()
        tableDef = app.getTableDef(TABLENAME)
        assert tableDef.getChildDef("childTable") != None, \
               "Didn't get the child back."
        

    def testGetDefaultValueFor(self):
        app = self.__prepareApp()
        val = app.getDefaultValueFor("description")
        assert val == "A description", \
               "Default value for description is " + val


    def testCreateDefaultObject(self):
        app = self.__prepareApp()
        rec = app.createDefaultObject(CHILDTABLENAME,
                                      description = "test")
        assert rec.__class__ == dbRecord, \
              "Wrong class: " + str(rec.__class__)


        rec = app.createDefaultObject(TABLENAME,
                                      description = "test")
        assert rec.__class__ == dummyRecordClass, \
              "Wrong class: " + str(rec.__class__)


    def testCreateObject(self):
        app = self.__prepareApp()
        rec = app.createObject(CHILDTABLENAME,
                               description = "test")
        assert rec.__class__ == dbRecord, \
              "Wrong class: " + str(rec.__class__)

        rec = app.createObject(TABLENAME,
                               description = "test")
        assert rec.__class__ == dummyRecordClass, \
              "Wrong class: " + str(rec.__class__)

    def testCreateTableObject(self):
        app = self.__prepareApp()
        tbl = app.createTableObject(CHILDTABLENAME)
        assert tbl.__class__ == dbTable, \
              "Wrong class: " + str(tbl.__class__)

        tbl = app.createTableObject(TABLENAME)
        assert tbl.__class__ == dummyTableClass, \
              "Wrong class: " + str(tbl.__class__)


    def testGetObject(self):
        pass


    def testGetObjects(self):
        pass


    def testGetTableLable(self):
        pass


    def testAddDef(self):
        app = self.__prepareApp()
        assert len(app.tables) == 2, \
               "Wrong number of tables added."


    def testToXML(self):
        pass


    def testToSQL(self):
        pass


    def testXMLInit(self):
        pass


    def testTextTable(self):
        """ Tests the plaintext backend of dbobj. """
        app = self.__prepareApp()
        textTable = Table("test", self.table)
        assert textTable.getName() == "test", \
               "Wrong name returned"
        rec = app.createDefaultObject(TABLENAME)
        try:
            textTable.insert(rec)
            fail("Could insert record with None object as primary key")
        except:
            pass
        
        rec.pk = 1
        rec.description = "description"
        rec.uniq = "unique"

        rec2 = app.createDefaultObject(TABLENAME)
        rec2.pk = 2
        rec2.description = "description rec2"
        rec2.uniq = "unique rec2"

        textTable.insert(rec)
        textTable.insert(rec2)

        assert len(textTable) == 2, \
               "Wrong number of rows in table, should be 2, was " \
               + len(textTable)
        try:
            textTable.insert(rec)
            fail("Could insert record twice")
        except:
            pass
        
        assert len(textTable) == 2, \
               "Wrong number of rows in table, should still be 2, was " \
               + len(textTable)


        # Test update
        rec.setFieldValue("description", "updated description")
        textTable.update(rec)
        searchRec = app.createDefaultObject(TABLENAME)
        searchRec.pk = 1
        result = textTable.select(searchRec)
        assert result[0]["description"] == "updated description", \
               "Update failed: should have been %s, was %s" % \
               ("updated description", result[0]["description"])
        
        # Search with empty record object
        searchRec = app.createDefaultObject(TABLENAME)
        searchRec.description = None
        result = textTable.select(searchRec)

        assert len(result) == 2, \
               "Wrong number of rows selected, should be 2, was" \
               + str(len(result))

        # Search by primary key
        searchRec = app.createDefaultObject(TABLENAME)
        searchRec.pk = 2
        result = textTable.select(searchRec)
        assert len(result) == 1, \
               "Wrong number of rows selected, should be 1, was" \
               + str(len(result))

        # Search by any field
        searchRec = app.createDefaultObject(TABLENAME)
        searchRec.description = "updated description"
        result = textTable.select(searchRec)
        assert len(result) == 1, \
               "Wrong number of rows selected, should be 1, was " \
               + str(len(result))


        # Search by unique field
        searchRec = app.createDefaultObject(TABLENAME)
        searchRec.uniq =  "unique rec2"
        searchRec.description = None
        result = textTable.select(searchRec)
        assert len(result) == 1, \
               "Wrong number of rows selected, should be 1, was " \
               + str(len(result))

        # Search by wildcard field
        searchRec = app.createDefaultObject(TABLENAME)
        searchRec.description = "%description%"
        result = textTable.select(searchRec)
        assert len(result) == 2, \
               "Wrong number of rows selected, should be 1, was " \
               + str(len(result))


class TableObjTestCase(unittest.TestCase):

    def setUp(self):
        
        self.pkField = dbFieldDef(name="pk", pk=TRUE)
        self.descriptionField = dbFieldDef(name="description")
        self.uniqueField = dbFieldDef(name="uniq")
        self.sequenceField = dbFieldDef(name="sequence", sequence = TRUE)
        
        self.childTable = createChildTableObject(self)
        
    def testInstantiation(self):
        tableDef = createParentTableObject(self)
                               

    def testOrderedFieldList(self):
        tableDef = createParentTableObject(self)

        
        order = [("pk", self.pkField),
                 ("description", self.descriptionField),
                 ("uniq", self.uniqueField),
                 ("sequence", self.sequenceField)]
        

        assert tableDef.orderedFieldList() == order, \
               "Sequence not equal"


    def testGetChildDef(self):
        tableDef = createParentTableObject(self)
        
        childTable = tableDef.getChildDef("childTable")
        
        assert childTable == self.childTable, \
               "Children not equal"



def suite():
    s1 = unittest.makeSuite(AppObjTestCase, "test")
    s2 = unittest.makeSuite(TableObjTestCase, "test")
    
    testSuite=unittest.TestSuite((s1, s2))
    return testSuite

def main():
    runner = unittest.TextTestRunner(sys.stderr, 1, 2)
    runner.run(suite())


DROP = "drop table test"
CREATE = """
create table test
( pk          integer unsigned not null auto_increment
,    primary  key (pk)
, description varchar(255)
,    index i_d (description)
, uniq        varchar(255) not null
,    unique u_u (uniq)
, sequence    int not null
,    unique u_s (sequence)
)
               """


if __name__=="__main__":
    main()


__copyright__="""
/***************************************************************************
        copyright                        : (C) 2002 by Boudewijn Rempt 
                                            see copyright notice for license
        email                            : boud@valdyas.org
        Revision                         : $Revision: 1.6 $
        Last edited                      : $Date: 2002/10/28 13:28:45 $
        
        CVS Log:                 

        $Log: unittests.py,v $
        Revision 1.6  2002/10/28 13:28:45  boud
        fixed index handling of text backend, updating and removed some
        config properties that were only confusing people.

        Revision 1.5  2002/10/23 21:07:20  boud
        It's now possible to use a file/memory based backend for Kura
        instead of a database.

        Revision 1.4  2002/10/15 21:07:01  boud
        search, update and delete functionality of file-based backend
        done.

        Revision 1.3  2002/10/15 17:04:14  boud
        Added begin of text-only backend

        Revision 1.2  2002/04/06 22:30:11  boud
        Added several unittests.

        Revision 1.1  2002/04/06 12:39:27  boud
        Building unittests for dbObj


 ***************************************************************************/
"""
