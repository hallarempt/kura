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

lexemes = kuraapp.app.getObjects("lng_lex",
                              languagenr = 1)
for lexeme in lexemes:
    elements = kuraapp.app.getObjects("lng_element",
                                      lexnr = lexeme.lexnr)
    if elements:
        print lexeme.form, lexeme.glosse
        print
        
        examples = {}
        for element in elements:
            if not examples.has_key(element.streamnr):
                stream = kuraapp.app.getObject("lng_stream",
                                               streamnr = element.streamnr)
                examples[element.streamnr] = stream
                
        for streamnr, stream in examples.items():
           
            print "\t", stream.text
            print "\t", stream.translation()
            print
        print
        print

