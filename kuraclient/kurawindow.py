""" Main window for Kura """

import codecs, os, os.path
from qt import *

True = 1
False = 0

from kuragui.guiconfig import guiConf, writeConfig
from kuragui import guiconfig
from kuragui import guiaction
from kuragui.guitable import GuiTable
from kuragui.guilistview import guiListView
from kuragui.comboproxy import ComboProxy
from kuralib import kuraapp
import resource

from kuratextlistview import KuraTextListView
from kurastatusbar import KuraStatusBar
import frmlogin;
import dlgpreferences;

def Icon(pixmap):
    """ Utilty function to create an icon from a pixmap."""
    return QIconSet(QPixmap(os.path.join(os.environ["KURADIR"], "pixmaps", pixmap)))

class LanguageSelector(QComboBox):
    """A combobox used to determine the current language."""
    
    def __init__(self, *args):
        QComboBox.__init__(self, *args)
        self.setEditable(False)
        self.cmbproxy = ComboProxy(self, kuraapp.app.getObjects("lng_language"),
                                   guiConf.languagenr, True)


    def reset(self):
        self.clear()
        self.cmbproxy = ComboProxy(self, kuraapp.app.getObjects("lng_language"),
                                   guiConf.languagenr, True)

    def currentLanguagenr(self):
        r =  self.cmbproxy.currentKey()
        if r == None:
            return None
        else:
            return r
    
class KuraWindow(QMainWindow):
    """The main window of the Kura application."""
    
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
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
                    QMessageBox.critical(self,
                                         "Kura",
                                         "Error connecting to database: %s" % e)
        kuraapp.initCurrentEnvironment(guiConf.usernr,
                                       guiConf.languagenr,
                                       guiConf.projectnr)
        self.windows = []
        self.__actions = {}
        
        self.initActions()
        self.initDataDependentActions()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
    
        self.view = None
        self.initView()
        try:
            QApplication.splash.close()
        except:
            pass
    
    def initMenuBar(self):
        self.file_menu = QPopupMenu()
        self.__actions["FILE_NEW_WINDOW"].addTo(self.file_menu)
        self.file_menu.insertSeparator()
        self.__actions["FILE_NEW"].addTo(self.file_menu)
        self.__actions["FILE_OPEN"].addTo(self.file_menu)
        self.__actions["FILE_SAVE"].addTo(self.file_menu)
        self.__actions["FILE_SAVE_AS"].addTo(self.file_menu)
        self.file_menu.insertSeparator()
        self.__actions["FILE_EXPORT"].addTo(self.file_menu)
        self.file_menu.insertSeparator()
        self.__actions["FILE_CONNECT"].addTo(self.file_menu)
        self.file_menu.insertSeparator()
        self.__actions["OPTIONS_PREFERENCES"].addTo(self.file_menu)
        self.file_menu.insertSeparator()
        self.__actions["FILE_QUIT"].addTo(self.file_menu)

        # menuBar entry self.edit_menu
        self.edit_menu = QPopupMenu()
        self.__actions["EDIT_NEW"].addTo(self.edit_menu)
        self.__actions["EDIT_FIND"].addTo(self.edit_menu)
        self.__actions["EDIT_OPEN"].addTo(self.edit_menu)
        self.__actions["EDIT_DELETE"].addTo(self.edit_menu)

        # menuBar entry self.view_menu
        self.view_menu = QPopupMenu()
        self.__actions["lng_lex"].addTo(self.view_menu)
        self.__actions["lng_recording"].addTo(self.view_menu)
        self.__actions["lng_scan"].addTo(self.view_menu)
        self.__actions["lng_text"].addTo(self.view_menu)
        self.__actions["lng_reference"].addTo(self.view_menu)
        
        self.admin_menu = QPopupMenu()
        self.__actions["lng_project"].addTo(self.admin_menu)
        self.__actions["lng_language"].addTo(self.admin_menu)
        self.__actions["lng_user"].addTo(self.admin_menu)
        self.__actions["lng_affiliationcode"].addTo(self.admin_menu)
        self.__actions["lng_document"].addTo(self.admin_menu)
        
        self.configuration_menu = QPopupMenu()
        self.__actions["lng_tag"].addTo(self.configuration_menu)
        self.__actions["lng_tagtypecode"].addTo(self.configuration_menu)
        self.__actions["lng_tagdomain"].addTo(self.configuration_menu)
        self.__actions["lng_lxlxrelcode"].addTo(self.configuration_menu)    
        self.__actions["lng_elementtypecode"].addTo(self.configuration_menu)
        self.__actions["lng_categorycode"].addTo(self.configuration_menu)

        self.abbrevs_menu = QPopupMenu()
        rows = kuraapp.app.getObjects("lng_tag", tagtypecode="DABBR")
        for row in rows:
            self.__actions["lng_tagdomain$tag=%s" % row.tag].addTo(self.abbrevs_menu)
            
        self.menuBar().insertItem("&File", self.file_menu)
        self.menuBar().insertItem("&Edit", self.edit_menu)
        self.menuBar().insertItem("&Documents", self.view_menu)
        self.menuBar().insertItem("&Abbreviations", self.abbrevs_menu)
        self.menuBar().insertItem("a&Dministration", self.admin_menu)
        self.menuBar().insertItem("&Configuration", self.configuration_menu)
        
        self.help = QPopupMenu(self)
        self.menuBar().insertSeparator()
        self.menuBar().insertItem('&Help', self.help)
        
        self.help.insertItem('&About', self.slotAbout)
        self.help.insertItem('About &Qt', self.aboutQt)

        
    def initToolBar(self):
        self.toolBar = QToolBar(self,'Main')
        self.buttons = []
        self.__actions["FILE_NEW"].addTo(self.toolBar)
        self.__actions["FILE_OPEN"].addTo(self.toolBar)
        self.__actions["FILE_SAVE"].addTo(self.toolBar)
        self.__actions["FILE_SAVE_AS"].addTo(self.toolBar)
        self.toolBar.addSeparator()
        self.__actions["FILE_EXPORT"].addTo(self.toolBar)
        self.toolBar.addSeparator()
        self.__actions["EDIT_NEW"].addTo(self.toolBar)
        self.__actions["EDIT_FIND"].addTo(self.toolBar)
        self.__actions["EDIT_OPEN"].addTo(self.toolBar)
        self.__actions["EDIT_DELETE"].addTo(self.toolBar)
        self.toolBar.addSeparator()
        self.lblLanguage = QLabel("Current language:", self.toolBar)
        self.cmbLanguage = LanguageSelector(self.toolBar)
        self.connect(self.cmbLanguage, SIGNAL("activated(int)"),
                     self.slotLanguageChanged)
        QWhatsThis.add(self.cmbLanguage, "Select a new default language.")
        
        self.toolBar.addSeparator()
        self.__actions["FILE_QUIT"].addTo(self.toolBar)

        
    def initStatusBar(self):
        self.statusBar = KuraStatusBar(self)


    def initView(self):
        if kuraapp.app.initialized and guiConf.currentTableName != "":
            self.openView(guiConf.currentTableName)
        else:
            w = QWidget(self)
            self.setCentralWidget(w)
            w.show
            self.setCaption("Kura 2.0")


    def __parseTableName(self, tableName):
        if tableName.find("$") == -1:
            return tableName, {}
        else:
            fields = {}
            tablename, fieldstring = tableName.split("$")
            for field in fieldstring.split(","):
                k, v = field.split("=")
                fields[k]=v
            return tablename, fields
            
    def openView(self, tableName, searchRec = None):
        guiConf.currentTableName = tableName        
        if self.view != None:
            self.view.close()
        
        if searchRec == None:
            tableName, fields = self.__parseTableName(tableName)
            searchRec = kuraapp.app.createObject(tableName, fields=fields)
            
            if guiConf.useDefaultForSearch:
                f = searchRec.getFields()
                if tableName != "lng_language" and f.has_key("languagenr"):
                    searchRec.setFieldValue("languagenr", guiConf.languagenr)
                if tableName != "lng_user" and f.has_key("usernr"):
                    searchRec.setFieldValue("usernr", guiConf.usernr)
                if tableName != "lng_project" and f.has_key("projectnr"):
                    searchRec.setFieldValue("projectnr", guiConf.projectnr)                    
                


        if tableName == "lng_text":
            self.view = KuraTextListView(parent = self,
                                         searchRec = searchRec)
        else:
            self.view=guiListView(app = kuraapp.app,
                                  tableName = tableName,
                                  searchRec = searchRec,
                                  dlgForm = self.__actions[tableName].dlgForm,
                                  dlgSearch = self.__actions[tableName].dlgSearch,
                                  parent = self)
   
       
            #dlgForm = self.__actions[tableName].dlgForm,
            #dlgSearch = self.__actions[tableName].dlgSearch,

            #self.view = GuiTable(self, dlgSearch, dlgForm)
            #self.view.refresh(searchRec)

            
        self.setCentralWidget(self.view)
        self.view.show()
        self.view.setFocus()
        self.setCaption("Kura: " +  kuraapp.app.getTableLable(tableName) )

    
    def enableCommand(self, action):
        self.__actions[action].setEnabled(True)


    def disableCommand(self, action):
        self.__actions[action].setEnabled(False)

    
    #
    # Events
    #     

    def closeEvent(self, e):
        if guiConf.backend == guiconfig.FILE:
            self.querySave()
        if self.view:
            self.view.close()
        guiConf.app_x = self.x()
        guiConf.app_y = self.y()
        guiConf.app_w = self.width()
        guiConf.app_h = self.height()
        writeConfig()
        e.accept()
  
    #
    # SLOT IMPLEMENTATION
    #

    def slotAbout(self):
        QMessageBox.about(self, 'Kura, the linguistics database',
                          resource.ABOUT % resource.VERSION)    

    def aboutQt(self):
        QMessageBox.aboutQt(self, 'Kura, the linguistics database.')


    def querySave(self):
        if kuraapp.app.isDirty():
            save = QMessageBox.warning(self, "Unsaved data",
                                       "Do you want to save your changes?",
                                       QMessageBox.Yes,
                                       QMessageBox.No,
                                       QMessageBox.NoButton)
            if save == QMessageBox.Yes:
                kuraapp.app.saveFile()

    def enterFileMode(self, fileName):
        (guiConf.filepath, guiConf.datastore) = os.path.split(fileName)
        self.setCaption("Kura " + fileName)
        guiConf.backend = guiconfig.FILE
        self.enableCommand("FILE_SAVE_AS")
        self.enableCommand("FILE_SAVE")
        self.statusBar.reset()
        self.initView()
        self.cmbLanguage.reset()

    def enterDatabaseMode(self):
        guiConf.backend = guiconfig.SQL
        self.disableCommand("FILE_SAVE_AS")
        self.disableCommand("FILE_SAVE")
        self.statusBar.reset()
        self.initView()
        self.cmbLanguage.reset()
        
    def slotFileNewWindow(self):
        window = KuraWindow()
        self.windows.append(window)
        window.show()

 
    def slotFileNew(self):
        if guiConf.backend == guiconfig.FILE:
            self.querySave()
        fileName = QFileDialog.getSaveFileName(guiConf.filepath,
                                               "datastores (*.dbobj)",
                                               self,
                                               "new file dialog",
                                               "Create a new Kura datastore")
        if not fileName.isEmpty():
            template = os.path.join(os.environ['KURADIR'],
                                    resource.TEMPLATE_FILE)

            if not os.path.exists(template):
                QMessageBox.critical(self, "No template", resource.TEMPLATE_FAILURE % template)

            if os.path.exists(unicode(fileName)):
                if QMessageBox.critical(self, "File already exists",
                                        "Do you want to overwrite %s?" % unicode(fileName),
                                        QMessageBox.Yes,
                                        QMessageBox.No,
                                        QMessageBox.NoButton) == QMessageBox.No:
                    return

            kuraapp.app.openFile(template)
            kuraapp.app.saveFile(unicode(fileName))
            self.enterFileMode(unicode(fileName))
            

    def slotFileOpen(self):
        if guiConf.backend == guiconfig.FILE:
            if kuraapp.app.isDirty():
                save = QMessageBox.warning(self, "Unsaved data",
                                           "Do you want to save your changes?",
                                           QMessageBox.Yes,
                                           QMessageBox.No,
                                           QMessageBox.NoButton)
                if save == QMessageBox.Yes:
                    kuraapp.app.saveFile()

        fileName = QFileDialog.getOpenFileName(guiConf.filepath,
                                               "datastores (*.dbobj)",
                                               self,
                                               "open file dialog",
                                               "Open a datastore")
        if not fileName.isEmpty():
            kuraapp.app.openFile(unicode(fileName))
            self.enterFileMode(unicode(fileName))
            
    def slotFileSave(self):
        if guiConf.backend == guiconfig.FILE:
            if kuraapp.app.isDirty():
                kuraapp.app.saveFile()
                self.statusBar.message("Datastore succesfully saved", 2000)


    def slotFileSaveAs(self):
        fileName = QFileDialog.getSaveFileName(guiConf.filepath,
                                               "datastores (*.dbobj)",
                                               self,
                                               "save as file dialog",
                                               "Save current datastore under a new name.")
        if not fileName.isEmpty():
            fileName = unicode(fileName)
            if os.path.exists(fileName):
                if QMessageBox.critical(self, "File already exists",
                                        "Do you want to overwrite %s?" % fileName,
                                        QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton) \
                                        == QMessageBox.No:
                    return

            (guiConf.filepath, guiConf.datastore) = os.path.split(fileName)
            guiConf.backend = guiconfig.FILE
            kuraapp.app.saveFile(fileName)
            self.statusBar.message("Datastore succesfully saved to %s" % fileName, 2000)
            
            

    def slotFileExport(self):
        fileName = QFileDialog.getSaveFileName(guiConf.filepath,
                                               "Export formats (*.xml *.sgml *.dbx)",
                                               self,
                                               "export file dialog",
                                               "Export current selection")
        if not fileName.isEmpty():
            fileName = unicode(fileName)
            if os.path.exists(fileName):
                if QMessageBox.critical(self, "File already exists",
                                        "Do you want to overwrite %s?" % fileName,
                                        QMessageBox.Yes,
                                        QMessageBox.No,
                                        QMessageBox.NoButton) == QMessageBox.No:
                    return
                
            (p, filetype) = os.path.splitext(fileName)
            
            if filetype in [".xml", ".sgml", ".dbx"]:
                exportformat = "docbook"
            elif filetype in [".txt",".ut8"]:
                exportformat = "text"
            else:
                exportformat = "xml"
                        
            table = kuraapp.app.createTableObject(guiConf.currentTableName)
            query = self.view.getCurrentQuery()
            try:
                f = codecs.open(fileName, "w+", "utf-8")
                f.write((table.export(query, exportformat, guiConf.interlinearstyle)));
                self.statusBar.message("Selection succesfully exported to %s." % fileName, 2000)
            except NotImplementedError, error:
                QMessageBox.critical(self, "Export error",unicode(error))
                    
    def slotFilePrint(self):
        printer = QPrinter()
        if printer.setup(self) == True:
            self.view.printView(printer)

    def slotConnect(self):
        if guiConf.backend == guiconfig.FILE:
            self.querySave()
            
        d = frmlogin.frmLogin(parent = self, modal = True)

        d.txtUsername.setText(guiConf.username)
        d.txtPassword.setText(guiConf.password)
        d.txtDatabase.setText(guiConf.database)
        d.txtHost.setText(guiConf.hostname)
        
        # intentionally modal
        if d.exec_loop() == 1: # accepted
            
            username = unicode(d.txtUsername.text())
            password = unicode(d.txtPassword.text())
            database = unicode(d.txtDatabase.text())
            hostname = unicode(d.txtHost.text())
            
            if username <> guiConf.username or password <> guiConf.password or \
                   database <> guiConf.database or hostname <> guiConf.hostname or \
                   guiConf.backend == guiconfig.FILE:
                guiConf.username = username
                guiConf.password = password
                guiConf.database = database
                guiConf.hostname = hostname
                try:
                    if not kuraapp.app.initialized:
                        kuraapp.initApp(guiConf.backend,
                                        username = str(guiConf.username),
                                        database = str(guiConf.database),
                                        password = str(guiConf.password),
                                        hostname = str(guiConf.hostname))
                    else:
                        kuraapp.app.reconnect(hostname, username, database, password)
                except Exception, error:
                    QMessageBox.critical(self, "Database error",unicode(error))

                self.statusBar.reset()
                self.enterDatabaseMode()
                
                
    def slotFileQuit(self):
        self.close()


    def slotEditNew(self):
        self.view.new()


    def slotEditOpen(self):
        self.view.open()


    def slotEditDelete(self):
        self.view.delete()

    
    def slotEditFind(self):
        self.view.find()


    def slotLanguageChanged(self):
        guiConf.languagenr = self.cmbLanguage.currentLanguagenr()
        kuraapp.app.settings(usernr = guiConf.usernr,
                             languagenr = guiConf.languagenr,
                             projectnr = guiConf.projectnr)
        self.initView()

        
    def slotPreferences(self):
        d = dlgpreferences.dlgPreferences(parent=self)
        # intentionally modal
        if d.exec_loop() == 1: # accepted
            # save in Config object
            d.savePreferences()
            self.statusBar.reset()

    def initDataDependentActions(self):
        rows = kuraapp.app.getObjects("lng_tag", tagtypecode="DABBR")
        for row in rows:
            action = guiaction.guiAction(self)
            action.setMenuText(row.description)
            action.setName("lng_tagdomain$tag=%s" % row.tag)
            action.setToolTip("Open the domain entries for the tag %s." % row.description)
            QObject.connect(action, PYSIGNAL("activatedName"), self.openView)
            self.__actions["lng_tagdomain$tag=%s" % row.tag]=action
        
    def initActions(self):
        #
        # Create actions
        #
        guiAction = guiaction.guiAction
        self.__actions["EDIT_OPEN"] = guiAction(self, "CTRL+ALT+O")
        self.__actions["EDIT_NEW"] = guiAction(self, "CTRL+ALT+N")
        self.__actions["EDIT_DELETE"] = guiAction(self, "DEL")
        self.__actions["EDIT_FIND"] = guiAction(self, "CTRL+F")
        self.__actions["FILE_CLOSE"] = guiAction(self, "CTRL+W")
        self.__actions["FILE_CONNECT"] = guiAction(self)
        self.__actions["FILE_NEW"] = guiAction(self, "CTRL+N")
        self.__actions["FILE_NEW_WINDOW"] = guiAction(self)
        self.__actions["FILE_OPEN"] = guiAction(self, "CTRL+O")
        self.__actions["FILE_PRINT"] = guiAction(self, "CTRL+P")
        self.__actions["FILE_QUIT"] = guiAction(self)
        self.__actions["FILE_SAVE"] = guiAction(self, "CTRL+S")
        self.__actions["FILE_SAVE_AS"] = guiAction(self)
        self.__actions["FILE_EXPORT"] = guiAction(self)
        self.__actions["lng_affiliationcode"] = guiAction(self)
        self.__actions["lng_document"] = guiAction(self)
        self.__actions["lng_language"] = guiAction(self)
        self.__actions["lng_linkcode"] = guiAction(self)
        self.__actions["lng_lxlxrelcode"] = guiAction(self)
        self.__actions["OPTIONS_PREFERENCES"] = guiAction(self)
        self.__actions["lng_project"] = guiAction(self)
        self.__actions["lng_categorycode"] = guiAction(self)
        self.__actions["lng_reference"] = guiAction(self)
        self.__actions["lng_tag"] = guiAction(self)
        self.__actions["lng_tagdomain"] = guiAction(self)
        self.__actions["lng_tagtypecode"] = guiAction(self)
        self.__actions["lng_elementtypecode"] = guiAction(self)
        self.__actions["lng_user"] = guiAction(self)
        self.__actions["lng_lex"] = guiAction(self)
        self.__actions["lng_recording"] = guiAction(self)
        self.__actions["lng_scan"] = guiAction(self)
        self.__actions["lng_text"] = guiAction(self)

        #
        # Set the (table)name for the activatedName pysignal
        #    
        for name, action in self.__actions.items():
          action.setName(name)
        #
        # Set menu texts
        #
        self.__actions["EDIT_NEW"].setMenuText("&New item")
        self.__actions["EDIT_OPEN"].setMenuText("&Open item")
        self.__actions["EDIT_DELETE"].setMenuText("&Delete")
        self.__actions["EDIT_FIND"].setMenuText("&Find")
        self.__actions["FILE_CONNECT"].setMenuText("&Connect...")
        self.__actions["FILE_NEW"].setMenuText("&New...")
        self.__actions["FILE_NEW_WINDOW"].setMenuText("New &Window")
        self.__actions["FILE_OPEN"].setMenuText("&Open...")
        self.__actions["FILE_PRINT"].setMenuText("&Print...")
        self.__actions["FILE_QUIT"].setMenuText("&Quit")
        self.__actions["FILE_SAVE"].setMenuText("&Save")
        self.__actions["FILE_SAVE_AS"].setMenuText("save &As")
        self.__actions["FILE_EXPORT"].setMenuText("&Export as")
        self.__actions["OPTIONS_PREFERENCES"].setMenuText("Preferences...")
        self.__actions["lng_affiliationcode"].setMenuText("Affiliation&s")
        self.__actions["lng_categorycode"].setMenuText("Reference Categories")
        self.__actions["lng_document"].setMenuText("&Document")
        self.__actions["lng_language"].setMenuText("&Language")
        self.__actions["lng_lex"].setMenuText("&Lexicon")
        self.__actions["lng_linkcode"].setMenuText("&Link types")
        self.__actions["lng_lxlxrelcode"].setMenuText("&Lexical relations")
        self.__actions["lng_project"].setMenuText("Pro&ject")
        self.__actions["lng_recording"].setMenuText("&Recording")
        self.__actions["lng_reference"].setMenuText("&References")
        self.__actions["lng_scan"].setMenuText("&Scan")
        self.__actions["lng_tag"].setMenuText("Ta&gs")
        self.__actions["lng_tagdomain"].setMenuText("Tag domains")
        self.__actions["lng_tagtypecode"].setMenuText("Tag categories")
        self.__actions["lng_elementtypecode"].setMenuText("Element types")
        self.__actions["lng_text"].setMenuText("&Text")
        self.__actions["lng_user"].setMenuText("&User")
        #
        # Set tooltips
        #
        self.__actions["EDIT_NEW"].setToolTip("Create a new item")
        self.__actions["EDIT_OPEN"].setToolTip("Open the selected item")
        self.__actions["EDIT_DELETE"].setToolTip("Delete the selected item")
        self.__actions["EDIT_FIND"].setToolTip("Search in ")
        self.__actions["FILE_CONNECT"].setToolTip("Connect to the Kura database")
        self.__actions["FILE_NEW"].setToolTip("Create a new Kura datafile")
        self.__actions["FILE_NEW_WINDOW"].setToolTip("Opens a new Kura window")
        self.__actions["FILE_EXPORT"].setToolTip("Exports the current selection to an external file format.")
                
        self.__actions["FILE_OPEN"].setToolTip("Open a Kura datafile")
        self.__actions["FILE_SAVE"].setToolTip("Save a Kura datafile")
        self.__actions["FILE_SAVE_AS"].setToolTip("Save a Kura datafile under a new name")
        self.__actions["FILE_PRINT"].setToolTip("Prints the current document")
        self.__actions["FILE_QUIT"].setToolTip("Quit")
        self.__actions["lng_affiliationcode"].setToolTip("Open the list of affilications")
        self.__actions["lng_document"].setToolTip("Open the list of link types")
        self.__actions["lng_language"].setToolTip("Open the list of languages")
        self.__actions["lng_linkcode"].setToolTip("Open the list of references")
        self.__actions["lng_lxlxrelcode"].setToolTip("Open the list of lexical relation types")
        self.__actions["OPTIONS_PREFERENCES"].setToolTip("User preferences")
        self.__actions["lng_project"].setToolTip("Open the list of projects")
        self.__actions["lng_categorycode"].setToolTip("Open the list of reference categories")
        self.__actions["lng_reference"].setToolTip("Open the list of documents")
        self.__actions["lng_tag"].setToolTip("Open the list of tags")
        self.__actions["lng_tagtypecode"].setToolTip("Open the list of tag types")
        self.__actions["lng_elementtypecode"].setToolTip("Open the list of element types")
        self.__actions["lng_user"].setToolTip("Open the list of users")
        self.__actions["lng_lex"].setToolTip("Open the lexicon")
        self.__actions["lng_recording"].setToolTip("Open the list of recordings")
        self.__actions["lng_scan"].setToolTip("Open the list of scanned images")
        self.__actions["lng_text"].setToolTip("Open the list of texts")
        #
        # Set pixmaps
        #
        self.__actions["FILE_CONNECT"].setIconSet(Icon("connect_creating.png"))
        self.__actions["FILE_NEW"].setIconSet(Icon("folder_new.png"))
        self.__actions["FILE_OPEN"].setIconSet(Icon("project_open.png"))
        self.__actions["FILE_SAVE"].setIconSet(Icon("filesave.png"))
        self.__actions["FILE_SAVE_AS"].setIconSet(Icon("filesaveas.png"))
        self.__actions["FILE_PRINT"].setIconSet(Icon("fileprint.png"))
        self.__actions["FILE_QUIT"].setIconSet(Icon("fileclose.png"))
        self.__actions["FILE_EXPORT"].setIconSet(Icon("fileexport.png"))
        
        self.__actions["EDIT_NEW"].setIconSet(Icon("filenew.png"))
        self.__actions["EDIT_OPEN"].setIconSet(Icon("edit.png"))
        self.__actions["EDIT_DELETE"].setIconSet(Icon("editdelete.png"))
        self.__actions["EDIT_FIND"].setIconSet(Icon("filefind.png"))

        #
        # Set forms
        #
        from dlgtagtypecode import dlgTagTypeCode
        self.__actions["lng_tagtypecode"].setSearchForm(dlgTagTypeCode)
        self.__actions["lng_tagtypecode"].setForm(dlgTagTypeCode)

        from dlglexeme import dlgLexeme
        self.__actions["lng_lex"].setForm(dlgLexeme)

        #
        # Set slots
        #
        QObject.connect(self.__actions["FILE_NEW_WINDOW"], SIGNAL("activated()"), self.slotFileNewWindow )
        QObject.connect(self.__actions["FILE_NEW"], SIGNAL("activated()"), self.slotFileNew)
        QObject.connect(self.__actions["FILE_OPEN"], SIGNAL("activated()"), self.slotFileOpen)
        QObject.connect(self.__actions["FILE_SAVE"], SIGNAL("activated()"), self.slotFileSave)
        QObject.connect(self.__actions["FILE_SAVE_AS"], SIGNAL("activated()"), self.slotFileSaveAs)
        QObject.connect(self.__actions["FILE_EXPORT"], SIGNAL("activated()"), self.slotFileExport)
        QObject.connect(self.__actions["FILE_PRINT"], SIGNAL("activated()"), self.slotFilePrint)
        QObject.connect(self.__actions["FILE_CONNECT"], SIGNAL("activated()"), self.slotConnect)
        QObject.connect(self.__actions["FILE_QUIT"], SIGNAL("activated()"), self.slotFileQuit)
        QObject.connect(self.__actions["EDIT_OPEN"], SIGNAL("activated()"), self.slotEditOpen)
        QObject.connect(self.__actions["EDIT_NEW"], SIGNAL("activated()"), self.slotEditNew)
        QObject.connect(self.__actions["EDIT_DELETE"], SIGNAL("activated()"), self.slotEditDelete)
        QObject.connect(self.__actions["EDIT_FIND"], SIGNAL("activated()"), self.slotEditFind)
        QObject.connect(self.__actions["lng_lex"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_recording"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_scan"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_text"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_project"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_language"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_user"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_document"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_lxlxrelcode"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_linkcode"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_reference"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_categorycode"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_tag"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_tagtypecode"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_elementtypecode"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_tagdomain"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["lng_affiliationcode"], PYSIGNAL("activatedName"), self.openView)
        QObject.connect(self.__actions["OPTIONS_PREFERENCES"], SIGNAL("activated()"), self.slotPreferences)


__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.35 $"""[11:-2]
