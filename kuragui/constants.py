# table types

# First three were 0 -- was that right?

PKNR = 0   # table with a numeric primary key
SEQ = 1    # table with a numeric primary key and a sequential counter
CODE = 2   # code table with a varchar primary key
SYSTEM = 3 # system code table with a varchar primary key
LINK = 4   # many-to-many link table with a primary key that consists
           # of the primary keys of the linked tables


# datatypes

INTEGER  = 0
VARCHAR  = 1
TEXT     = 2
BOOLEAN  = 3
DATETIME = 4
DATE     = 5

# widgettypes

LINEEDIT  = 0
MULTILINE = 1
COMBOBOX  = 2

# config

USERNR = 2

# modes

INSERT = 0
UPDATE = 1
DELETE = 2
SEARCH = 4

# form types

MASTER = 0
DETAIL = 1

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.2 $"""[11:-2]

__cvslog__="""
    $Log: constants.py,v $
    Revision 1.2  2002/05/23 18:31:16  boud
    Converted some dialogs.

 ***************************************************************************/
"""
