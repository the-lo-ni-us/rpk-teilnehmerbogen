#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import white, black
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph, BaseDocTemplate, PageTemplate, Frame, Table, \
          TableStyle, Spacer, PageBreak, FrameBreak, CondPageBreak, KeepTogether, LongTable
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

  def __init__(self, filename='test.pdf', year=None):
    if not(year):
      year = {'': u'Teilnahme noch nicht beendet', None: u'alle (inkl. nicht beendete)'}[year]
    self.year = year

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
                                title = PDF_TITLE % self.year,
                                author = "schweesni",
                                subject = "Subjekt",
                                creator = "https://github.com/the-lo-ni-us/bagrpk-summenbogen",
                                producer = "Produzent",
                                keywords = "Schl[sselw;rter",
                                _pageBreakQuick = 0 )

    # pdfencrypt.encryptDocTemplate(self.doc,userPassword='u',ownerPassword='o', 
    #                               canPrint=1, canModify=1, canCopy=1, canAnnotate=1,	
    #                               strength=40) 

    datum = strftime("%d.%m.%Y")
  
    self.story = []

  def write_pdf(self):

    fmts = {'multi_int': DB_FMT_MI, 'multi_bool': DB_FMT_MB}

    self.story.append( Paragraph( PDF_TITLE % self.year, styleH ))

    col_cap = Table( [['','Medizinisch','','Teilnahme',''],
                      ['','planm.','vorz.','planm.','vorz.']], spaltenInner, None, styleInnerHeading, 0, 0 )

    self.story.append( Table( [ [ '', col_cap ] ], spaltenBreiten, None, styleOuter, 0, 0 ) )

    for field in STRUCTURE.tab_items:
  
      if field.has_key('fieldname'):
        fn = field['fieldname']

      if field['typ'] == 'heading':
        self.story.append( Paragraph( field['title'], styleH ))
      elif field['typ'] == 'int':
        r_fields = ['%0.1f' % n for n in range(4)]
        self.story.append( Table( [ [ Paragraph( field['title'], styleN ), '', ] + r_fields ], spaltenAllInSix, None, styleAllInSix, 0, 0 ) )
      elif field['typ'] == 'str':
        self.story.append( Table( [ [Paragraph(field['title'], styleN), 'nix'] ], spaltenBreiten, None, styleOuter, 0, 0 ) )
      elif field['typ'] in ['multi_int','multi_bool']:
        t = Paragraph( field['title'], styleN )
        table = []
        for n, item in enumerate(field['allowance']):
          table.append( [ '', item ] + [ fmts[field['typ']] % (fn,n)  for m in range(4) ] )
          # table.append( [ '', item ] + [ data[fmts[field['typ']] % (fn,n)][m] for m in range(4) ] )
        table[0][0] = t
        self.story.append( KeepTogether(Table( table, spaltenAllInSix, None, styleAllInSix, splitByRow=1 ) ))
      elif field['typ'] == 'dropdown': 
        t = Paragraph( field['title'], styleN )
        table = [ [ '', item, n , n , n , n ] for n, item in enumerate(field['allowance']) ]
        table[0][0] = t
        # print repr(table)
        self.story.append( KeepTogether(Table( table, spaltenAllInSix, None, styleAllInSix, splitByRow=1 ) ))

    self.story.append( Spacer(1,0.3*cm) )
 
    # self.doc.build(self.story)
    try:
      self.doc.build(self.story)
      r_val = True
    except:
      r_val = False
    return r_val

  def headRoutine (self, c, doc):
    if c.getPageNumber() == 1:
      return
    c.saveState()
    c.setFont( 'Helvetica', 10 )
    c.drawString( 1.5*cm, 28*cm, PDF_TITLE  % self.year)
    c.drawString( 18.4*cm, 28*cm, "Seite %d" % c.getPageNumber() )
    c.restoreState()
  
if __name__ == '__main__':
  print PdfWriter(year=u'2012').write_pdf()
