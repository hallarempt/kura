"""
 Repository Definition
"""
from dbobj.appobj  import *
from dbobj.dbtypes import *

#
# Couple of easy macros - typing is a tiresome business...
#

def PK(relation=None): # primary key
    return dbFieldDef( length=10
                   , pk=TRUE
                   , datatype=INTEGER
                   , autoincrement=TRUE
                   , nullable=FALSE
                   , relation=relation
                   , inList=FALSE
                   , dialog=TRUE
                   , readonly=TRUE
                   )

def SQ(label=None, dialog=TRUE, inList=TRUE, readonly=TRUE): # sequence number
    return dbFieldDef( length=10
                   , datatype=INTEGER
                   , nullable=FALSE
                   , sequence=TRUE
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , readonly=readonly
                   )
#
# Foreign keys not in the listviews
#  
def FK(relation,label=None, dialog=TRUE, inList=FALSE, readonly=FALSE): # foreign key
    return dbFieldDef( length=10
                   , datatype=INTEGER
                   , nullable=FALSE
                   , relation=relation
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , readonly=readonly
                   )

def OK(relation,label=None, dialog=TRUE, inList=FALSE, readonly=FALSE, default=None): # optional foreign key
    return dbFieldDef( length=10
                   , datatype=INTEGER
                   , nullable=TRUE
                   , relation=relation
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , readonly=readonly
                   , default=default
                   )

def FC(relation, length=255,label=None, dialog=TRUE, inList=FALSE, readonly=FALSE): # foreign key to a code
    return dbFieldDef( relation=relation
                   , length=length
                   , nullable=FALSE
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , readonly=readonly
                   )

def OC(relation, length=255,label=None, dialog=TRUE, inList=FALSE, readonly=FALSE): # optional foreign key to a code
  return dbFieldDef( relation=relation
                   , length=length
                   , nullable=TRUE
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , readonly=readonly
                   )

def NN(datatype=VARCHAR, length=255,label=None, dialog=TRUE, inList=TRUE, readonly=FALSE): # not nullable
    return dbFieldDef( nullable=FALSE
                   , datatype=datatype
                   , length=length
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , readonly=readonly
                   )
  
def NO(label=None, inList=TRUE, dialog=FALSE, readonly=TRUE): # not owner
    return dbFieldDef( owner=FALSE
                   , inList=inList
                   , dialog=dialog
                   , label=label
                   , readonly=readonly
                   )

def DS(): # datestamp
    return dbFieldDef(label=None
      , inList=FALSE
      , dialog=FALSE
      , auto=TRUE
      , datatype=DATETIME
      , readonly=TRUE
      )

def FL( length = 255
      , pk=FALSE
      , datatype = VARCHAR
      , nullable=TRUE
      , sequence=FALSE
      , owner=TRUE
      , auto=FALSE
      , autoincrement=FALSE
      , relation=None
      , label=None
      , dialog=TRUE
      , inList=TRUE
      , default=None
      , readonly=FALSE
      ): # plain field
    return dbFieldDef( length = length
                   , pk = pk
                   , datatype = datatype
                   , nullable=nullable
                   , sequence=FALSE
                   , owner=owner
                   , auto=auto
                   , autoincrement=autoincrement
                   , relation=relation
                   , label=label
                   , dialog=dialog
                   , inList=inList
                   , default=default
                   , readonly=readonly
                   )


def setRepository(self):

    #
    # Foreign key relations (used to mimic referential integrity and views on
    #   platforms like MySQL, and to provide picklists)
    #
    self.relations={ "proj_doc": dbRelationDef(name="proj_doc"
                                     , keys=dbPair("documentroot", "documentnr")
                                     , descriptors=dbPair("title", "title")
                                     , rtable="lng_document"
                                     , ralias="doc"
                                     )
                   , "user_affc": dbRelationDef(name="user_affc"
                                     , keys=dbPair("affiliationcode", "affiliationcode")
                                     , descriptors=dbPair("affiliation", "description")
                                     , rtable="lng_affiliationcode"
                                     , ralias="affc"
                                     )
                   , "lngg_lngg": dbRelationDef(name="lngg_lngg"
                                     , keys=dbPair("parent_languagenr", "languagenr")
                                     , descriptors=dbPair("parent_language", "language")
                                     , rtable="lng_language"
                                     , ralias="lngg2"
                                     )
                   , "lngg_doc": dbRelationDef(name="lngg_doc"
                                     , keys=dbPair("documentroot", "documentnr")
                                     , descriptors=dbPair("title", "title")
                                     , rtable="lng_document"
                                     , ralias="doc"
                                     )
                   , "doc_user": dbRelationDef(name="doc_user"
                                     , keys=dbPair("usernr", "usernr")
                                     , descriptors=dbPair("user", "name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "dcdc_doc1": dbRelationDef(name="dcdc_doc1"
                                     , keys=dbPair("documentnr_1", "documentnr")
                                     , descriptors=dbPair("title_1", "title")
                                     , rtable="lng_document"
                                     , ralias="doc1"
                                     )
                   , "dcdc_doc2": dbRelationDef(name="dcdc_doc2"
                                     , keys=dbPair("documentnr_2", "documentnr")
                                     , descriptors=dbPair("title_2", "title")
                                     , rtable="lng_document"
                                     , ralias="doc2"
                                     )
                   , "dcdc_lnkc": dbRelationDef(name="dcdc_lnkc"
                                     , keys=dbPair("linkcode", "linkcode")
                                     , descriptors=dbPair("link", "description")
                                     , rtable="lng_linkcode"
                                     , ralias="lnkc"
                                     )
                   , "refs_catc1": dbRelationDef(name="refs_catc1"
                                     , keys=dbPair("main_categorycode","categorycode")
                                     , descriptors=dbPair("main_category","description")
                                     , rtable="lng_categorycode"
                                     , ralias="catc1"
                                     )
                   , "refs_catc2": dbRelationDef(name="refs_catc2"
                                     , keys=dbPair("sub_categorycode","categorycode")
                                     , descriptors=dbPair("sub_category","description")
                                     , rtable="lng_categorycode"
                                     , ralias="catc2"
                                     )
                   , "prus_proj": dbRelationDef(name="prus_proj"
                                     , keys=dbPair("projectnr","projectnr")
                                     , descriptors=dbPair("project","description")
                                     , rtable="lng_project"
                                     , ralias="proj"
                                     )
                   , "prus_user": dbRelationDef(name="prus_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "prln_proj": dbRelationDef(name="prln_project"
                                     , keys=dbPair("projectnr","projectnr")
                                     , descriptors=dbPair("project","description")
                                     , rtable="lng_project"
                                     , ralias="proj"
                                     )
                   , "prln_lngg": dbRelationDef(name="prln_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "recd_user": dbRelationDef(name="recd_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "recd_lngg": dbRelationDef(name="recd_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "recd_proj": dbRelationDef(name="recd_proj"
                                     , keys=dbPair("projectnr","projectnr")
                                     , descriptors=dbPair("project","description")
                                     , rtable="lng_project"
                                     , ralias="proj"
                                     )
                   , "scan_user": dbRelationDef(name="scan_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "scan_lngg": dbRelationDef(name="scan_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "scan_proj": dbRelationDef(name="scan_proj"
                                     , keys=dbPair("projectnr","projectnr")
                                     , descriptors=dbPair("project","description")
                                     , rtable="lng_project"
                                     , ralias="proj"
                                     )
                   , "text_recd": dbRelationDef(name="text_recd"
                                     , keys=dbPair("recordingnr","recordingnr")
                                     , descriptors=dbPair("recording","title")
                                     , rtable="lng_recording"
                                     , ralias="recd"
                                     )
                   , "text_scan": dbRelationDef(name="text_scan"
                                     , keys=dbPair("scannr","scannr")
                                     , descriptors=dbPair("scan","description")
                                     , rtable="lng_scan"
                                     , ralias="scan"
                                     )
                   , "text_user": dbRelationDef(name="text_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "text_lngg": dbRelationDef(name="text_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "prtx_proj": dbRelationDef(name="prtx_proj"
                                     , keys=dbPair("projectnr","projectnr")
                                     , descriptors=dbPair("project","description")
                                     , rtable="lng_project"
                                     , ralias="proj"
                                     )
                   , "prtx_text": dbRelationDef(name="prtx_text"
                                     , keys=dbPair("textnr","textnr")
                                     , descriptors=dbPair("text","title")
                                     , rtable="lng_text"
                                     , ralias="text"
                                     )
                   , "strm_text": dbRelationDef(name="strm_text"
                                     , keys=dbPair("textnr","textnr")
                                     , descriptors=dbPair("title","title")
                                     , rtable="lng_text"
                                     , ralias="text"
                                     )
                   , "strm_lngg": dbRelationDef(name="strm_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "strm_user": dbRelationDef(name="strm_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "elmt_strm": dbRelationDef(name="elmt_strm"
                                     , keys=dbPair("streamnr","streamnr")
                                     , descriptors=dbPair("stream","text")
                                     , rtable="lng_stream"
                                     , ralias="strm"
                                     )
                   , "elmt_elmt": dbRelationDef(name="elmt_elmt"
                                     , keys=dbPair("parent_elementnr","elementnr")
                                     , descriptors=dbPair("parent_element","text")
                                     , rtable="lng_element"
                                     , ralias="elmt2"
                                     )
                   , "elmt_lex": dbRelationDef(name="elmt_lex"
                                     , keys=dbPair("lexnr","lexnr")
                                     , descriptors=dbPair("lexeme","glosse")
                                     , rtable="lng_lex"
                                     , ralias="lex"
                                     )
                   , "elmt_eltc": dbRelationDef(name="elmt_eltc"
                                     , keys=dbPair("elementtypecode","elementtypecode")
                                     , descriptors=dbPair("elementtype","description")
                                     , rtable="lng_elementtypecode"
                                     , ralias="eltc"
                                     )
                   , "elmt_lngg": dbRelationDef(name="elmt_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "elmt_user": dbRelationDef(name="elmt_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "lex_user" : dbRelationDef(name="lex_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )

                   , "lex_lngg" : dbRelationDef(name="lex_lngg"
                                     , keys=dbPair("languagenr","languagenr")
                                     , descriptors=dbPair("language","language")
                                     , rtable="lng_language"
                                     , ralias="lngg"
                                     )
                   , "lxlx_lex1": dbRelationDef(name="lxlx_lex1"
                                     , keys=dbPair("lexnr_1", "lexnr")
                                     , descriptors=dbPair("form_1", "form")
                                     , rtable="lng_lex"
                                     , ralias="lex1"
                                     )
                   , "lxlx_lex2": dbRelationDef(name="lxlx_lex2"
                                     , keys=dbPair("lexnr_2", "lexnr")
                                     , descriptors=dbPair("form_2", "form")
                                     , rtable="lng_lex"
                                     , ralias="lex2"
                                     )
                   , "lxlx_lxrl": dbRelationDef(name="lxlx_lxrl"
                                     , keys=dbPair("lxlxrelcode", "lxlxrelcode")
                                     , descriptors=dbPair("relation", "description")
                                     , rtable="lng_lxlxrelcode"
                                     , ralias="lxrl"
                                     )
                     
                   , "lxlx_user": dbRelationDef(name="lxlx_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "tag_ttpc": dbRelationDef(name="tag_ttpc"
                                     , keys=dbPair("tagtypecode","tagtypecode")
                                     , descriptors=dbPair("tagtype","description")
                                     , rtable="lng_tagtypecode"
                                     , ralias="ttpc"
                                     )
                   , "txtg_text": dbRelationDef(name="txtg_text"
                                     , keys=dbPair("textnr","textnr")
                                     , descriptors=dbPair("title","title")
                                     , rtable="lng_text"
                                     , ralias="text"
                                     )
                   , "txtg_tag": dbRelationDef(name="txtx_tag"
                                     , keys=dbPair("tag","tag")
                                     , descriptors=dbPair("tagname","name")
                                     , rtable="lng_tag"
                                     , ralias="tag"
                                     )
                   , "txtg_user": dbRelationDef(name="txtg_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "sttg_strm": dbRelationDef(name="sttg_strrm"
                                     , keys=dbPair("streamnr","streamnr")
                                     , descriptors=dbPair("stream","text")
                                     , rtable="lng_stream"
                                     , ralias="strm"
                                     )
                   , "sttg_tag": dbRelationDef(name="sttg_tag"
                                     , keys=dbPair("tag","tag")
                                     , descriptors=dbPair("tagname","name")
                                     , rtable="lng_tag"
                                     , ralias="tag"
                                     )
                   , "sttg_user": dbRelationDef(name="sttg_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "eltg_elmt": dbRelationDef(name="eltg_elmt"
                                     , keys=dbPair("elementnr","elementnr")
                                     , descriptors=dbPair("element","text")
                                     , rtable="lng_element"
                                     , ralias="elmt"
                                     )
                   , "eltg_tag": dbRelationDef(name="eltg_tag"
                                     , keys=dbPair("tag","tag")
                                     , descriptors=dbPair("tagname","name")
                                     , rtable="lng_tag"
                                     , ralias="tag"
                                     )
                   , "eltg_user": dbRelationDef(name="eltg_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "lxtg_lex": dbRelationDef(name="lxtg_lex"
                                     , keys=dbPair("lexnr","lexnr")
                                     , descriptors=dbPair("lexeme","form")
                                     , rtable="lng_lex"
                                     , ralias="lex"
                                     )
                   , "lxtg_tag": dbRelationDef(name="lxtg_tag"
                                     , keys=dbPair("tag","tag")
                                     , descriptors=dbPair("tagname","name")
                                     , rtable="lng_tag"
                                     , ralias="tag"
                                     )
                   , "lxtg_user": dbRelationDef(name="lxtg_user"
                                     , keys=dbPair("usernr","usernr")
                                     , descriptors=dbPair("user","name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   , "tdmn_tag": dbRelationDef(name="tdmn_tag"
                                     , keys=dbPair("tag","tag")
                                     , descriptors=dbPair("tagname","name")
                                     , rtable="lng_tag"
                                     , ralias="tag"
                                     )
                   , "eltc_eltc": dbRelationDef(name="eltc_eltc"
                                     , keys=dbPair("parent_elementtypecode", "elementtypecode")
                                     , descriptors=dbPair("parent_elementtype","description")
                                     , rtable="lng_elementtypecode"
                                     , ralias="eltc2"
                                     )
                   , "plmt_lex": dbRelationDef(name="plmt_lex"
                                     , keys=dbPair("lexnr", "lexnr")
                                     , descriptors=dbPair("lexeme", "form")
                                     , rtable="lng_lex"
                                     , ralias="lex"
                                     )
                   , "plmt_user": dbRelationDef(name="plmt_user"
                                     , keys=dbPair("usernr", "usernr")
                                     , descriptors=dbPair("user", "name")
                                     , rtable="lng_user"
                                     , ralias="user"
                                     )
                   }
    
    self.addDef( lng_project = dbTableDef( tabletype=PKNR
                     , alias="proj"
                     , childtables={ "lng_proj_user": dbChildDef("lng_proj_user",
                                                                 dbPair("projectnr", "projectnr"))
                                   , "lng_proj_lngg": dbChildDef("lng_proj_lngg",
                                                                 dbPair("projectnr", "projectnr"))
                                   , "lng_recording": dbChildDef("lng_recording",
                                                                 dbPair("projectnr", "projectnr"))
                                   , "lng_scan": dbChildDef("lng_scan",
                                                            dbPair("projectnr", "projectnr"))
                                   , "lng_proj_text": dbChildDef("lng_proj_text",
                                                                 dbPair("projectnr", "projectnr"))
                                   }
                     , lookuptables=["proj_doc"]
                     , fieldOrder=["projectnr", "description", "summary", "url",
                                   "documentroot", "title", "grants"]
                     , primarykey="projectnr"
                     , fields={ "projectnr"   : PK()
                              , "description" : NN()
                              , "summary"     : FL(datatype=TEXT, inList=FALSE)
                              , "url"         : FL()
                              , "documentroot" : OK(relation="proj_doc")
                              , "title"       : NO()
                              , "grants"      : FL()
                              }
                     , hint="""
Projects

A project is a basic unit of research in Kura.
"""
                     )
              )
    self.addDef( lng_user = dbTableDef( tabletype=PKNR
                      , alias="user"
                      , childtables={"lng_lex": dbChildDef("lng_lex", dbPair("usernr", "usernr"))
                                    ,"lng_lex_lex": dbChildDef("lng_lex_lex", dbPair("usernr",
                                                                                     "usernr"))
                                    ,"lng_lex_tag": dbChildDef("lng_lex_tag", dbPair("usernr",
                                                                                     "usernr"))
                                    ,"lng_document": dbChildDef("lng_document", dbPair("usernr",
                                                                                       "usernr"))
                                    ,"lng_proj_user": dbChildDef("lng_proj_user", dbPair("usernr",
                                                                                         "usernr"))
                                    ,"lng_recording": dbChildDef("lng_recording", dbPair("usernr",
                                                                                         "usernr"))
                                    ,"lng_scan": dbChildDef("lng_scan", dbPair("usernr", "usernr"))
                                    ,"lng_text": dbChildDef("lng_text", dbPair("usernr", "usernr"))
                                    ,"lng_stream": dbChildDef("lng_stream", dbPair("usernr",
                                                                                   "usernr"))
                                    ,"lng_element": dbChildDef("lng_element", dbPair("usernr",
                                                                                     "usernr"))
                                    ,"lng_text_tag": dbChildDef("lng_text_tag", dbPair("usernr",
                                                                                       "usernr"))
                                    ,"lng_stream_tag": dbChildDef("lng_stream_tag", dbPair("usernr",
                                                                                           "usernr"))
                                    ,"lng_element_tag": dbChildDef("lng_element_tag",
                                                                   dbPair("usernr",
                                                                          "usernr"))
                                    }
                      , lookuptables=["user_affc"]
                      , descriptors=["name", "email"]
                      , primarykey="usernr"
                      , fieldOrder=["usernr", "name", "affiliationcode"
                         , "affiliation", "email", "snailmail", "fax", "telephone"
                         , "url" ]
                      , fields = { 'usernr'  : PK()
                         , 'name'            : NN()
                         , 'title'           : FL()
                         , 'affiliationcode' : OC( length=5, relation="user_affc")
                         , 'affiliation'     : NO()
                         , 'email'           : FL()
                         , 'snailmail'       : FL()
                         , 'fax'             : FL()
                         , 'telephone'       : FL()
                         , 'url'             : FL()
                         }
                      )
     )
    self.addDef( lng_document = dbTableDef( tabletype=PKNR
                      , alias="doc"
                      , childtables={ "lng_doc_doc": dbChildDef("lng_doc_doc", dbPair("documentnr", "documentnr_1"))
                                    , "lng_doc_doc_2": dbChildDef("lng_doc_doc", dbPair("documentnr", "documentnr_1"))
                                    }
                      , lookuptables=["doc_user"]
                      , primarykey="documentnr"
                      , fieldOrder=["documentnr", "title", "description", "url"
                         , "creation_date", "usernr", "user"]
                      , fields = { 'documentnr'  : PK()
                         , 'title'               : NN()
                         , 'description'         : FL(datatype=TEXT, inList=FALSE)
                         , 'creation_date'       : FL()
                         , "usernr"              : OK(relation="doc_user")
                         , "user"                : NO(inList=FALSE)
                         , "url"                 : FL()
                        }
                      )
     )
    self.addDef( lng_doc_doc = dbTableDef( tabletype=PKNR
                      , alias="dcdc"
                      , lookuptables=["dcdc_doc1", "dcdc_doc2", "dcdc_lnkc"]
                      , primarykey="docdocnr"
                      , fieldOrder=["docdocnr", "documentnr_1", "title_1", "documentnr_2", "title_2",
                                    "linkcode", "link", "description"]
                      , fields = { 'docdocnr'           : PK()
                                 , 'documentnr_1'       : FK(relation="dcdc_doc1")
                                 , 'title_1'            : NO()
                                 , 'documentnr_2'       : FK(relation="dcdc_doc2")
                                 , 'title_2'            : NO()
                                 , 'linkcode'           : FC(relation='dcdc_lnkc')
                                 , 'link'               : NO()
                                 , 'description'        : FL()
                        }
                      )
     )
    self.addDef( lng_linkcode = dbTableDef( tabletype=CODE
                      , alias="lnkc"
                      , childtables={"lng_doc_doc": dbChildDef("lng_doc_doc", dbPair("linkcode", "linkcode"))
                                    }
                      , lookuptables=[]
                      , primarykey="linkcode"
                      , fieldOrder=["linkcode", "description"]
                      , fields = { 'linkcode'  : NN()
                      , 'description'         : NN()
                      }
                      )
     )
    self.addDef( lng_language = dbTableDef( tabletype=RECURS
                          , alias="lngg"
                          , childtables={ "lng_language": dbChildDef("lng_language", dbPair("languagenr", "parent_languagenr"))
                                        , "lng_proj_lngg": dbChildDef("lng_proj_lngg", dbPair("languagenr", "languagenr"))
                                        , "lng_text":    dbChildDef("lng_text", dbPair("languagenr", "languagenr"))
                                        , "lng_lex":  dbChildDef("lng_lex", dbPair("languagenr", "languagenr"))
                                        , "lng_stream":  dbChildDef("lng_stream", dbPair("languagenr", "languagenr"))
                                        , "lng_recording": dbChildDef("lng_recording", dbPair("languagenr", "languagenr"))
                                        , "lng_scan":    dbChildDef("lng_scan", dbPair("languagenr", "languagenr"))
                                        , "lng_element": dbChildDef("lng_element", dbPair("languagenr", "languagenr"))
                                        }
                          , lookuptables=["lngg_lngg", "lngg_doc"]
                          , primarykey="languagenr"
                          , fieldOrder=["languagenr", "language", "description", "parent_languagenr"
                                , "parent_language", "documentroot", "title"]
                          , indexes = ['parent_languagenr']
                          , descriptors=["language"]
                          , fields= { 'languagenr': PK()
                            , 'description'       : FL( datatype=TEXT, inList=FALSE)
                            , 'parent_languagenr' : OK(relation="lngg_lngg")
                            , 'parent_language'   : NO()
                            , 'language'          : NN()
                            , "documentroot"      : OK(relation="lngg_doc")
                            , "title"             : NO()
                            }
                          )
       )

    self.addDef( lng_reference= dbTableDef( tabletype=PKNR
                     , alias="refs"
                     , lookuptables=["refs_catc1", "refs_catc2"]
                     , primarykey="referencenr"
                     , fieldOrder=["referencenr", "author", "year", "abbrev"
                         , "title", "periodical", "place", "publisher", "catalogue_card", "series"
                         , "volume", "pages" 
                         , "note", "main_categorycode", "main_category"
                         , "sub_categorycode", "sub_category"]
                     , descriptors=["title","author"]
                     , indexes = ['author', 'abbrev', 'title']
                     , fields={ "referencenr"       : PK()
                              , "author"            : NN()
                              , "year"              : NN()
                              , "abbrev"            : FL(length=25)
                              , "title"             : NN()
                              , "place"             : FL()
                              , "catalogue_card"    : FL()
                                , "periodical" : FL()
                              , "series"            : FL()
                              , "volume"            : FL()
                              , "pages"             : FL()
                              , "publisher"         : FL() 
                              , "note"              : FL(datatype=TEXT, inList=FALSE)
                              , "main_categorycode" : OC(relation="refs_catc1")
                              , "main_category"     : NO()
                              , "sub_categorycode"  : OC(relation="refs_catc2")
                              , "sub_category"      : NO()
                              }
                     )
              )
    self.addDef( lng_proj_user= dbTableDef( tabletype=PKNR
                     , alias="prus"
                     , childtables={}
                     , lookuptables=["prus_proj","prus_user"]
                     , primarykey="prusnr"
                     , descriptors=["project","user"]
                     , fieldOrder=["prusnr", "projectnr", "project", "usernr", "user"]
                     , fields={ "prusnr"    : PK()
                              , "projectnr" : FK(relation="prus_proj")
                              , "project"   : NO()
                              , "usernr"    : FK(relation="prus_user")
                              , "user"      : NO(inList=FALSE)
                              }
                     )
              )
    self.addDef( lng_proj_lngg = dbTableDef( tabletype=PKNR
                     , alias="prln"
                     , childtables={}
                     , lookuptables=["prln_proj","prln_lngg"]
                     , primarykey="prlnnr"
                     , indexes = ['languagenr']
                     , descriptors=["project","language"]
                     , fields={ "prlnnr"     : PK()
                              , "projectnr"  : FK(relation="prln_proj")
                              , "project"    : NO()
                              , "languagenr" : FK(relation="prln_lngg")
                              , "language"   : NO()
                              }
                     )
              )
    self.addDef( lng_recording = dbTableDef( tabletype=PKNR
                     , alias="recd"
                     , childtables={"lng_text": dbChildDef("lng_text", dbPair("recordingnr","recordingnr"))}
                     , lookuptables=["recd_user", "recd_lngg", "recd_proj"]
                     , primarykey="recordingnr"
                     , fieldOrder=["recordingnr", "title",  "url", "source"
                         , "tapenr", "tape_location", "informant", "duration"
                         , "recording_date", "languagenr"
                         , "language", "projectnr", "project", "description"
                         , "usernr", "user"]
                     , indexes = ['languagenr', 'projectnr']
                     , fields={ "recordingnr"    : PK()
                              , "description"    : NN(datatype=TEXT, inList=FALSE)
                              , "url"            : NN()
                              , "source"         : FL()
                              , "tapenr"         : FL()
                              , "tape_location"  : FL()
                              , "informant"      : FL()
                              , "duration"       : FL()
                              , "title"          : NN()
                              , "usernr"         : OK(relation="recd_user", readonly=TRUE)
                              , "user"           : NO()
                              , "recording_date" : FL(datatype=DATETIME)
                              , "languagenr"     : FK(relation="recd_lngg")
                              , "language"       : NO()
                              , "projectnr"      : OK(relation="recd_proj")
                              , "project"        : NO()
                              }
                     )
              )
    self.addDef( lng_scan= dbTableDef( tabletype=PKNR
                     , alias="scan"
                     , childtables={"lng_text": dbChildDef("lng_text", dbPair("scannr","scannr"))}
                     , lookuptables=["scan_user", "scan_lngg", "scan_proj"]
                     , primarykey="scannr"
                     , fieldOrder=["scannr", "title", "url", "manuscript_location"
                         , "page", "scan_date", "size", "description"
                         , "languagenr", "language", "projectnr", "project"
                         , "usernr", "user"]
                     , descriptors=["title","scan_date"]
                     , fields={ "scannr"              : PK()
                              , "description"         : NN(datatype=TEXT, inList=FALSE)
                              , "url"                 : NN()
                              , "manuscript_location" : FL()
                              , "title"               : NN()
                              , "page"                : FL()
                              , "usernr"              : OK(relation="scan_user")
                              , "user"                : NO(inList=FALSE)
                              , "scan_date"           : FL(datatype=DATETIME)
                              , "size"                : FL()
                              , "languagenr"          : FK(relation="scan_lngg")
                              , "language"            : NO()
                              , "projectnr"           : FK(relation="scan_proj")
                              , "project"             : NO()
                              }
                     , indexes = ['languagenr', 'projectnr']
                     )
              )
    self.addDef(lng_text = dbTableDef( tabletype=PKNR
                     , alias="text"
                     , childtables={"lng_proj_text": dbChildDef("lng_proj_text", dbPair("textnr", "textnr"))
                                   ,"lng_stream": dbChildDef("lng_stream", dbPair("textnr", "textnr"))
                                   ,"lng_text_tag": dbChildDef("lng_text_tag", dbPair("textnr", "textnr"))
                                   }
                     , lookuptables=["text_recd", "text_scan", "text_user", "text_lngg"]
                     , primarykey="textnr"
                     , fieldOrder=["textnr", "title","recordingnr", "recording", "scannr"
                         , "scan", "description", "url",  "usernr", "user"
                         , "transcription_date", "raw_text", "languagenr", "language"]
                     , descriptors=["title"] 
                     , fields={ "textnr"             : PK()
                              , "recordingnr"        : OK(relation="text_recd")
                              , "recording"          : NO(inList=TRUE)
                              , "scannr"             : OK(relation="text_scan")
                              , "scan"               : NO(inList=TRUE)
                              , "description"        : NN(datatype=TEXT, inList=FALSE)
                              , "url"                : FL(inList=FALSE)
                              , "title"              : NN()
                              , "usernr"             : OK(relation="text_user")
                              , "user"               : NO(inList=FALSE, readonly=TRUE, label="Last changed by")
                              , "transcription_date" : FL(datatype=DATETIME, inList=FALSE)
                              , "raw_text"           : FL(datatype=TEXT, inList=FALSE)
                              , "languagenr"         : FK(relation="text_lngg")
                              , "language"           : NO(inList=TRUE)
                              }
                     , indexes = ['languagenr']
                     )
              )
    self.addDef( lng_proj_text = dbTableDef( tabletype=PKNR
                     , alias="prtx"
                     , childtables={}
                     , lookuptables=["prtx_proj", "prtx_text"]
                     , primarykey="prtxnr"
                     , descriptors=["project","text"]
                     , indexes = ['projectnr', 'textnr']
                     , fieldOrder=["prtxnr", "projectnr", "project", "textnr", "text"]
                     , fields={ "prtxnr"    : PK()
                              , "projectnr" : FK(relation="prtx_proj")
                              , "project"   : NO()
                              , "textnr"    : FK(relation="prtx_text")
                              , "text"      : NO()
                              }
                     )
              )
    self.addDef( lng_stream = dbTableDef( tabletype=SEQ
                     , alias="strm"
                     , childtables={ "lng_element":
                                     dbChildDef("lng_element",
                                                dbPair("streamnr", "streamnr"))
                                   , "lng_stream_tag":
                                     dbChildDef("lng_stream_tag",
                                                dbPair("streamnr", "streamnr"))
                                   }
                     , lookuptables=["strm_text", "strm_user", "strm_lngg"]
                     , primarykey="streamnr"
                     , fieldOrder=["streamnr", "textnr", "title", "text", "seqnr"
                         , "languagenr", "language", "usernr", "user", "datestamp"]
                     , descriptors=["text"]
                     , sequencebase="textnr"
                     , fields={ "streamnr"  : PK()
                              , "textnr"    : FK(relation="strm_text", readonly=TRUE, label="Text")
                              , "title"     : NO()
                              , "text"      : FL()
                              , "languagenr": FK(relation="strm_lngg")
                              , "language"  : NO()
                              , "seqnr"     : SQ(dialog=FALSE)
                              , "usernr"    : OK(relation="strm_user", readonly=TRUE, label="Last changed by")
                              , "user"      : NO(inList=FALSE, readonly=TRUE)
                              , "datestamp" : DS()
                              }
                     , indexes = ['textnr', 'languagenr', 'seqnr']
                     )
              )

                                          
    #
    # Note: parent_elementnr is defined as default=0 because MySQL can't index columns with null fields.
    #
    self.addDef( lng_element = dbTableDef( tabletype=SEQ
                     , alias="elmt"
                     , childtables={"lng_element_tag": dbChildDef("lng_element_tag", dbPair("elementnr","elementnr"))
                                   , "lng_element": dbChildDef("lng_element", dbPair("elementnr","parent_elementnr"))}
                     , lookuptables=["elmt_lex", "elmt_strm", "elmt_elmt", "elmt_user", "elmt_lngg", "elmt_eltc"]
                     , primarykey="elementnr"
                     , fieldOrder=["elementnr", "text", "elementtypecode", "elementtype", "streamnr", "stream", "seqnr", 
                          "languagenr", "language", "parent_elementnr", "parent_element", "lexnr"
                          , "lexeme", "usernr", "user", "datestamp"]
                     , descriptors=["text"]
                     , sequencebase="streamnr"
                     , fields={ "elementnr" : PK()
                              , "streamnr"  : FK(relation="elmt_strm", label="Phrase", readonly=TRUE, dialog=FALSE)
                              , "stream"    : NO()
                              , "languagenr"  : FK(relation="elmt_lngg", label="Language")
                              , "language"    : NO()
                              , "seqnr"     : SQ(readonly=TRUE, dialog=FALSE, inList=FALSE)
                              , "parent_elementnr": OK(relation="elmt_elmt", label="This element is part of", readonly=TRUE, default=0)
                              , "parent_element" : NO()
                              , "text"      : FL()
                              , "elementtypecode": FC(relation="elmt_eltc", label="Type")
                              , "elementtype" : NO()
                              , "lexnr"     : OK(relation="elmt_lex", dialog=FALSE)
                              , "lexeme"    : NO()
                              , "usernr"    : OK(relation="elmt_user", readonly=TRUE, label="Last changed by")
                              , "user"      : NO(inList=FALSE)
                              , "datestamp" : DS()
                              }
                     , indexes = ['streamnr', 'languagenr', 'seqnr', 'parent_elementnr', 'lexnr']
                     )
              )


    self.addDef( lng_lex = dbTableDef( tabletype=PKNR
                     , alias="lex"
                     , childtables={"lng_lex_lex": dbChildDef("lng_lex_lex", dbPair("lexnr", "lexnr_1"))
                                   ,"lng_lex_tag": dbChildDef("lng_lex_tag", dbPair("lexnr", "lexnr"))
                                   ,"lng_element": dbChildDef("lng_element", dbPair("lexnr", "lexnr"))
                                   }
                     , lookuptables=["lex_lngg", "lex_user"]
                     , primarykey="lexnr"
                     , descriptors=["form"]
                     , indexes = ["languagenr", "glosse", "form"]                
                     , fieldOrder=["lexnr", "form"
                         , "glosse", "description", "phonetic_form", "alternative_form", "languagenr", "language", "isdone",
                         "usernr", "user", "datestamp"]
                     , fields={ "lexnr" : PK()
                      , "form"          : NN(length=50)
                      , "phonetic_form" : FL(length=100)
                      , "glosse"        : NN()
                      , "description"   : FL( inList=FALSE, datatype=TEXT )
                      , "languagenr"    : FK( relation="lex_lngg", label="language" )
                      , "language"      : NO()
                      , "usernr"        : OK( relation="lex_user", label="user", readonly=TRUE )
                      , "user"          : NO(inList=FALSE, readonly=TRUE)
                      , "datestamp"     : DS()
                      , "alternative_form" : FL(length=50, inList=TRUE)
                      , "isdone": FL(datatype=BOOLEAN, inList=TRUE)
                      }
                      )
     )

       
    self.addDef( lng_lex_lex = dbTableDef( tabletype=PKNR
                         , alias="lxlx"
                         , lookuptables=["lxlx_user", "lxlx_lex1", "lxlx_lex2", "lxlx_lxrl"]
                         , primarykey="lxlxnr"
                         , fieldOrder=["lxlxnr", "lexnr_1", "form_1", "lexnr_2", "form_2"
                              , "lxlxrelcode", "relation", "usernr", "note", "user", "datestamp"]
                         , descriptors=["form_1","form_2", "relation"]
                         , fields= { "lxlxnr": PK()
                           , 'lexnr_1'     : FK(relation="lxlx_lex1")
                           , 'form_1'      : NO(inList=FALSE)
                           , 'lexnr_2'     : FK(relation="lxlx_lex2")
                           , 'form_2'      : NO(label="Related form")
                           , 'lxlxrelcode' : FC(relation="lxlx_lxrl")
                           , 'relation'    : NO(label="Relation type")
                           , 'note'        : FL(datatype=TEXT, inList=FALSE)
                           , "usernr"      : OK(relation="lxlx_user")
                           , "user"        : NO(inList=FALSE)
                           , "datestamp"   : DS()
                           }
                         , indexes = ['lexnr_1', 'lexnr_2']
                         )
       )
    self.addDef( lng_lxlxrelcode = dbTableDef( tabletype=CODE
                     , alias="lxrl"
                     , childtables={"lng_lex_lex": dbChildDef("lng_lex_lex", dbPair("lxlxreclode", "lxlxrelcode"))}
                     , lookuptables=[]
                     , primarykey="lxlxrelcode"
                     , fieldOrder=["lxlxrelcode", "description"]
                     , fields={ "lxlxrelcode" : NN(length=5, label="Lexical relationcode")
                              , "description" : FL()
                              }
                     )
              )
    self.addDef( lng_tag = dbTableDef( tabletype=CODE
                     , alias="tag"
                     , childtables={"lng_stream_tag": dbChildDef("lng_stream_tag",dbPair("tag","tag"))
                                   ,"lng_text_tag": dbChildDef("lng_text_tag",dbPair("tag","tag"))
                                   ,"lng_element_tag": dbChildDef("lng_element_tag",dbPair("tag","tag"))
                                   ,"lng_lex_tag": dbChildDef("lng_lex_tag",dbPair("tag","tag"))
                                   }
                     , lookuptables=["tag_ttpc"]
                     , descriptors=["name"]
                     , primarykey="tag"
                     , fieldOrder=["tag", "name", "description", "tagtypecode", "tagtype",
                                   "text", "stream", "element", 
                                   "lexeme"]
                     , fields={ "tag"         : NN(length=5)
                              , "name"        : NN()
                              , "description" : FL()
                              , "tagtypecode" : FC(relation="tag_ttpc")
                              , "tagtype"     : NO()
                              , "text"        : FL(datatype=BOOLEAN)
                              , "stream"      : FL(datatype=BOOLEAN)
                              , "element"     : FL(datatype=BOOLEAN)
                              , "lexeme"      : FL(datatype=BOOLEAN)
                              }
                     )
              )
              
    self.addDef( lng_text_tag = dbTableDef( tabletype=PKNR
                     , alias="txtg"
                     , childtables={}
                     , lookuptables=["txtg_text", "txtg_tag", "txtg_user"]
                     , descriptors=["tagname"]
                     , primarykey="text_tagnr"
                     , fieldOrder=["text_tagnr", "textnr", "tag", "title", "tagname"
                          , "value", "description", "note", "usernr", "user", "datestamp"]
                     , fields={ "text_tagnr": PK()
                              , "textnr"    : FK(relation="txtg_text")
                              , "tag"       : FC(relation="txtg_tag")
                              , "title"     : NO(inList=FALSE)
                              , "tagname"   : NO(label="Tag")
                              , "value"     : FL(inList=FALSE)
                              , "description": FL(length=200, label="Value")
                              , "note"      : FL(datatype=TEXT, inList=FALSE)
                              , "usernr"    : OK(relation="txtg_user")
                              , "user"      : NO()
                              , "datestamp" : DS()
                              }
                     , indexes = ['textnr', 'tag']
                     )
              )
    self.addDef( lng_stream_tag = dbTableDef( tabletype=PKNR
                     , alias="sttg"
                     , childtables={}
                     , lookuptables=["sttg_strm", "sttg_tag", "sttg_user"]
                     , primarykey="stream_tagnr"
                     , descriptors=["tagname"]
                     , fieldOrder=["stream_tagnr", "streamnr", "tag", "stream", "tagname", "value", "description"
                           , "note", "usernr", "user", "datestamp"]
                     , fields={ "stream_tagnr": PK()
                              , "streamnr"  : FK(relation="sttg_strm")
                              , "tag"       : FC(relation="sttg_tag")
                              , "stream"    : NO()
                              , "tagname"   : NO()
                              , "value"     : FL()
                              , "description": FL(length=200, label="Value")        
                              , "note"      : FL(datatype=TEXT, inList=FALSE)
                              , "usernr"    : OK(relation="sttg_user")
                              , "user"      : NO(inList=FALSE)
                              , "datestamp" : DS()
                              }
                     , indexes = ['streamnr', 'tag']
                     )
              )
    self.addDef( lng_element_tag = dbTableDef( tabletype=PKNR
                     , alias="eltg"
                     , childtables={}
                     , lookuptables=["eltg_elmt", "eltg_tag", "eltg_user"]
                     , primarykey="element_tagnr"
                     , descriptors=["tagname"]
                     , fieldOrder=["element_tagnr", "elementnr", "tag", "element", "tagname", "value", "description"
                        , "note", "usernr", "user", "datestamp"]
                     , fields={ "element_tagnr": PK()
                              , "elementnr" : FK(relation="eltg_elmt")
                              , "tag"       : FC(relation="eltg_tag")
                              , "element"   : NO()
                              , "tagname"   : NO()
                              , "value"     : FL()
                              , "description": FL(length=200)
                              , "note"      : FL(datatype=TEXT, inList=FALSE)
                              , "usernr"    : OK(relation="eltg_user")
                              , "user"      : NO(inList=FALSE)
                              , "datestamp" : DS()
                              }
                     , indexes = ['elementnr', 'tag']
                     )
                     
              )
    self.addDef( lng_lex_tag = dbTableDef( tabletype=PKNR
                     , alias="lxtg"
                     , childtables={}
                     , lookuptables=["lxtg_lex", "lxtg_tag", "lxtg_user"]
                     , descriptors=["tagname"]
                     , primarykey="lex_tagnr"
                     , fieldOrder=["lex_tagnr", "lexnr", "tag", "lexeme", "tagname", "value", "description"
                          , "note", "usernr", "datestamp"]
                     , fields={ "lex_tagnr": PK()
                              , "lexnr"     : FK(relation="lxtg_lex")
                              , "tag"       : FC(relation="lxtg_tag")
                              , "lexeme"    : NO(label="Lexeme")
                              , "tagname"   : NO(label="Tag")
                              , "value"     : FL(label="Value", inList=FALSE)
                              , "note"      : FL(datatype=TEXT, inList=FALSE)
                              , "description": FL(length=200, label="Value")
                              , "usernr"    : OK(relation="lxtg_user")
                              , "user"      : NO(inList=FALSE)
                              , "datestamp" : DS()
                              }
                     , indexes = ['lexnr', 'tag'])
              )

    self.addDef( lng_tagtypecode = dbTableDef( tabletype=CODE
                     , alias="ttpc"
                     , childtables={"lng_tag": dbChildDef("lng_tag", dbPair("tagtypecode","tagtypecode"))}
                     , primarykey="tagtypecode"
                     , fieldOrder=["tagtypecode", "description", "isdomain", "isvalue", "isnote", "isreference"]
                     , fields={ "tagtypecode" : NN()
                              , "description" : NN()
                              , "isdomain"    : FL(datatype=BOOLEAN, inList=FALSE, label="Pick value from list of abbreviations", default="1")
                              , "isvalue"     : FL(datatype=BOOLEAN, inList=FALSE, label="Type a short value", default="0")
                              , "isnote"      : FL(datatype=BOOLEAN, inList=FALSE, label="Type a long note", default="0")
                              , "isreference" : FL(datatype=BOOLEAN, inList=FALSE, label="Pick a reference from a list", default="0")
                              }
                     )
              )
    self.addDef( lng_tagdomain = dbTableDef( tabletype=PKNR
                     , alias="tdmn"
                     , childtables={"lng_text_tag": dbChildDef("lng_text_tag", dbPair("domainnr","domainnr"))
                                   ,"lng_stream_tag": dbChildDef("lng_stream_tag", dbPair("domainnr","domainnr"))
                                   ,"lng_element_tag": dbChildDef("lng_element_tag", dbPair("domainnr","domainnr"))
                                   ,"lng_lex_tag": dbChildDef("lng_lex_tag", dbPair("domainnr","domainnr"))}
                     , primarykey="domainnr"
                     , lookuptables=["tdmn_tag"]
                     , fieldOrder=["domainnr","tag", "tagname",  "abbreviation", "description"]
                     , fields={ "domainnr"      : PK()
                              , "abbreviation" : NN(length=50)
                              , "tag"          : FC(relation="tdmn_tag")
                              , "tagname"      : NO()
                              , "description"  : NN(length=50)
                              }
                     , hint="""
Tag domains

The items you define here form the set of choices you are presented with when
you want to add a tag with some value to an item. For instance, if you want
to label a word in a phrase with a part of speech, you can define here all 
possible parts of speech.

When labelling the word, you will then be able to choose from the possibilities
defined here.                     
"""
                     )
              )
    self.addDef( lng_affiliationcode = dbTableDef( tabletype=CODE
                         , alias="affc"
                         , childtables={"lng_user": dbChildDef("lng_user", dbPair("affiliationcode", "affiliationcode"))}
                         , primarykey="affiliationcode"
                         , fieldOrder=["affiliationcode", "description", "institution", "url"]
                         , fields = { 'affiliationcode'  : NN (length=10)
                                    , 'description'      : NN()
                                    , 'institution'      : FL()
                                    , 'url'              : FL()
                                    }
                          )
      )
    self.addDef( lng_elementtypecode = dbTableDef( tabletype=CODE
                         , alias="eltc"
                         , childtables={"lng_element": dbChildDef("lng_element", dbPair("elementtypecode", "elementtypecode"))
                                       ,"lng_elementtypecode": dbChildDef("lng_elementtypecode", dbPair("elementtypecode",
                                                                                                        "parent_elementtypecode"))
                                       }
                         , primarykey="elementtypecode"
                         , fieldOrder=["elementtypecode", "description", "parent_elementtypecode", "parent_elementtype", 
                                       "splitmarker", "joinmarker"]
                         , lookuptables=['eltc_eltc']
                         , fields = { 'elementtypecode'  : NN (length=10)
                                    , 'description'      : NN()
                                    , 'parent_elementtypecode'  : OC(relation="eltc_eltc")
                                    , 'parent_elementtype'      : NO(label="Parent element type")
                                    , 'splitmarker'             : FL(label="Character used to split this element")
                                    , 'joinmarker'              : FL(label="Character used to join elements of this class")
                                    }
                          )
      )

    self.addDef( lng_categorycode = dbTableDef( tabletype=PKNR
                     , alias="catc"
                     , childtables={"lng_reference": dbChildDef("lng_reference", dbPair("categorycode","main_categorycode"))
                                   ,"lng_reference_2": dbChildDef("lng_reference", dbPair("categorycode","sub_categorycode"))
                                   }
                     , primarykey="categorycode"
                     , fieldOrder=["categorycode", "description"]
                     , fields={ "categorycode": NN()
                              , "description": NN()
                              }
                     )
              )
