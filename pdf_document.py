#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import white, black
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph, BaseDocTemplate, PageTemplate, Frame, Table, \
          TableStyle, Spacer, PageBreak, FrameBreak, CondPageBreak, KeepTogether, LongTable
from reportlab.platypus.tableofcontents import SimpleIndex
from reportlab.lib.pagesizes import A4
from reportlab.platypus.doctemplate import ActionFlowable, NextPageTemplate
from reportlab.lib.units import cm, inch, mm
from reportlab.lib import pdfencrypt
import locale
import re, os
from time import gmtime, strftime

from structure import structure as STRUCTURE 
from pdf_styles import *
import report
from settings import *


class PdfWriter():

  def __init__(self, filename='Teil-Dok.pdf', prevent_exceptions=False):

    self.prv_excps = prevent_exceptions
    self.datum = strftime("%d.%m.%Y")
    self.anchors = []
  
    pageFrame = Frame(  12*mm, 10*mm, 18.6*cm, 26.5*cm, showBoundary=0 )

    pageT = PageTemplate(	id = 'seite',
                                frames = [ pageFrame ],
                                onPage = self.headRoutine,
                                pagesize=A4)

    self.doc = BaseDocTemplate( filename,
                                pagesize = A4,
                                pageTemplates = [ pageT ],
                                showBoundary = 0,
                                leftMargin = cm,
                                rightMargin = cm,
                                topMargin = cm,
                                bottomMargin = cm,
                                allowSplitting = 1,
                                title = DOC_TITLE % self.datum,
                                author = "schweesni",
                                subject = "Subjekt",
                                creator = "https://github.com/the-lo-ni-us/bagrpk-summenbogen",
                                producer = "Produzent",
                                keywords = "Schl[sselw;rter",
                                _pageBreakQuick = 0 )

    # pdfencrypt.encryptDocTemplate(self.doc,userPassword='u',ownerPassword='o', 
    #                               canPrint=1, canModify=1, canCopy=1, canAnnotate=1,	
    #                               strength=40) 

    self.story = []

  def write_pdf(self):

    fmts = {'multi_int': DB_FMT_MI, 'multi_bool': DB_FMT_MB}

    self.story.append( Paragraph( DOC_TITLE % self.datum, styleH ))
    self.story.append( Spacer(1,0.4*cm) )

    for field in STRUCTURE.doc_items:
  
      fn = field.get('fieldname')

      if field['typ'] == 'heading':
        self.story.append( Paragraph( field['title'], styleH ))
        to_append = None
      elif field['typ'] == 'doc_paragraph':
        self.story.append( Paragraph( field['content'], styleText ))
        to_append = None
      elif field['typ'] == 'pagebreak':
        self.story.append( PageBreak())
        to_append = None
      elif field['typ'] == 'int':
        to_append = Table( [ [ Paragraph( self.indexed(field['title'], fn), styleN ), 'integer'] ], spaltenAllInTwo, None, styleAllInTwo, 0, 0 )
      elif field['typ'] == 'str':
        to_append = Table( [ [Paragraph(self.indexed(field['title'], fn), styleN), 'string'] ], spaltenAllInTwo, None, styleAllInTwo, 0, 0 )
      elif field['typ'] in ['multi_int','multi_bool']:
        p = Paragraph( self.indexed(field['title'], fn), styleN )
        table = []
        for n, item in enumerate(field['allowance']):
          table.append( [ '',  fmts[field['typ']] % (fn,n), Paragraph(item, styleMult), {'multi_int': 'integer','multi_bool': 'bool'}[field['typ']] ] )
          # table.append( [ '', item ] + [ data[fmts[field['typ']] % (fn,n)][m] for m in range(4) ] )
        table[0][0] = p
        to_append = KeepTogether(Table( table, spaltenAllInFour, None, styleAllInFour, splitByRow=1 ) )
      elif field['typ'] == 'dropdown': 
        p = Paragraph( self.indexed(field['title'], fn), styleN )
        table = [ [ '', Paragraph(item + (n==field['default'] and ' *' or ''), styleMult), n  ] for n, item in enumerate(field['allowance']) ]
        table[0][0] = p
        # print repr(table)
        to_append = KeepTogether(Table( table, spaltenAllInThree, None, styleAllInThree, splitByRow=1 ) )
      elif field['typ'] == 'enum': 
        p = Paragraph( self.indexed(field['title'], fn), styleN )
        table = [ [ '', Paragraph(item + (n==field['default'] and ' *' or ''), styleMult), n  ] for n, item in field['allowance'] ]
        table[0][0] = p
        # print repr(table)
        to_append = KeepTogether(Table( table, spaltenAllInThree, None, styleAllInThree, splitByRow=1 ))
      elif field['typ'] == 'typ_specification': 
        t = [ [ Paragraph(u'<font face="courier"><b>%s</b></font><br/><font size="-2">(Häufigkeit: %d)</font>' % (field['title'],
                    STRUCTURE.frequency.get(field['title'])), styleText), 
                Paragraph(u'<a name="typ_%s" />%s' % (field['title'], field['purpose']), styleText) ] ] 
        self.story.append( Table(t, typSpecWidths, None, styleTypSpec, splitByRow=1) )
        self.story.append( Spacer(1,0.3*cm) )
      else:
        to_append = None
        print('nicht berücksichtigter Typ %s' % field['typ'])

      if to_append:
        self.story.append( to_append )
        t = [ [ Paragraph(u'Typ: <a color="blue" href="#typ_%s">%s</a>' % (field['typ'], field['typ']), styleMult), 'Feldname: %s' % fn, '' ], 
              ['Datentyp: %s' % field['default'].__class__.__name__, field.get('longname')], 
              ['Vorgabe: %s' % str(field['default']), field['typ'] in ('multi_int','multi_bool') and 'mehrspaltig' or ''] ]
        # t = [ [ '', fn, '' ], [type(field['default']), field.get('longname')], [str(field['default']), field['typ'] in ('multi_int','multi_bool') and 'mehrspaltig'] ]
        if 'remark' in field:
          t[0][2] = Paragraph(field['remark'], styleN)
        self.story.append( Table(t, commonWidths, None, styleCommon, splitByRow=1) )
        self.story.append( Spacer(1,0.3*cm) )

    self.story.append( Spacer(1,0.4*cm) )

    anchors = ''.join(['<a href="#%s">%s</a><br />' % (a,a) for a in self.anchors ])

    # self.story.append( Paragraph(anchors, styleText) )

    # index = SimpleIndex(dot=' ') #, headers=headers)
    # self.story.append(index)
 
    if self.prv_excps:
      try:
        self.doc.build(self.story)
        r_val = True
      except:
        r_val = False
        return r_val
    else:
      self.doc.build(self.story) #, canvasmaker=index.getCanvasMaker())

  def indexed(self, words, index_text):
    # return index_text
    self.anchors.append(index_text)
    return '<a name="%s" />%s' % (index_text, words)
    # return '<index item="%s" />%s' % (index_text, words)
    

  def headRoutine (self, c, doc):
    if c.getPageNumber() == 1:
      return
    c.saveState()
    c.setFont( 'Helvetica', 10 )
    c.drawString( 1.5*cm, 28*cm, DOC_TITLE  % self.datum)
    c.drawString( 18.4*cm, 28*cm, "Seite %d" % c.getPageNumber() )
    c.restoreState()
  
if __name__ == '__main__':
  print PdfWriter().write_pdf()
