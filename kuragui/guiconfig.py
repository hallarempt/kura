""" guiconfig.py

Configuration settings for the Kura GUI. Uses the Qt.QSettings class.

"""
import sys, os

from qt import QSettings, QFont

TEXT = 0
NUM = 1

ILVIEW = 0
TREEVIEW = 1
XMLVIEW = 2

FILE="TextQuery"
SQL="dbSql"

tables = [
    "lng_project",
    "lng_user",
    "lng_document",
    "lng_doc_doc",
    "lng_doc_refs",
    "lng_linkcode",
    "lng_language",
    "lng_reference",
    "lng_proj_user",
    "lng_proj_lngg",
    "lng_recording",
    "lng_scan",
    "lng_text",
    "lng_proj_text",
    "lng_stream",
    "lng_element",
    "lng_lex",
    "lng_lex_lex",
    "lng_lxlxrelcode",
    "lng_text_tag",
    "lng_stream_tag",
    "lng_element_tag",
    "lng_lex_tag",
    "lng_tag",
    "lng_tagtypecode",
    "lng_tagdomain",
    "lng_affiliationcode",
    "lng_elementtypecode",
    "lng_categorycode"]

defaults = {
    "textselectorwidth": (NUM, "/kura/lng_text/selector/width", 120),
    "interlinearstyle": (NUM, "/kura/export/interlinear", 1),
    "backend": (TEXT, "/kura/backend", FILE),
    "datastore": (TEXT, "/kura/backend/store", "new.dbobj"),
    "filepath": (TEXT, "/kura/backend/filepath", os.environ["HOME"]),
    "database" : (TEXT, "/kura/database/database", "andal"),
    "hostname" : (TEXT, "/kura/database/hostname", "localhost"),
    "password" : (TEXT, "/kura/database/password", ""),
    "username" : (TEXT, "/kura/database/username", ""),
    "usernr" : (NUM, "/kura/defaults/usernr", 0),
    "languagenr" : (NUM, "/kura/defaults/languagenr", 0),
    "projectnr" : (NUM, "/kura/defaults/projectnr", 0),
    "textfontfamily" : (TEXT, "/kura/defaults/textfont/family", "unifont"),
    "textfontsize" : (NUM, "/kura/defaults/textfont/size", 16),
    "app_w" : (NUM, "/kura/geometry/app_w", 640),
    "app_h" : (NUM, "/kura/defaults/app_h", 640),
    "app_x" : (NUM, "/kura/geometry/app_x", 0),
    "app_y" : (NUM, "/kura/geometry/app_y", 0),
    "widgetfontfamily" : (TEXT, "/kura/defaults/widgetfont/family",
                          "arial"),
    "widgetfontsize" : (NUM, "/kura/defaults/widgetfont/size", 16),
    "currentTableName" : (TEXT, "/kura/defaults/currentview/tablename",
                          "lng_lex"),
    "useDefaultForSearch" : (NUM, "/kura/defaults/usedefaultforsearch", 0),
    "ShowValueHint" : (NUM, "/kura/defaults/showvaluehint", 0),
    "streamRegExp" : (TEXT, "/kura/defaults/stream/streamRegExp",
                      "\. |\.\n|[!?\12]"),
    "elementRegExp" : (TEXT, "/kura/defaults/element/elementRegExp",
                       '=--|[ ,:;"]'),
    "morphemeRegExp" : (TEXT, "/kura/defaults/element/morphemeRegExp", "[.]")
    }


def __readAndSetEntry(key, pos, default):
    d, ok = guiConf.readNumEntry("/kura/dialog/%s/%s" % (key, pos), default)
    setattr(guiConf, unicode("%s_%s" % (key, pos)), d)
    
def initialize():

    if sys.platform[:3] == 'win':
        guiConf.insertSearchPath(QSettings.Windows, "Kura")

    for k, v in defaults.items():
        if v[0] == TEXT:
            d, ok = guiConf.readEntry(v[1], v[2])
            setattr(guiConf, unicode(k), unicode(d))
        elif v[0] == NUM:
            d, ok = guiConf.readNumEntry(v[1], v[2])
            setattr(guiConf, unicode(k), int(d))
        if not ok:
            guiConf.writeEntry(v[1], v[2])

    for t in tables:
        __readAndSetEntry(t, 'x', 30)
        __readAndSetEntry(t, 'y', 30)
        __readAndSetEntry(t, 'w', 300)
        __readAndSetEntry(t, 'h', 200)
        d, ok = guiConf.readEntry("/kura/listview/%s_width" % t, "")
        setattr(guiConf, "%s_width" % t, unicode(d))

        d, ok = guiConf.readEntry("/kura/table/%s_table_width" % t, "")
        setattr(guiConf, "%s_table_width" % t, unicode(d))

        d, ok = guiConf.readEntry("/kura/table/%s_formlist_width" % t, "")
        setattr(guiConf, "%s_formlist_width" % t, unicode(d))
        
    guiConf.textfont = QFont(guiConf.textfontfamily, guiConf.textfontsize)
    guiConf.widgetfont = QFont(guiConf.widgetfontfamily, guiConf.widgetfontsize)

def writeConfig():
    for k, v in defaults.items():
        guiConf.writeEntry(v[1], getattr(guiConf, k, v[2]))
        
    for t in tables:
        guiConf.writeEntry("/kura/dialog/%s/x" % t, getattr(guiConf, "%s_x" % t, 30))
        guiConf.writeEntry("/kura/dialog/%s/y" % t, getattr(guiConf, "%s_y" % t, 30))
        guiConf.writeEntry("/kura/dialog/%s/w" % t, getattr(guiConf, "%s_w" % t, 300))
        guiConf.writeEntry("/kura/dialog/%s/h" % t, getattr(guiConf, "%s_h" % t, 200))
        guiConf.writeEntry("/kura/listview/%s_width" % t, getattr(guiConf, "%s_width" % t, ""))
        guiConf.writeEntry("/kura/table/%s_width" % t, getattr(guiConf, "%s_table_width" % t, ""))
        guiConf.writeEntry("/kura/formlist/%s_width" % t,
                           getattr(guiConf, "%s_formlist_width" % t, ""))
        
guiConf = QSettings()
initialize()




__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.26 $"""[11:-2]

