"""
  Constants to define the db-related types
"""
# Evergreens...

TRUE  = 1
FALSE = 0


# table types

PKNR   = 0   # table with a numeric primary key
RECURS = 1   # recursive table with a numeric primary key
SEQ    = 2   # table with a numeric primary key and a sequential counter
CODE   = 3   # code table with a varchar primary key
SYSTEM = 4   # system code table with a varchar primary key

# datatypes

INTEGER  = 0
VARCHAR  = 1
TEXT     = 2
BOOLEAN  = 3
DATETIME = 4


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.2 $
    Last edited          : $Date: 2002/04/03 00:08:32 $
    
    CVS Log:
    
    $Log: dbtypes.py,v $
    Revision 1.2  2002/04/03 00:08:32  boud
    Removed circular import.

    Revision 1.1.1.1  2002/03/27 23:48:31  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:42  boud
    Manu changes.

    Revision 1.2  2001/01/08 20:55:00  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
