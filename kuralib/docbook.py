""" docbook utils """

False = 0
True = 1

def xmlHeader(doctype):
    return """<?xml version="1.0"  encoding='UTF-8'?>
<!DOCTYPE %s PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
                    "http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd">""" % doctype
                    
def periodical_RAW():
    return """
    <biblioentry id="references_%(referencenr)i">
      <biblioset relation="article">
        <author><surname>%(author_surname)s</surname>
          <firstname>%(author_firstname)s</firstname></author>
        <title>%(title)s</title>
        <subtitle>%(subtitle)s</subtitle>
        <issuenum>%(issuenum)s</issuenum>
        <date>%(year)s</date>
        <pagenums>%(pages)s</pagenums>
      </biblioset>
      <biblioset relation="journal">
        <title>%(periodical)s</title>
        <publisher>
          <publishername>%(publisher)s</publishername>
          <address><city>%(place)s</city></address>
        </publisher>
        </biblioset>
    </biblioentry>"""

def book_RAW():
    return """
    <biblioentry id="references_%(referencenr)i">
        <author><surname>%(author_surname)s</surname>
          <firstname>%(author_firstname)s</firstname></author>
        <title>%(title)s</title>
        <pubdate><year>%(year)s</year></pubdate>
      <publisher>
          <publishername>%(publisher)s</publishername>
          <address><city>%(place)s</city></address>
      </publisher>
    </biblioentry>
    """

def collection_RAW():
    return """
    """

def website_RAW():
    return """
    """

def periodical():
    return """
<bibliomixed id="%(abbrev)s">
  <bibliomset relation='article'>
    <surname>%(author_surname)s</surname>,
    <firstname>%(author_firstname)s</firstname>
    <pubdate>%(year)s</pubdate>
    <title role='article'>%(title)s</title>,
  </bibliomset>
  <bibliomset relation='journal'>
    <title>%(periodical)s</title> 
    <issuenum>%(issuenum)s</issuenum>,
    <publishername>%(publisher)s</publishername>:
    <pagenums>%(pages)s</pagenums>.
    </bibliomset>
</bibliomixed>"""

def book():
        return """
<bibliomixed id="%(abbrev)s">
  <bibliomset>
    <surname>%(author_surname)s</surname>,
    <firstname>%(author_firstname)s</firstname>
    <pubdate>%(year)s</pubdate>
    <title><emphasis>%(title)s</emphasis></title>,
    <address><city>%(place)s</city></address>
    <publishername>%(publisher)s</publishername>
    </bibliomset>.
</bibliomixed>"""

def collection(): pass
def website(): pass

def lexemelink():
    return u"""<emphasis><link linkend="lexeme_%i">%s</link></emphasis>
'%s'"""

def reflink():
    return u"""<link linkend="%s">(%s %s)</link>"""
    

def textlink():
    return u"""<emphasis><link linkend="text_%i">%s</link></emphasis>"""


def glossentry():
    return u"""
<glossentry id="lexeme_%i">
   <glossterm>%s</glossterm>
   <glossdef><para>[<emphasis role="bold">%s</emphasis>] %s.
   %s.
   <emphasis role="bold">Alternative forms: </emphasis><emphasis>%s</emphasis></para>
      <!-- TODO: tags -->
   </glossdef>
</glossentry>
    """

def recordingHeader():
    return """
<table  rowsep="1" colsep="0" frame="sides">
    <title>%s</title>
    <tgroup cols="5">
        <thead>
          <row>
         <entry>Title</entry>
         <entry>Informant</entry>
         <entry>Source</entry>
         <entry>Date recorded</entry>
         <entry>Tape</entry>
         </row>
         </thead>
         <tbody>
"""

def recording(description = False):
    if description:
        return """
    <row id="recording_%(recordingnr)i">
        <entry><ulink url="%(url)s">%(title)s</ulink>
        <footnote><para>%(description)s</para></footnote></entry>
        <entry>%(informant)s</entry>
        <entry>%(source)s</entry>
        <entry>%(recording_date)s</entry>
        <entry>%(tapenr)s</entry>
    </row>
        """
    else:
        return """
    <row id="recording_%(recordingnr)i">
        <entry><ulink url="%(url)s">%(title)s</ulink>
        <entry>%(informant)s</entry>
        <entry>%(source)s</entry>
        <entry>%(recording_date)s</entry>
        <entry>%(tapenr)s</entry>"""        


def scanHeader():
    return """
<table rowsep="1" colsep="0" frame="sides">
    <title>%s</title>
    <tgroup cols="5">
        <thead>
          <row>
         <entry>Title</entry>
         <entry>Manuscript</entry>
         <entry>Page</entry>
         <entry>Date recorded</entry>
         <entry>Size</entry>
         </row>
         </thead>
         <tbody>
"""
def scan(description = False):
    if description:
        return """
    <row id="scan_%(scannr)i">
        <entry><ulink url="%(url)s">%(title)s</ulink>
        <footnote><para>%(description)s</para></footnote></entry>
        <entry>%(manuscript_location)s</entry>
        <entry>%(page)s</entry>
        <entry>%(scan_date)s</entry>
        <entry>%(size)s</entry>
    </row>
"""
    else:
        return """
    <row id="scan_%(scannr)i">
        <entry><ulink url="%(url)s">%(title)s</ulink></entry>
        <entry>%(manuscript_location)s</entry>
        <entry>%(page)s</entry>
        <entry>%(scan_date)s</entry>
        <entry>%(size)s</entry>
    </row>
"""        

def element(lexnr, note):
    s = [u"""<entry><literallayout>"""]
    if note:
        s.append(u"<footnote><para>%(note)s</para></footnote>")
    if lexnr:
        s.append(u"""<link linkend="lexeme_%(lexnr)i">%(text)s</link>""")
    else:
        s.append(u"%(text)s")
    s.append(u"\n%(glosse)s</literallayout></entry>")
    return "".join(s)

def textHeader(r):
    s = []

    if r.url != "" and r.url != None:
        s.append("""<section id="text_%(textnr)i"><title><ulink url="%(url)s">%(title)s</ulink></title>""")
    else:
        s.append("""<section id="text_%(textnr)i"><title>%(title)s</title>""")
    if r.recording or r.scannr or r.transcription_date:
        s.append("""<informaltable frame="none" colsep="0" rowsep="0"><tgroup cols="2"><tbody>""")
        if r.recordingnr:
            s.append("""
        <row>
            <entry><emphasis role="strong">Recording</emphasis></entry>
            <entry><link linkend="recording_%(recordingnr)i">%(recording)s</link></entry>
        </row>""")
        if r.scannr:
            s.append("""
        <row>
            <entry><emphasis role="strong">Manuscript</emphasis></entry>
            <entry><link linkend="scan_%(scannr)i">%(scan)s</link></entry>
        </row>""")
        if r.transcription_date:
            s.append("""
        <row>
            <entry><emphasis role="strong">Date transcribed</emphasis></entry>
            <entry>%(transcription_date)s</entry>
        </row>""")
            
        s.append("</tbody></tgroup></informaltable>")
        
    s.append("<para>%(description)s</para>")
    return u"\n".join(s)

def filter(s):
    """ Filters a plain text and makes it acceptable for docbook """
    if s == None:
        return ""
    s = s.replace(">", "&gt;")
    s = s.replace("<", "&lt;")
    return s

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.15 $"""[11:-2]
