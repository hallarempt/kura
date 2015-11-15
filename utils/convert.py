from os import path, environ
import codecs, sys, os

sys.setappdefaultencoding("utf-8")

True = 1
False = 0

from kuragui.guiconfig import guiConf
from dbobj.textdb import textquery

from kuralib import kuraapp

kuraapp.initApp("dbSql",
		username = str(guiConf.username),
                database = sys.argv[1],
                password = str(guiConf.password),
                hostname = str(guiConf.hostname))
  
kuraapp.initCurrentEnvironment(1,1,1)

textdb = textquery.TextQuery(kuraapp.app, sys.argv[v])

for table, tabledef in kuraapp.app.tables.items():
    print "Converting", table
    records = kuraapp.app.getObjects(table)
    for r in records:
        textdb.insert(table, r, False)

textdb.saveDatabase()

