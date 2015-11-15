# $Id: Makefile,v 1.8 2003/03/02 22:55:43 boud Exp $

.PHONY:	clean dbtest libtest dialogs distr manual

manual:
	cd doc; db2ps manual.sgml && ps2pdf manual.ps
dialogs:
	cd dialogs; ./convert.py
clean:
	find . -name \*pyc -or -name \*pyo -or -name \*~ -or -name \*flc | xargs rm

dbtest:
	cd dbobj; ./unittests.py

libtest:
	cd kuralib; ./unittests.py

distr: 
	/usr/bin/python setup.py sdist; /usr/bin/python setup.py bdist_rpm; cp dist/* ~/public_html

#
# $Log: Makefile,v $
# Revision 1.8  2003/03/02 22:55:43  boud
# *** empty log message ***
#
# Revision 1.7  2003/01/03 21:28:50  boud
# Added a dynamic menu with abbreviations, bumped up minor version number
#
# Revision 1.6  2002/11/09 14:54:33  boud
# Added manual target, fixed lots of small bugs, added text to manual.
#
# Revision 1.5  2002/11/06 21:28:36  boud
# Added manual
#
# Revision 1.4  2002/07/30 11:34:37  boud
# Fixes, fixes, fixes...
#
# Revision 1.3  2002/05/22 18:52:17  boud
# login works again. More or less.
#
# Revision 1.2  2002/05/20 21:12:32  boud
# Done for tonight: now I need designer.
#
# Revision 1.1  2002/05/20 19:34:06  boud
# Added makefile
#
#
