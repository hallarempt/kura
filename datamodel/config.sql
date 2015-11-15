# MySQL dump 8.16
#
# Host: localhost    Database: andal
#--------------------------------------------------------
# Server version	3.23.44-Max-log

#
# Table structure for table 'lng_affiliationcode'
#

CREATE TABLE lng_affiliationcode (
  affiliationcode varchar(10) NOT NULL default '',
  description varchar(255) NOT NULL default '',
  institution varchar(255) default NULL,
  url varchar(255) default NULL,
  PRIMARY KEY  (affiliationcode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_affiliationcode'
#


#
# Table structure for table 'lng_categorycode'
#

CREATE TABLE lng_categorycode (
  categorycode varchar(10) NOT NULL default '',
  description varchar(255) NOT NULL default '',
  PRIMARY KEY  (categorycode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_categorycode'
#

INSERT INTO lng_categorycode VALUES ('PERIOD','Periodical');
INSERT INTO lng_categorycode VALUES ('BOOK','Book');
INSERT INTO lng_categorycode VALUES ('WWW','Website');
INSERT INTO lng_categorycode VALUES ('COLL','Collection');

#
# Table structure for table 'lng_doc_doc'
#

CREATE TABLE lng_doc_doc (
  docdocnr int(10) unsigned NOT NULL auto_increment,
  documentnr_1 int(10) unsigned NOT NULL default '0',
  documentnr_2 int(10) unsigned NOT NULL default '0',
  linkcode varchar(5) NOT NULL default '',
  description varchar(50) default NULL,
  PRIMARY KEY  (docdocnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_doc_doc'
#


#
# Table structure for table 'lng_doc_refs'
#

CREATE TABLE lng_doc_refs (
  documentnr int(10) unsigned NOT NULL default '0',
  referencenr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (documentnr,referencenr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_doc_refs'
#


#
# Table structure for table 'lng_document'
#

CREATE TABLE lng_document (
  documentnr int(10) unsigned NOT NULL auto_increment,
  title varchar(255) NOT NULL default '',
  description text,
  creation_date date default NULL,
  url varchar(255) NOT NULL default '',
  usernr int(10) unsigned default NULL,
  PRIMARY KEY  (documentnr),
  KEY i_doc_1 (title),
  KEY i_doc_2 (url)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_document'
#


#
# Table structure for table 'lng_element'
#

CREATE TABLE lng_element (
  elementnr int(10) unsigned NOT NULL auto_increment,
  streamnr int(10) unsigned NOT NULL default '0',
  seqnr int(11) NOT NULL default '0',
  parent_elementnr int(10) unsigned NOT NULL default '0',
  text varchar(255) NOT NULL default '',
  elementtypecode varchar(10) NOT NULL default '',
  lexnr int(10) unsigned default NULL,
  languagenr int(10) unsigned default NULL,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (elementnr),
  KEY i_elmt_1 (streamnr),
  KEY i_elmt_2 (parent_elementnr),
  KEY i_elmt_3 (text),
  KEY i_elmt_4 (lexnr),
  KEY i_elmt_5 (languagenr)
) TYPE=MyISAM;

#
# Table structure for table 'lng_element_tag'
#

CREATE TABLE lng_element_tag (
  element_tagnr int(10) unsigned NOT NULL auto_increment,
  elementnr int(10) unsigned NOT NULL default '0',
  tag varchar(50) NOT NULL default '',
  value varchar(200) default NULL,
  description varchar(200) default NULL,
  note text,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (element_tagnr),
  KEY i_elmt_1 (elementnr),
  KEY i_elmt_2 (tag)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_element_tag'
#


#
# Table structure for table 'lng_elementtypecode'
#

CREATE TABLE lng_elementtypecode (
  elementtypecode varchar(10) NOT NULL default '',
  description varchar(250) NOT NULL default '',
  parent_elementtypecode varchar(10) default NULL,
  splitmarker char(1) NOT NULL default '',
  joinmarker char(1) NOT NULL default '',
  PRIMARY KEY  (elementtypecode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_elementtypecode'
#

INSERT INTO lng_elementtypecode VALUES ('CLAUSE','Clause',NULL,'$','');
INSERT INTO lng_elementtypecode VALUES ('FORM','Form','CLAUSE','.','');
INSERT INTO lng_elementtypecode VALUES ('MORPHEME','Morpheme','FORM','.','.');
INSERT INTO lng_elementtypecode VALUES ('PHONEME','Phoneme','MORPHEME','-','');

#
# Table structure for table 'lng_language'
#

CREATE TABLE lng_language (
  languagenr int(10) unsigned NOT NULL auto_increment,
  language varchar(255) NOT NULL default '',
  parent_languagenr int(10) unsigned default NULL,
  description text,
  documentroot int(10) unsigned default NULL,
  PRIMARY KEY  (languagenr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_language'
#

#
# Table structure for table 'lng_lex'
#

CREATE TABLE lng_lex (
  lexnr int(10) unsigned NOT NULL auto_increment,
  form varchar(50) NOT NULL default '',
  phonetic_form varchar(100) default NULL,
  glosse varchar(255) NOT NULL default '',
  description text,
  languagenr int(10) unsigned NOT NULL default '0',
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  alternative_form varchar(50) default NULL,
  done char(1) default NULL,
  isdone decimal(1,0) NOT NULL default '0',
  PRIMARY KEY  (lexnr),
  KEY i_lex (form)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_lex'
#

#
# Table structure for table 'lng_lex_lex'
#

CREATE TABLE lng_lex_lex (
  lxlxnr int(10) unsigned NOT NULL auto_increment,
  lexnr_1 int(10) unsigned NOT NULL default '0',
  lexnr_2 int(10) unsigned NOT NULL default '0',
  lxlxrelcode varchar(255) default NULL,
  note text,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (lxlxnr),
  UNIQUE KEY u_lxlx (lexnr_1,lexnr_2)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_lex_lex'
#

#
# Table structure for table 'lng_lex_tag'
#

CREATE TABLE lng_lex_tag (
  lex_tagnr int(10) unsigned NOT NULL auto_increment,
  lexnr int(10) unsigned NOT NULL default '0',
  tag varchar(50) NOT NULL default '',
  value varchar(200) default NULL,
  description varchar(200) default NULL,
  note text,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (lex_tagnr),
  KEY i_lxtg_1 (lexnr),
  KEY i_lxtg_2 (tag)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_lex_tag'
#

INSERT INTO lng_lex_tag VALUES (1,141,'POS','2','Verb',NULL,1,20020618005215);

#
# Table structure for table 'lng_linkcode'
#

CREATE TABLE lng_linkcode (
  linkcode varchar(5) NOT NULL default '',
  description varchar(255) NOT NULL default '',
  PRIMARY KEY  (linkcode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_linkcode'
#


#
# Table structure for table 'lng_lxlxrelcode'
#

CREATE TABLE lng_lxlxrelcode (
  lxlxrelcode varchar(10) NOT NULL default '',
  description varchar(255) default NULL,
  PRIMARY KEY  (lxlxrelcode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_lxlxrelcode'
#

INSERT INTO lng_lxlxrelcode VALUES ('ETYM','Etymology');
INSERT INTO lng_lxlxrelcode VALUES ('DERIV','Derivation');
INSERT INTO lng_lxlxrelcode VALUES ('VCMP','Verbal compound');
INSERT INTO lng_lxlxrelcode VALUES ('DVAND','Co-ordinative (dvandva) compound');
INSERT INTO lng_lxlxrelcode VALUES ('KARMA','Descriptive (Karmadhāraya) determinative');
INSERT INTO lng_lxlxrelcode VALUES ('BAHU','Possessive (Bahuvrīhi) compound');
INSERT INTO lng_lxlxrelcode VALUES ('TAT','Dependent (Tatpuruṣa) determinative');
INSERT INTO lng_lxlxrelcode VALUES ('PARA','Paradigmatical derviation');
INSERT INTO lng_lxlxrelcode VALUES ('ADVRB','Adverbial compound');
INSERT INTO lng_lxlxrelcode VALUES ('MORPH','Morpho-phonological variaton');

#
# Table structure for table 'lng_proj_lngg'
#

CREATE TABLE lng_proj_lngg (
  prlnnr int(10) unsigned NOT NULL auto_increment,
  projectnr int(10) unsigned NOT NULL default '0',
  languagenr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (prlnnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_proj_lngg'
#


#
# Table structure for table 'lng_proj_text'
#

CREATE TABLE lng_proj_text (
  prtxnr int(10) unsigned NOT NULL auto_increment,
  projectnr int(10) unsigned NOT NULL default '0',
  textnr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (prtxnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_proj_text'
#


#
# Table structure for table 'lng_proj_user'
#

CREATE TABLE lng_proj_user (
  prusnr int(10) unsigned NOT NULL auto_increment,
  projectnr int(10) unsigned NOT NULL default '0',
  usernr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (prusnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_proj_user'
#


#
# Table structure for table 'lng_project'
#

CREATE TABLE lng_project (
  projectnr int(10) unsigned NOT NULL auto_increment,
  description varchar(255) default NULL,
  summary text,
  url varchar(255) default NULL,
  grants text,
  documentroot int(10) unsigned default NULL,
  PRIMARY KEY  (projectnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_project'
#

#
# Table structure for table 'lng_recording'
#

CREATE TABLE lng_recording (
  recordingnr int(10) unsigned NOT NULL auto_increment,
  description text,
  url varchar(255) NOT NULL default '',
  source varchar(255) default NULL,
  tapenr varchar(255) default NULL,
  tape_location varchar(255) default NULL,
  informant varchar(255) default NULL,
  duration int(10) unsigned default NULL,
  title varchar(255) NOT NULL default '',
  usernr int(10) unsigned default NULL,
  recording_date date default NULL,
  languagenr int(10) unsigned NOT NULL default '0',
  projectnr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (recordingnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_recording'
#

#
# Table structure for table 'lng_reference'
#

CREATE TABLE lng_reference (
  referencenr int(10) unsigned NOT NULL auto_increment,
  author varchar(255) NOT NULL default '',
  year varchar(4) NOT NULL default '',
  title varchar(255) NOT NULL default '',
  place varchar(255) NOT NULL default '',
  catalogue_card text,
  note text,
  main_categorycode varchar(10) NOT NULL default '',
  sub_categorycode varchar(10) NOT NULL default '',
  series varchar(50) default NULL,
  volume varchar(20) default NULL,
  pages varchar(50) default NULL,
  publisher varchar(50) default NULL,
  periodical varchar(100) default NULL,
  abbrev varchar(25) NOT NULL default '',
  PRIMARY KEY  (referencenr),
  UNIQUE KEY u_ref_1 (abbrev),
  KEY i_refs_1 (author),
  KEY i_refs_2 (year),
  KEY i_refs_3 (title),
  KEY i_refs_4 (place),
  KEY i_refs_5 (main_categorycode),
  KEY i_refs_6 (sub_categorycode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_reference'
#


#
# Table structure for table 'lng_scan'
#

CREATE TABLE lng_scan (
  scannr int(10) unsigned NOT NULL auto_increment,
  description text,
  url varchar(255) default NULL,
  manuscript_location varchar(255) default NULL,
  title varchar(255) NOT NULL default '',
  page varchar(255) default NULL,
  usernr int(10) unsigned default NULL,
  scan_date date default NULL,
  size varchar(255) default NULL,
  languagenr int(10) unsigned NOT NULL default '0',
  projectnr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (scannr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_scan'
#


#
# Table structure for table 'lng_stream'
#

CREATE TABLE lng_stream (
  streamnr int(10) unsigned NOT NULL auto_increment,
  textnr int(10) unsigned NOT NULL default '0',
  seqnr int(11) NOT NULL default '0',
  text text NOT NULL,
  languagenr int(10) unsigned default NULL,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (streamnr),
  UNIQUE KEY u_strm (textnr,seqnr),
  KEY i_text (textnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_stream'
#

# Table structure for table 'lng_stream_tag'
#

CREATE TABLE lng_stream_tag (
  stream_tagnr int(10) unsigned NOT NULL auto_increment,
  streamnr int(10) unsigned NOT NULL default '0',
  tag varchar(50) NOT NULL default '',
  value varchar(200) default NULL,
  description varchar(200) default NULL,
  note text,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (stream_tagnr),
  KEY i_sttg_1 (streamnr),
  KEY i_sttg_2 (tag)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_stream_tag'
#


# Table structure for table 'lng_tag'
#

CREATE TABLE lng_tag (
  tag varchar(50) NOT NULL default '',
  name varchar(255) NOT NULL default '',
  description text,
  tagtypecode varchar(5) NOT NULL default '',
  text decimal(1,0) NOT NULL default '1',
  stream decimal(1,0) NOT NULL default '1',
  element decimal(1,0) NOT NULL default '1',
  lexeme decimal(1,0) NOT NULL default '1',
  PRIMARY KEY  (tag),
  UNIQUE KEY name (name)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_tag'
#

INSERT INTO lng_tag VALUES ('TAPEP','Tape Position','Start - end in seconds on a recording.','TIME',1,1,1,1);
INSERT INTO lng_tag VALUES ('GL','Glosse','Glosse (freeform)','GLOSS',1,1,1,1);
INSERT INTO lng_tag VALUES ('FUNC','Function','Syntactical function','DABBR',0,0,1,0);
INSERT INTO lng_tag VALUES ('POS','Part of Speech','Part of Speech','DABBR',0,0,1,1);
INSERT INTO lng_tag VALUES ('PENN','Penn-Treebank','Penn-Treebank part-of-speech tags (according to Jurafsk & Martin 2000)','DABBR',0,0,1,1);
INSERT INTO lng_tag VALUES ('TR','Translation','Translation','TRNS',0,1,0,0);
INSERT INTO lng_tag VALUES ('FTR','Full translation','Full translation','TRNS',1,0,0,0);
INSERT INTO lng_tag VALUES ('TRANS','Transcription','Phonetic transcription','PHON',1,1,1,1);
INSERT INTO lng_tag VALUES ('REF','Reference','Reference','REF',1,1,1,1);
INSERT INTO lng_tag VALUES ('FORM','Form','morphological form','DABBR',0,0,1,1);
INSERT INTO lng_tag VALUES ('PHON','Phonetic form',NULL,'PHON',0,1,1,1);
INSERT INTO lng_tag VALUES ('NOTE','Note','Note','TEXT',1,1,1,1);
INSERT INTO lng_tag VALUES ('ABBR','Abbreviation','Glosse (from an abbreviation)','DABBR',1,1,1,1);
INSERT INTO lng_tag VALUES ('SEMDO','Semantic domain','A semantic domain, allofam','DABBR',0,0,0,1);

#
# Table structure for table 'lng_tagdomain'
#

CREATE TABLE lng_tagdomain (
  domainnr int(10) unsigned NOT NULL auto_increment,
  abbreviation varchar(10) NOT NULL default '',
  tag varchar(50) NOT NULL default '',
  description varchar(50) default NULL,
  PRIMARY KEY  (domainnr),
  UNIQUE KEY abbreviation (abbreviation,tag)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_tagdomain'
#

INSERT INTO lng_tagdomain VALUES (1,'N','POS','Noun');
INSERT INTO lng_tagdomain VALUES (2,'V','POS','Verb');
INSERT INTO lng_tagdomain VALUES (3,'ADJ','POS','Adjective');
INSERT INTO lng_tagdomain VALUES (4,'ADV','POS','Adverb');
INSERT INTO lng_tagdomain VALUES (5,'PRON','POS','Pronoun');
INSERT INTO lng_tagdomain VALUES (6,'ART','POS','Article');
INSERT INTO lng_tagdomain VALUES (7,'PART','POS','Particle');
INSERT INTO lng_tagdomain VALUES (8,'PREPOS','POS','Preposition');
INSERT INTO lng_tagdomain VALUES (9,'POSTPOS','POS','Postposition');
INSERT INTO lng_tagdomain VALUES (10,'CONJ','POS','Conjuction');
INSERT INTO lng_tagdomain VALUES (11,'INTER','POS','Interjection');
INSERT INTO lng_tagdomain VALUES (12,'PROPN','POS','Proper noun');
INSERT INTO lng_tagdomain VALUES (14,'AUX','POS','Auxiliary verb');
INSERT INTO lng_tagdomain VALUES (13,'MASS','POS','Mass noun');
INSERT INTO lng_tagdomain VALUES (15,'DETER','POS','Determiner');
INSERT INTO lng_tagdomain VALUES (16,'NUM','POS','Numeral');
INSERT INTO lng_tagdomain VALUES (17,'COMPL','POS','Complementizer');
INSERT INTO lng_tagdomain VALUES (18,'POSSPRON','POS','Possessive pronoun');
INSERT INTO lng_tagdomain VALUES (19,'QPART','POS','Question particle');
INSERT INTO lng_tagdomain VALUES (20,'SUBOR','POS','Subordinator');
INSERT INTO lng_tagdomain VALUES (21,'vi','POS','Intransitive verb');
INSERT INTO lng_tagdomain VALUES (22,'vt','POS','Transitive verb');
INSERT INTO lng_tagdomain VALUES (23,'vtt','POS','Ditransitive verb');
INSERT INTO lng_tagdomain VALUES (26,'STATV','POS','Stative verb');
INSERT INTO lng_tagdomain VALUES (25,'DEMON','POS','Demonstrative');
INSERT INTO lng_tagdomain VALUES (27,'CC','PENN','Coordinative conjunction');
INSERT INTO lng_tagdomain VALUES (28,'CD','PENN','Cardinal number');
INSERT INTO lng_tagdomain VALUES (29,'DT','PENN','Determiner');
INSERT INTO lng_tagdomain VALUES (30,'EX','PENN','Existential \'there\'');
INSERT INTO lng_tagdomain VALUES (31,'FW','PENN','Foreign word');
INSERT INTO lng_tagdomain VALUES (32,'IN','PENN','Preposition/sub-conj');
INSERT INTO lng_tagdomain VALUES (33,'JJ','PENN','Adjective');
INSERT INTO lng_tagdomain VALUES (34,'JJR','PENN','Adj. comparative');
INSERT INTO lng_tagdomain VALUES (35,'JJS','PENN','Adj. superlative');
INSERT INTO lng_tagdomain VALUES (36,'LS','PENN','List item marker');
INSERT INTO lng_tagdomain VALUES (37,'MD','PENN','Modal');
INSERT INTO lng_tagdomain VALUES (38,'NN','PENN','Noun, sing. or mass');
INSERT INTO lng_tagdomain VALUES (39,'NNS','PENN','Noun, plural');
INSERT INTO lng_tagdomain VALUES (40,'NNP','PENN','Proper noun, singular');
INSERT INTO lng_tagdomain VALUES (41,'NNPS','PENN','Proper noun, plural');
INSERT INTO lng_tagdomain VALUES (42,'PDT','PENN','Predeterminer');
INSERT INTO lng_tagdomain VALUES (43,'POS','PENN','Possessive ending');
INSERT INTO lng_tagdomain VALUES (44,'PP','PENN','Personal pronoun');
INSERT INTO lng_tagdomain VALUES (45,'PPS','PENN','Possessive pronoun');
INSERT INTO lng_tagdomain VALUES (46,'RB','PENN','Adverb');
INSERT INTO lng_tagdomain VALUES (47,'RBR','PENN','Adverb, comparative');
INSERT INTO lng_tagdomain VALUES (48,'RBS','PENN','Adverb, superlative');
INSERT INTO lng_tagdomain VALUES (49,'RP','PENN','Particle');
INSERT INTO lng_tagdomain VALUES (50,'SYM','PENN','Symbol');
INSERT INTO lng_tagdomain VALUES (51,'TO','PENN','\"to\"');
INSERT INTO lng_tagdomain VALUES (52,'UH','PENN','Interjection');
INSERT INTO lng_tagdomain VALUES (53,'VB','PENN','Verb, base form');
INSERT INTO lng_tagdomain VALUES (54,'VBD','PENN','Verb, past tense');
INSERT INTO lng_tagdomain VALUES (55,'VBG','PENN','Verb, gerund');
INSERT INTO lng_tagdomain VALUES (56,'VBN','PENN','Verb, past-participle');
INSERT INTO lng_tagdomain VALUES (57,'VBP','PENN','Verb, non-3sg pres');
INSERT INTO lng_tagdomain VALUES (58,'VBZ','PENN','Verb, 3sg pres');
INSERT INTO lng_tagdomain VALUES (59,'WDT','PENN','Wh-determiner');
INSERT INTO lng_tagdomain VALUES (60,'WP','PENN','Wh-pronoun');
INSERT INTO lng_tagdomain VALUES (61,'WP$','PENN','Possessive wh-');
INSERT INTO lng_tagdomain VALUES (62,'WRB','PENN','Wh-adverb');
INSERT INTO lng_tagdomain VALUES (63,'$','PENN','Dollar sign');
INSERT INTO lng_tagdomain VALUES (64,'#','PENN','Pound sign (₤)');
INSERT INTO lng_tagdomain VALUES (65,'“','PENN','Left quote');
INSERT INTO lng_tagdomain VALUES (66,'”','PENN','Right quote');
INSERT INTO lng_tagdomain VALUES (67,'(','PENN','Left parenthesis');
INSERT INTO lng_tagdomain VALUES (68,')','PENN','Right parenthesis');
INSERT INTO lng_tagdomain VALUES (69,',','PENN','Comma');
INSERT INTO lng_tagdomain VALUES (70,'.','PENN','Sentence-final punc');
INSERT INTO lng_tagdomain VALUES (71,':','PENN','Mid-sentence punc');
INSERT INTO lng_tagdomain VALUES (72,'S','FUNC','Subject');
INSERT INTO lng_tagdomain VALUES (73,'V','FUNC','Verb');
INSERT INTO lng_tagdomain VALUES (74,'O','FUNC','Object');
INSERT INTO lng_tagdomain VALUES (75,'O2','FUNC','Indirect object');
INSERT INTO lng_tagdomain VALUES (76,'TOP','FUNC','Topic');
INSERT INTO lng_tagdomain VALUES (77,'FOCUS','FUNC','Focus');
INSERT INTO lng_tagdomain VALUES (127,'part','ABBR','participle');
INSERT INTO lng_tagdomain VALUES (126,'n-prt','ABBR','non-preterite');
INSERT INTO lng_tagdomain VALUES (125,'fut','ABBR','futurum');
INSERT INTO lng_tagdomain VALUES (124,'np','ABBR','non-plural');
INSERT INTO lng_tagdomain VALUES (123,'ns','ABBR','non-singular');
INSERT INTO lng_tagdomain VALUES (122,'d','ABBR','dual');
INSERT INTO lng_tagdomain VALUES (121,'prt','ABBR','preterite');
INSERT INTO lng_tagdomain VALUES (120,'prs','ABBR','praesens');
INSERT INTO lng_tagdomain VALUES (119,'p','ABBR','plural');
INSERT INTO lng_tagdomain VALUES (118,'s','ABBR','singular');
INSERT INTO lng_tagdomain VALUES (117,'3','ABBR','third person');
INSERT INTO lng_tagdomain VALUES (116,'2','ABBR','second person');
INSERT INTO lng_tagdomain VALUES (115,'1','ABBR','first person');
INSERT INTO lng_tagdomain VALUES (110,'s','FORM','suffix');
INSERT INTO lng_tagdomain VALUES (111,'p','FORM','prefix');
INSERT INTO lng_tagdomain VALUES (112,'i','FORM','infix');
INSERT INTO lng_tagdomain VALUES (113,'∑','FORM','verbal root');
INSERT INTO lng_tagdomain VALUES (114,'√','FORM','Nominal root');
INSERT INTO lng_tagdomain VALUES (128,'AAM','SEMDO','army and military');

#
# Table structure for table 'lng_tagtypecode'
#

CREATE TABLE lng_tagtypecode (
  tagtypecode varchar(5) NOT NULL default '',
  description varchar(255) NOT NULL default '',
  isdomain decimal(1,0) NOT NULL default '0',
  isvalue decimal(1,0) NOT NULL default '1',
  isnote decimal(1,0) NOT NULL default '0',
  isreference decimal(1,0) NOT NULL default '0',
  PRIMARY KEY  (tagtypecode)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_tagtypecode'
#

INSERT INTO lng_tagtypecode VALUES ('TEXT','Longer free text',0,0,1,0);
INSERT INTO lng_tagtypecode VALUES ('REF','Reference',0,0,0,1);
INSERT INTO lng_tagtypecode VALUES ('GLOSS','Glosse',0,1,0,0);
INSERT INTO lng_tagtypecode VALUES ('DABBR','Domain based abbreviation',1,0,0,0);
INSERT INTO lng_tagtypecode VALUES ('PHON','Phonetic transcription',0,1,0,0);
INSERT INTO lng_tagtypecode VALUES ('TRLIT','Transliteration',0,1,0,0);
INSERT INTO lng_tagtypecode VALUES ('TRNS','Translation',0,0,1,0);
INSERT INTO lng_tagtypecode VALUES ('TIME','Value in seconds',0,1,0,0);

#
# Table structure for table 'lng_text'
#

CREATE TABLE lng_text (
  textnr int(10) unsigned NOT NULL auto_increment,
  recordingnr int(10) unsigned default NULL,
  scannr int(10) unsigned default NULL,
  description text,
  url varchar(255) default NULL,
  title varchar(255) NOT NULL default '',
  usernr int(10) unsigned default NULL,
  transcription_date date default NULL,
  raw_text text NOT NULL,
  languagenr int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (textnr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_text'
#

# Table structure for table 'lng_text_tag'
#

CREATE TABLE lng_text_tag (
  text_tagnr int(10) unsigned NOT NULL auto_increment,
  textnr int(10) unsigned NOT NULL default '0',
  tag varchar(50) NOT NULL default '',
  value varchar(200) NOT NULL default '',
  description varchar(200) default NULL,
  note text,
  usernr int(10) unsigned default NULL,
  datestamp timestamp(14) NOT NULL,
  PRIMARY KEY  (text_tagnr),
  KEY i_txtg_1 (textnr),
  KEY i_txtg_2 (tag)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_text_tag'
#


#
# Table structure for table 'lng_user'
#

CREATE TABLE lng_user (
  usernr int(10) unsigned NOT NULL auto_increment,
  name varchar(255) NOT NULL default '',
  title varchar(255) default NULL,
  affiliationcode varchar(5) default NULL,
  email varchar(255) default NULL,
  snailmail varchar(255) default NULL,
  fax varchar(255) default NULL,
  telephone varchar(255) default NULL,
  url varchar(255) default NULL,
  PRIMARY KEY  (usernr)
) TYPE=MyISAM;

#
# Dumping data for table 'lng_user'
#


