#!/usr/bin/env python
import string
from kuralib import lngapp

class App:

    def __init__(self):
        self.tables = {}

    def addDef(self, **args):
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


def tableType(type):
    if type == 0:
        return "numeric primary key"
    elif type ==  1:
        return "Recursive table with a numeric primary key"
    elif type == 2:
        return "Numeric primary key and a sequential counter"
    elif type == 3:
        return "Code table with a textual primary key"
    elif type == 4:
        return "System code table with a textual primary key"
    else:
        return "Unknown type"

def dataTypes(type):
    if type == 0:
        return "Integer"
    elif type == 1:
        return "String"
    elif type == 2:
        return "Text"
    elif type == 3:
        return "Boolean"
    elif type == 4:
        return "Date/time"


def buildFieldDef(fieldDef):
    if fieldDef.pk:
        return "%s, %i (pk)" % (dataTypes(fieldDef.datatype), fieldDef.length)
    elif fieldDef.sequence:
        return "%s, %i (seq)" % (dataTypes(fieldDef.datatype), fieldDef.length)
    elif fieldDef.nullable:
        return "%s, %i (null allowed)" % (dataTypes(fieldDef.datatype), fieldDef.length)
    elif not fieldDef.owner:
        return "%s, %i (lookup)" % (dataTypes(fieldDef.datatype), fieldDef.length)
    
def buildFields(tableDef):
    r = [fieldHeader]
    for field, fieldDef in tableDef.fields.items():
        r.append(fieldRow % {"field": field,
                             "definition": buildFieldDef(fieldDef)})
    r.append("</tbody></informaltable>")
    return "\n".join(r)




def buildLookupTables(table, app):
    if len(table.lookuptables) == 0:
        return ""
    r = ["""
       <refsect1><title>Lookup tables (parents)</title>
          <informaltable><tgroup cols="5">
    <thead>
    <row>
      <entry>Name</entry>
      <entry>Keypair</entry>
      <entry>Descriptors</entry>
      <entry>Related table</entry>
      <entry>Related alias</entry></row>
    <tbody>"""]
    for table in table.lookuptables:
        rel = app.relations[table]
        r.append("""     <row>
        <entry>%s</entry>
        <entry>%s</entry>
        <entry>%s</entry>
        <entry><link linkend="%s">%s</link></entry>
        <entry>%s</entry>
     </row>""" %
                 (rel.name,
                  unicode(rel.keys),
                  unicode(rel.descriptors),
                  rel.rtable, rel.rtable,
                  rel.ralias))
    r.append("""</tbody></tgroup></informaltable></refsect1>
""")
    return "\n".join(r)

def buildChildRelations(table):
    if len(table.childtables.keys()) == 0:
        return ""
    r = ["""<refsect1><title>Lookup tables (parents)</title>
   <informaltable><tgroup cols="3">
    <thead>
    <row>
      <entry>Childtable</entry>
      <entry>Local key</entry>
      <entry>Foreign key</entry>
    </row>
    <tbody>"""]
    for child in table.childtables.values():
        r.append("""     <row>
        <entry><link linkend="%s">%s</link></entry>
        <entry>%s</entry>
        <entry>%s</entry>
      </row>""" %
                 (child.childTable,
                  child.childTable,
                  child.keys.local,
                  child.keys.foreign))
    r.append("""</tbody></tgroup></informaltable>
    </refsect1>""")
    return "\n".join(r)

def main():
    app = App()
    lngapp.setRepository(app)

    keys = app.tables.keys()
    keys.sort()
    for key in keys:
        table = app.tables[key]
        print tableEntry % {"tablename": table.name,
                            "tablename": table.name,
                            "tablename": table.name,
                            "comment": table.comment,
                            "tabletype": tableType(table.tabletype),
                            "alias": table.alias,
                            "primarykey": table.primarykey,
                            "sequencebase": table.sequencebase,
                            "hint": table.hint,
                            "descriptors": ", ".join(table.descriptors),
                            "fieldorder": ", ".join(table.fieldOrder),
                            "fields": buildFields(table),
                            "indexes": ", ".join(table.indexes),
                            "uniqueIndexes": ", ".join(table.unique_indexes),
                            "childtables": buildChildRelations(table),
                            "lookuptables": buildLookupTables(table, app)}
        

fieldHeader = """
        <informaltable>
           <tgroup cols="2">
              <thead>
                 <row><entry>Fieldname</entry><entry>Field definition</entry></row>
              </thead>
              <tbody>"""

fieldRow = """<row><entry>%(field)s</entry><entry>%(definition)s</entry></row>"""


tableEntry = """<refentry id="%(tablename)s">
      <refmeta>
        <refentrytitle>%(tablename)s</refentrytitle>
      </refmeta>
      <refnamediv>
        <refname>%(tablename)s</refname>
        <refpurpose>%(comment)s</refpurpose>
      </refnamediv>
      <refsect1>
        <title>Attributes</title>

        <informaltable>
          <tgroup cols="2">
            <tbody>
              <row>
                <entry>Table type</entry>
                <entry>%(tabletype)s</entry>
              </row>
              <row>
                <entry>Table alias</entry>
                <entry>%(alias)s</entry>
              </row>
              <row>
                <entry>Primary key field</entry>
                <entry>%(primarykey)s</entry>
              </row>
              <row>
                <entry>Sequence field</entry>
                <entry>%(sequencebase)s</entry>
              </row>
              <row>
                <entry>Hint</entry>
                <entry>%(hint)s</entry>
              </row>
              <row>
                <entry>Table described by</entry>
                <entry>%(descriptors)s</entry>
              </row>
              <row>
                <entry>Fieldorder</entry>
                <entry>%(fieldorder)s</entry>
              </row>
              <row>
                <entry>Indexes</entry>
                <entry>%(indexes)s</entry>
              </row>
              <row>
                <entry>Unique Indexes</entry>
                <entry>%(uniqueIndexes)s</entry>
              </row>
              
           </tbody>
          </tgroup>
        </informaltable>

      <refsect1><title>Fields</title>
        %(fields)s
      </refsect1>
      %(childtables)s
      %(lookuptables)s
    </refentry>
"""


if __name__ == "__main__":
    main()
