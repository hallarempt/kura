False = 0
True = 1

import os.path, sys
from kuralib import kuraapp
from kuragui.guiconfig import guiConf
from kuragui import guiconfig

if guiConf.backend == guiconfig.FILE:
    kuraapp.initApp(guiConf.backend,
                    dbfile = os.path.join(guiConf.filepath, guiConf.datastore))
elif guiConf.backend == guiconfig.SQL:
    if guiConf.username != "":
        try:
            kuraapp.initApp(guiConf.backend,
                            username = str(guiConf.username),
                            database = str(guiConf.database),
                            password = str(guiConf.password),
                            hostname = str(guiConf.hostname))
            
        except Exception, e:
            print "Error connecting to database: %s" % e
            sys.exit(1)
            
kuraapp.initCurrentEnvironment(guiConf.usernr,
                               guiConf.languagenr,
                               guiConf.projectnr)


orders = {}

for stream in kuraapp.app.getObjects("lng_stream"):
    order = []
    for element in stream.getElements():
        tag = element.getTag(tag = "POS")
        if tag.element_tagnr:
            order.append(tag.getDescription(False))
            continue
        elif element.lexnr:
            lexeme = kuraapp.app.getObject("lng_lex",
                                      lexnr = element.lexnr)
            tag = lexeme.getTag(tag = "POS")
            if tag.lex_tagnr:
                order.append(tag.getDescription(False))
                continue
        order.append("#")

    s = " ".join(order)
    if orders.has_key(s):
        orders[s] += 1
    else:
        orders[s] = 1
    
for k, v in orders.items():
    print k, v
