#!/usr/bin/env python
# coding: utf-8

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

import inspect

import locale
import re, os, random
from time import gmtime, strftime

from pdf_doku_template import DokuTemplate
from structure import structure as STRUCTURE 
from pdf_styles import *
import report
from settings import *


class PdfRaising():

  def __init__(self, filename='Doku/Erfassungsbogen.pdf', participant=None, prevent_exceptions=False):

    self.participant = participant

    self.prv_excps = prevent_exceptions
    self.datum = strftime("%d.%m.%Y")
    self.anchors = []
  
    pageFrame = Frame(  12*mm, 10*mm, 18.6*cm, 26.5*cm, showBoundary=0 )

    pageT = PageTemplate(	id = 'seite',
                                frames = [ pageFrame ],
                                onPage = self.headRoutine,
                                pagesize=A4)

    self.doc = DokuTemplate( filename,
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
                                subject = "Erfassungsbogen",
                                creator = "https://github.com/the-lo-ni-us/bagrpk-summenbogen",
                                producer = "Produzent",
                                keywords = u"Schlüsselwörter",
                                _pageBreakQuick = 0 )

    # pdfencrypt.encryptDocTemplate(self.doc,userPassword='u',ownerPassword='o', 
    #                               canPrint=1, canModify=1, canCopy=1, canAnnotate=1,	
    #                               strength=40) 
    # self.bm_ables = {1: [], 2: []}
    self.bm_ables = ([],[],[])
    self.doc.bm_ables = self.bm_ables
    self.story = []

  def write_pdf(self):

    fmts = {'multi_int': DB_FMT_MI, 'multi_bool': DB_FMT_MB, 'multi_select': DB_FMT_MS, 'multi_numeric': DB_FMT_MN}

    p =  Paragraph( 'Erfassungsbogen', styleH )
    self.story.append( p )
    self.story.append( Spacer(1,0.4*cm) )

    together_with_next = None

    for field in STRUCTURE.cap_items:
  
      fn = str(field.get('fieldname', '')) 
      if self.participant and hasattr(self.participant, fn):
        value = getattr(self.participant, fn)
      else:
        value = ''

      to_append  = None

      if field['typ'] == 'heading':
        n = str(random.randint(1000, 1000000))
        p = Paragraph( self.indexed(field['title'], n), styleH )
        p.bm_title = field['title']
        p.bm_name = n
        together_with_next =  p
        # self.story.append( p )
        self.bm_ables[0].append( n )
      elif field['typ'] == 'pagebreak':
        self.story.append( PageBreak())
      else:
        first3 = [ str(field.get('number', '')), 
                   '{0}/{1}'.format(field['raise_time'],field['raiser']), 
                   Paragraph(self.indexed(field['title'], fn), styleText)
        ]

        if field['typ'] == 'int':
          to_append = Table( [ first3 + [ '', value >= 0 and value or '' ] ], spaltenRaise, None, styleRaise_int, 0, 0 )
        elif field['typ'] == 'str':
          to_append = Table( [ first3 + [ value, '' ] ], spaltenRaise, None, styleRaise_str, 0, 0 )
        elif field['typ'] in fmts:
          if field['typ'] in ('multi_bool', 'multi_int'):
            fl = field['allowance'] 
          else:
            fl = [ v for k,v in field['allowance']]
          if value:
            if field['typ'] in ('multi_bool'):
              vl = [ v and 'x' or '' for v in value ] 
            elif field['typ'] in ('multi_select'):
              vl = [ v > 0 and 'x' or '' for v in value ] 
            else:
              vl = [ v > 0 and v or '' for v in value ]
          else:
            vl = ['' for n in range(len(field['allowance']))]
          # print('{2}; {0},{1}'.format(len(vl),len(fl), fn))
          table = [ first3 + [ Paragraph(item, styleMult), vl[n] ] for n, item in enumerate(fl) ] 
          to_append = Table( table, spaltenRaise, None, styleRaise, splitByRow=1 )
        elif field['typ'] == 'dropdown': 
          table = [ first3 + [ Paragraph(item, styleMult), (n-1 == value and 'x' or '') ] for n, item in enumerate(field['allowance']) ] 
          to_append = Table( table, spaltenRaise, None, styleRaise, splitByRow=1 )
        elif field['typ'] in ('enumber', 'enum'): 
          table = [ first3 + [ Paragraph(item, styleMult), (v == value and 'x' or '') ] for v, item in field['allowance'] ] 
          to_append = Table( table, spaltenRaise, None, styleRaise, splitByRow=1 )
        else:
          # print('nicht berücksichtigter Typ %s' % field['typ'])
          pass

      if to_append:
        fl = to_append
        fl.bm_title = str(fn)
        fl.bm_name = str(fn)
        self.bm_ables[1].append( fn )
        pre = [ together_with_next ] if together_with_next else []
        self.story.append( KeepTogether( pre + [ to_append] ) )
        # self.story.append( KeepTogether( pre + [ to_append, table ] ) )
        self.story.append( Spacer(1,0.3*cm) )
        together_with_next = None

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
      # self.doc.build(self.story, canvasmaker=canvas.Canvas) #, canvasmaker=index.getCanvasMaker())
      self.doc.multiBuild(self.story) #, canvasmaker=index.getCanvasMaker())

  def _get_child_of_keeptogether(self, fl):
    while fl.__class__ == KeepTogether:
      fl = fl._content[0]
    return fl
    
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
  from PyQt4 import QtCore
  import sqlalchemy as sqAl
  from sqlalchemy.orm import sessionmaker as sqAl_sessionmaker
  from participant import Participant
  config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)
  engine = sqAl.create_engine('sqlite:///%s' % config.value(CONFIG_DB_PATH_NAME))
  session = sqAl_sessionmaker(bind=engine)()
  participant = session.query(Participant).filter(Participant.id == 1).first()
  print PdfRaising(participant=participant).write_pdf()
