TRUE = True =1
FALSE = False = 0

STYLE_LIST=["Platinum", "Motif", "Motif+", "SGI", "CDE", "Windows"]
SEPARATOR_MAP={"dash":"-", "space":" ", "dot":"."}

ABOUT = """Kura is a database for linguistic data: texts, recordings,
manuscripts, lexical item, grammatical data and etymological
relations. The data can be edited in this application and presented
on the web using the Kuraserver.
                          
Version %s
                          
(c) 1999, 2000. Boudewijn Rempt
"""

TEMPLATE_FAILURE = """Could not open template %s.
Check your installation of Kura. Possibly the
environment variable KURADIR is not set correctly.

Your name datastore will be completely empty."""

TEMPLATE_FILE = "template.dbobj"

VERSION="2.00 Beta 2"


__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.3 $
    Last edited          : $Date: 2002/10/28 21:34:17 $
    
    CVS Log:         
    $Log: resource.py,v $
    Revision 1.3  2002/10/28 21:34:17  boud
    Opening, saving, renaming files and connecting to databases
    implemented

    Revision 1.2  2002/09/07 11:53:13  boud
    Fixed busy-cursor bug.

    Revision 1.1.1.1  2002/03/27 23:48:32  boud
    Kura for Qt 3

    Revision 1.2  2002/01/22 21:03:47  boud
    Manu changes.

    Revision 1.9  2001/05/15 20:00:58  boud
    Version 1.0.1

    Revision 1.8  2001/01/08 20:55:06  boud
    Cleanup for version 1.0

 ***************************************************************************/
"""
