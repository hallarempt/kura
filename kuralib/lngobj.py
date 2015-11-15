"""
  dictionary mapping between tablenames, record objects, 
  table objects and descriptive labels.
"""
from dbobj.appobj import  dbAppObj

from lng_affc import *
from lng_catc import *
from lng_elmt import *
from lng_eltg import *
from lng_lex  import *
from lng_lngg import *
from lng_lxtg import *
from lng_proj import *
from lng_recd import *
from lng_refs import *
from lng_scan import *
from lng_strm import *
from lng_sttg import *
from lng_tag  import *
from lng_text import *
from lng_ttpc import *
from lng_txtg import *
from lng_user import *
from lng_lnkc import *
from lng_tdmn import *
from lng_doc  import *
from lng_lxlx import *


def setObjects(self):
    self.objects = {"lng_categorycode"     : dbAppObj(recObj=lng_categorycode, tblObj=lng_categorycodes, label="Categories")
            , "lng_element"        : dbAppObj(recObj=lng_element, tblObj=lng_elements, label="Elements")
            , "lng_element_tag"    : dbAppObj(recObj=lng_element_tag, tblObj=lng_element_tags, label="Element tags")
            , "lng_lex"            : dbAppObj(recObj=lng_lex, tblObj=lng_lexemes, label="Lexemes")
            , "lng_language"       : dbAppObj(recObj=lng_language, tblObj=lng_languages, label="Languages")
            , "lng_document"       : dbAppObj(recObj=lng_document, tblObj=lng_documents, label="Documents")  
            , "lng_linkcode"       : dbAppObj(recObj=lng_linkcode, tblObj=lng_linkcodes, label="Link codes")  
            , "lng_lex_tag"        : dbAppObj(recObj=lng_lex_tag, tblObj=lng_lex_tags, label="Lexeme tags")
            , "lng_project"        : dbAppObj(recObj=lng_project, tblObj=lng_projects, label="Projects")
            , "lng_recording"      : dbAppObj(recObj=lng_recording, tblObj=lng_recordings, label="Recordings")
            , "lng_reference"      : dbAppObj(recObj=lng_reference, tblObj=lng_references, label="References")
            , "lng_scan"           : dbAppObj(recObj=lng_scan, tblObj=lng_scans, label="Scans")
            , "lng_stream"         : dbAppObj(recObj=lng_stream, tblObj=lng_streams, label="Streams")
            , "lng_stream_tag"     : dbAppObj(recObj=lng_stream_tag, tblObj=lng_stream_tags, label="Stream tags")
            , "lng_tag"            : dbAppObj(recObj=lng_tag, tblObj=lng_tags, label="Tag definitions")
            , "lng_text"           : dbAppObj(recObj=lng_text, tblObj=lng_texts, label="Texts")
            , "lng_tagtypecode"    : dbAppObj(recObj=lng_tagtypecode, tblObj=lng_tagtypecodes, label="Tag types")
            , "lng_text_tag"       : dbAppObj(recObj=lng_text_tag, tblObj=lng_text_tags, label="Text tags")
            , "lng_user"           : dbAppObj(recObj=lng_user, tblObj=lng_users, label="System users")
            , "lng_affiliationcode": dbAppObj(recObj=lng_affiliationcode, tblObj=lng_affiliationcodes, label="Affiliations")
            , "lng_tagdomain"      : dbAppObj(recObj=lng_tagdomain, tblObj=lng_tagdomains, label="Standard abbreviations")
            , "lng_lex_lex"        : dbAppObj(recObj=lng_lex_lex, tblObj=lng_lex_lexemes, label="Related lexemes")
            
  }

__copyright__="""
/***************************************************************************
    copyright            : (C) 2000 by Boudewijn Rempt 
                           see copyright notice for license
    email                : boud@rempt.xs4all.nl
    Revision             : $Revision: 1.5 $
    Last edited          : $Date: 2002/11/16 12:37:03 $
 ***************************************************************************/
"""
