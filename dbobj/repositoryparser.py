"""
  Create a dbObj repository from an XML file.
"""

import xmllib, os, os.path

from appobj import *

TRUE=1
FALSE=0

def checkNone(val):
    if val == "None":
      return None
    else:
      return val


class RepositoryParser(xmllib.XMLParser): 

  def __init__(self):
    xmllib.XMLParser.__init__(self)

    self.relations={}
    self.tables={}
    self.currentTable={}
    
    self.currentdbPair={}
    
    self.currentKeys=[]
    self.inKey=FALSE
    
    self.currentDescriptors=[]
    self.inDescriptor=FALSE
    
    self.currentLookuptables=[]
    self.currentTableDescriptors=[]
    self.currentChildtables={}
    self.currentPrimaryKeys=None
    self.currentFieldOrder=[]
    self.currentFields={}
    
    self.elements={'repository':  ( self.start_repository
                                  , self.end_repository)
                   ,'relation'  : ( self.start_relation
                                  , self.end_relation)
                   ,'table': ( self.start_table
                             , self.end_table )
                   ,'lookuptable': ( self.start_lookuptable
                                   , self.end_lookuptable )
                   ,'childtable': ( self.start_childtable
                                  , self.end_childtable )                   
                   ,'primarykey': ( self.start_primarykey
                                  , self.end_primarykey )
                   ,'field': ( self.start_field
                             , self.end_field )
                   ,'tabledescriptor': ( self.start_tabledescriptor
                                       , self.end_tabledescriptor)
                  }

  def start_repository(self, attrs): pass

  def end_repository(self): pass

  def start_relation(self, attrs):

    rel=dbRelationDef( name=attrs['name']
               , keys=dbPair( attrs['keys_local']
                            , attrs['keys_foreign'])
               , descriptors=dbPair( attrs['descriptor_local']
                                   , attrs['descriptor_foreign'])
               , rtable=attrs['rtable']
               , ralias=attrs['ralias']
               )
    self.relations[rel.name]=rel
   
  def end_relation(self):
    pass

  def start_table(self, attrs):
    self.currentTable=attrs

  def end_table(self):
    self.tables[self.currentTable['name'] ] = \
     dbTableDef(tabletype=self.currentTable.get('tabletype',0)
              , alias=self.currentTable['alias']
              , primarykey=self.currentPrimaryKey
              , fields=self.currentFields
              , descriptors=self.currentTableDescriptors
              , childtables=self.currentChildtables
              , lookuptables=self.currentLookuptables
              , fieldOrder=self.currentFieldOrder
              )
    self.currentLookuptables=[]
    self.currentChildtables={}
    self.currentPrimaryKey=None
    self.currentFieldOrder=[]
    self.currentDescriptors=[]
    self.currentFields={}
    
  def start_lookuptable(self, attrs):
    self.currentLookuptables.append(attrs['name'])
    
  def end_lookuptable(self): pass

  def start_childtable(self, attrs): 
    self.currentChildtables[attrs['name']]=dbChildDef(attrs['name'],
                   dbPair(attrs['local'],
                          attrs['foreign']))
    
  def end_childtable(self): pass

  def start_primarykey(self, attrs):
    self.currentPrimaryKey=attrs['name']
    
  def end_primarykey(self): pass


  def start_field(self, attrs):
    fielddef=dbFieldDef(length = int(attrs.get("length", 255)),
                        pk = int(attrs.get("pk", 0)),
                        datatype = int(attrs.get("datatype", VARCHAR)),
                        nullable= int(attrs.get("nullable", 1)),
                        sequence = int(attrs.get("sequence", FALSE)),
                        owner = int(attrs.get("owner", TRUE)),
                        auto = int(attrs.get("auto", FALSE)),
                        default = checkNone(attrs.get("default", None)),
                        autoincrement = int(attrs.get("autoincrement", FALSE)),
                        relation = checkNone(attrs.get("relation", None)),
                        label = checkNone(attrs.get("label", None)),
                        dialog = int(attrs.get("dialog", TRUE)),
                        inList = int(attrs.get("inList", TRUE)),
                        url = int(attrs.get("url", FALSE)),
                        name = checkNone(attrs.get("name", "")),
                        comment = checkNone(attrs.get("comment", "")),
                        hint = checkNone(attrs.get("hint", "")),
                        readonly = int(attrs.get("readonly", FALSE)))
    self.currentFields[attrs['name']]=fielddef
    self.currentFieldOrder.append(attrs['name'])
        
  def end_field(self): pass

  def start_tabledescriptor(self, attrs): 
    self.currentTableDescriptors.append(attrs['name'])
    
  def end_tabledescriptor(self): pass

def main():
 parser=RepositoryParser()
 parser.feed(open("test/repository.xml").read())
 parser.close()
 print parser.tables
 print parser.relations

if __name__=="__main__":
  main()

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.6 $
    Last edited          : $Date: 2002/05/20 19:34:21 $
    
    CVS Log:         
    $Log: repositoryparser.py,v $
    Revision 1.6  2002/05/20 19:34:21  boud
    Fixed and order bug in repository parser

    Revision 1.5  2002/05/19 19:49:11  boud
    Split guitable and combobox.

    Revision 1.4  2002/05/12 18:38:22  boud
    guitable starts to wrok.

    Revision 1.3  2002/05/01 07:38:33  boud
    Started on table integration.

    Revision 1.2  2002/04/03 00:08:32  boud
    Removed circular import.

    Revision 1.1.1.1  2002/03/27 23:48:31  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:42  boud
    Manu changes.

    Revision 1.4  2001/01/24 19:18:28  boud
    Added a bit of exception handling.

    Revision 1.3  2001/01/08 20:55:00  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
