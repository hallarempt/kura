import os.path, sys, string, codecs
from kuralib import kuraapp
from kuragui.guiconfig import guiConf
from kuragui import guiconfig

False = 0
True = 1

def splitCSVLine(line):
    """Splits a CSV-formatted line into a list.
    See: http://www.colorstudy.com/software/webware/
    """
    list = []
    position = 0
    fieldStart = 0
    while 1:
        if position >= len(line):
            # This only happens when we have a trailing comma
            list.append('')
            return list
        if line[position] == '"':
            field = ""
            position = position + 1
            while 1:
                end = string.find(line, '"', position)
                if end == -1:
                    # This indicates a badly-formed CSV file, but
                    # we'll accept it anyway.
                    field = line[position:]
                    position = len(line)
                    break
                if end + 1 < len(line) and line[end + 1] == '"':
                    field = "%s%s" % (field, line[position:end + 1])
                    position = end + 2
                else:
                    field = "%s%s" % (field, line[position:end])
                    position = end + 2
                    break
        else:
            end = string.find(line, ",", position)
            if end == -1:
                list.append(line[position:end])
                return list
            field = line[position:end]
            position = end + 1
        list.append(field)
    return list


def init():
    if guiConf.backend == guiconfig.FILE:
        kuraapp.initApp(guiConf.backend,
                        dbfile = os.path.join(guiConf.filepath,
                                              guiConf.datastore))
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


def main(args):
    if len(args) < 2:
        print "Usage: python script5.py f1...fn"
        sys.exit(1)
    init()
    for line in codecs.open(args[1], "r", "UTF-8"):
        line = splitCSVLine(line)
        print "Inserting %s" % line[0]
        lexeme = kuraapp.app.createObject("lng_lex", fields={},
                                          form = line[0],
                                          glosse = line[1],
                                          languagenr = guiConf.languagenr,
                                          phonetic_form = line[3],
                                          usernr = guiConf.usernr)
        lexeme.insert()
        tag = kuraapp.app.createObject("lng_lex_tag", fields={},
                                       lexnr = lexeme.lexnr,
                                       tag = "POS",
                                       value = line[2],
                                       usernr = guiConf.usernr)
        tag.insert()
        tag = kuraapp.app.createObject("lng_lex_tag",
                                       lexnr = lexeme.lexnr,
                                       tag = "FILE",
                                       value = args[1],
                                       usernr = guiConf.usernr)
        tag.insert()
    kuraapp.app.saveFile()
if __name__ == "__main__":
    main(sys.argv)
