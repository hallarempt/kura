"""
 Application definition classes (repository definition)

  dbPair:       pair of field, local and foreign
  dbRelationDef:   foreign key relation definition
  dbFieldDef:   field property definitions (length, nullable, etc.)
                   Provides  generic data validation information.
  dbRecDef:     record definition (list of dbFieldDefs)
  dbTableDef:   table property definitions (table type,
                   related tables, prefixes)
  dbAppDef:     collection of repository information  

"""
# FIXME: assert some basic repository saneness

import string, sys

from dbtypes import *
from dbobj import *
from sql import dbSql
from dbexceptions import *

    
class dbPair:
    """
        defines a pair of fields
    """
    def __init__(self, local, foreign):
        self.local=local
        self.foreign=foreign

    def __repr__(self):
        return self.local + ", " + self.foreign



class dbChildDef:
    """
        Defines a child relation, i.e. from parent to child
    """
    def __init__(self, childTable, keys):
        self.childTable = childTable
        self.keys = keys



class dbRelationDef:
    """
        Defines a foreign key relationship, i.e. from child to parent
    """
    def __init__(self, name, keys, descriptors, rtable, ralias):
        self.name=name                          # name of the relation
        self.keys=keys                          # tuple containing the relating keys
        self.descriptors=descriptors            # tuple containing the descriptive columns
        self.rtable=rtable                      # foreign table
        self.ralias=ralias                      # different alias, in case the alias of the rtable is
                                                # the same as the alias of the local table

    def __repr__(self):
        return "name: " + self.name + \
               "\nkeys: " + unicode(self.keys) + \
               "\ndescriptors: " + unicode(self.descriptors) + \
               "\nrtable: " + self.rtable + \
               "\nralias: " + self.ralias
      


class dbFieldDef:
    """
        Repository-like definition of the properties of a
        field in the database.
    """
    def __init__( self
                  , length = 255
                  , pk=FALSE
                  , datatype = VARCHAR
                  , nullable=TRUE
                  , sequence=FALSE
                  , owner=TRUE
                  , auto=FALSE
                  , default=None
                  , autoincrement = FALSE
                  , relation = None
                  , label = None
                  , dialog=TRUE
                  , inList=TRUE
                  , url=FALSE
                  , name=""
                  , comment=""
                  , hint=""
                  , readonly=FALSE
                  ):
                            
        self.length = length                # maximum length
        self.pk = pk
        self.datatype = datatype                            
        self.nullable=nullable
        self.sequence=sequence              # sequential columns
        self.owner=owner
        self.auto=auto                      # if the value is None, will the value
                                            # be added automatically by the database?
        self.default=default                                                                                    
        self.autoincrement=autoincrement    # autoincrement with
                                            # select max(fieldname) + 1 pity
                                            # not all databases support
                                            # returning the most recently
                                            # autoincremented number, like
                                            # MySQL
        self.relation=relation              # pointer to the dbRelationDef definition 
        self.label=label                    # label in lists and dialogs
        self.dialog=dialog                  # does the field appear in dialgs
        self.inList=inList                  # does the field in lists
        self.url=url                        # is this field an url
        self.name=name
        self.comment=comment
        self.hint=hint
        self.readonly=readonly



class dbTableDef:
    """
        Repository-like definition of tables.
    """
    def __init__( self, tabletype, alias,
                  primarykey = None,
                  fields = None,
                  descriptors=["description"],
                  childtables= None,
                  lookuptables=[],
                  fieldOrder=None,
                  unique_indexes=[],
                  indexes=[],
                  name="",
                  comment="",
                  hint="",
                  sequencebase=None):
        if fields == None: fields = {}
        if childtables == None: childtables = {}
        
        self.tabletype=tabletype          # relational type
        self.alias=alias                  # alias to be used in SQL statements
        self.primarykey=primarykey        # primary key (No longer a list! Every
                                          # table _must_ have a single-column
                                          # primary key!)
        self.fields=fields                # dictionary of fielddefinitions
        self.descriptors=descriptors      # list of columns that describe a record
                                          # to a user
        self.childtables=childtables       # list of child tables
        self.lookuptables=lookuptables     # list of parent relations
        self.unique_indexes=unique_indexes # list of tuples of fields that should
                                          # be uniquely indexed
        self.indexes=indexes              # list of tuples of fields that should be
                                          # indexed
        self.name=name
        self.comment=comment
        self.hint=hint
        self.sequencebase=sequencebase
        self.fieldOrder=fieldOrder
        #
        # Set the fieldname
        #
        for field, fielddef in self.fields.items():
            if fielddef.name=="":
                fielddef.name=field
        #
        # Hoping that the order is still the order we
        # entered the fields in.
        #
        self.fieldList=[]
        if fieldOrder==None:
            self.fieldList=self.fields.items()
            self.fieldOrder=self.fields.keys()
        else:
            for field in fieldOrder:
                self.fieldList.append((field, self.fields[field]))


    def orderedFieldList(self):
        """
            Return an ordered LIST of the fields in fhe fields dictionary.
            Necessary to be able make up matched field/value pairs
        """
        return self.fieldList


    def getChildDef(self, childtable):
        return self.childtables[childtable]


class dbAppDef:
    """
        Application definition.
    """
    def __init__(self, sql):
        self.tables={}
        self.relations={}
        self.objects={}
        self.fieldDefaults={}
        self.sql = sql

    
    def reconnect(self, host, user, database, password):
        self.sql=dbSql(host=host,
                       user=user,
                       database=database,
                       password=password,
                       app=self)

    
    def getLabel(self, tableName):
        try:
            return self.objects.get(tableName, tableName).label
        except:
            return tableName


    def getTableDef(self, tableName):
        return self.tables[tableName]


    def getDefaultValueFor(self, key):
        return self.fieldDefaults[key]


    def createDefaultObject(self, tableName, fields=None, **args):
        """
            create a single record object of the type tableName and fill it with
            fields **args
        """
        if fields == None: fields = {}
        if self.objects.has_key(tableName):
            rec = self.objects[tableName].recObj(self)
        else:
            rec = dbRecord(self, tableName)

        for fieldName, fieldDef in self.tables[tableName].fields.items():
            #
            # No sense in filling primary keys with default values.
            #
            if fieldName==self.tables[tableName].primarykey:
                continue
            rec.setFieldValue(fieldName, fieldDef.default)
            if args.has_key(fieldName):
                rec.setFieldValue(fieldName, args[fieldName])
                continue
            if fields.has_key(fieldName):
                rec.setFieldValue(fieldName, fields[fieldName])
                continue
            if self.fieldDefaults.has_key(fieldName):
                rec.setFieldValue(fieldName, self.fieldDefaults[fieldName])
                continue
        return rec


    def createObject(self, tableName, fields=None, **args):
        """
            create a single record object of the type tableName and fill it with
            fields **args
        """
        if fields == None: fields = {}
        fields.update(args)
        
        if self.objects.has_key(tableName):
            rec = self.objects[tableName].recObj(self, fields=fields)
        else:
            rec = dbRecord(self, tableName, fields=fields)
        return rec


    def createTableObject(self, tableName):
        if self.objects.has_key(tableName):
            return self.objects[tableName].tblObj(self)
        else:
            return dbTable(self, tableName)


    def getObject(self, tableName, fields=None, **args):
        """
            retrieve a single object from the database by table name
            and argument list.
        """
        if fields <> None:
            args=fields
        rows = self.getObjects(tableName, args)
        
        if len(rows) > 0:
            return rows[0]
        
        elif len(rows) > 1:
            raise dbTooManyRowsException(tableName,
                                         self.createDefaultObject(tableName, args))
        
        else:
            raise dbRecordNotFoundException(tableName,
                                            self.createDefaultObject(tableName, args))

            
    def getObjects(self, tableName, fields=None, orderBy = None, **args):
        """
            retrieve a list of objects from the database by
            table name and argument list
        """
        if fields == None: fields = {}
        if fields != {}:
            args=fields
        rec = self.createObject(tableName, args)
        tbl = self.createTableObject(tableName)
        tbl.select(rec, orderBy = orderBy)
        if len(tbl) > 0:
            return tbl.rows
        else:
            return []


    def getObjectsByRec(self, rec, orderBy = None):
        tbl = self.createTableObject(rec.table)
        tbl.select(rec, orderBy)
        if len(tbl) > 0:
            return tbl.rows
        else:
            return []
            
    def getTableLable(self, tableName):
        if self.objects.has_key(tableName):
            return self.objects[tableName].label
        else:
            return tableName

            
    def addDef(self, **args):
        """
            Add a dictionary of table definitions to the repository.

            Usage:

            app.addDef( table1=dbTableDef(...), table2=dbTableDef(...)

        """
        for (tableName, tableDef) in args.items():
            #
            # Store tableNama/table definition
            #                
            tableDef.name=tableName
            self.tables[tableName]=tableDef
            
            #
            # updating field labels that can be calculated
            #
            for (fieldname, field) in tableDef.orderedFieldList():
                if field.label==None:
                    if fieldname[-2:]=="nr":
                        field.label=fieldname[:-2]
                    field.label=string.replace(fieldname, "_", " ")
                    field.label=field.label.capitalize()


    def toXML(self, outfile):
        """
        Create an XML file that contains the repository
        """
        out=outfile.write

        out("""<?xml version="1.0" encoding='iso-8859-1'?>\n""")
        out("<repository>\n")
        #
        # Relations
        #
        for k, v in self.relations.items():
            out("""<relation name="%s" rtable="%s" ralias="%s" \n""" \
                    % (k, v.rtable, v.ralias) )
            out("""keys_local="%s" keys_foreign="%s" \n""" \
                    % (v.keys.local, v.keys.foreign) )
            out("""descriptor_local="%s" descriptor_foreign="%s" \n """ \
                    % (v.descriptors.local, v.descriptors.foreign) )
            out("/>\n")
        #
        # Tables
        #
        for k, v in self.tables.items():
            out("""<table name="%s"
            alias="%s"
            tabletype="%s"
            comment="%s"
            sequencebase="%s"
            >\n""" % (v.name, v.alias, str(v.tabletype), v.comment, v.sequencebase))
            out("""<primarykey name="%s"/>\n""" % v.primarykey)
            for childtable, childdef in v.childtables.items():
                out("""<childtable name="%s" local="%s" foreign="%s"/>\n""" \
                        % (childtable, childdef.keys.local, childdef.keys.foreign))
            for lookuptable in v.lookuptables:
                out("""<lookuptable name="%s"/>\n""" % lookuptable)
            for fieldname, fielddef in v.fields.items():
                out("""<field """)
                for attr in dir(fielddef):
                    if attr[:2]!="__":
                        out ("""%s="%s" """ % (attr, unicode(getattr(fielddef, attr))))
                out("/>\n")
            for descriptor in v.descriptors:
                out("<tabledescriptor>%s</tabledescriptor>\n" % descriptor)
            out("<fieldorder>")
            for f in v.fieldOrder:
                out("<field>%s</field>" % f)
            out("</fieldorder>\n")
            out("<hint>%s</hint>\n" % v.hint)
            out("</table>\n")

        out("</repository>\n")
        outfile.close()


    def toSQL(self, outfile=sys.stdout):
        """
            Create or alter tables in the target database

        """
        from ddl import dbDDL
        dbddl=dbDDL(self.relations)
        
        for table, tableDef in self.tables.items():
            tableDef.name=table
            outfile.write(dbddl.getCreateTableDDL(tableDef))


    def XMLinit(self, infile):

        from repositoryparser import RepositoryParser
        parser=RepositoryParser()
        lines=infile.read()
        
        parser.feed(lines)
        parser.close()
        self.tables = parser.tables
        self.relations=parser.relations
        for table in self.tables.keys():
            if not self.objects.has_key(table):
                self.objects[table]=dbAppObj(dbRecord, dbTable, table)


            
class dbAppObj:
    def __init__(self, recObj, tblObj, label):
        self.recObj=recObj
        self.tblObj=tblObj
        self.label=label


    def __repr__(self):
        return self.label + ": " + str(self.recObj) + ", " + str(self.tblObj)


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.14 $
    Last edited          : $Date: 2002/11/16 12:36:56 $
    
***************************************************************************/
"""
