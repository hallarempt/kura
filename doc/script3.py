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

for text in kuraapp.app.getObjects("lng_text"):
    print
    print text.title
    print
    print text.description
    print
    for stream in text.getStreams():
        print
        print stream.getInterlinearLines(stream.getElements())
        print stream.translation()
