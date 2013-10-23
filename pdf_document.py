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
import re, os, random, collections
from time import gmtime, strftime

from pdf_doku_template import DokuTemplate
from structure import structure as STRUCTURE
from pdf_styles import *
import report
from settings import *


class PdfWriter():

  def __init__(self, filename='Doku/Tech-Dok.pdf', prevent_exceptions=False):

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
                                subject = "Subjekt",
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
    mnames = {'multi_select': '-1, 0 oder 1','multi_numeric': u'-1 bis ∞', 'multi_int': 'integer','multi_bool': 'bool'}
    sav_opts_tr = ( ('measure_level', 'Skalierung'),
                    ('column_width', 'Breite'),
                    ('alignment', 'Ausrichtung'),
                    ('var_type', 'Typ'),
                    ('format', 'Format'),
                    ('missing_values', 'fehlende Werte') )


    n = 'DOC_TITLE'
    p =  Paragraph( self.indexed(DOC_TITLE % self.datum, n), styleH )
    p.bm_title = DOC_TITLE % self.datum
    p.bm_name = n
    self.bm_ables[0].append( n )
    self.story.append( p )
    self.story.append( Spacer(1,0.4*cm) )

    together_with_next = None

    for field in STRUCTURE.doc_items:

      fn = str(field.get('fieldname'))

      to_append  = None

      if field['typ'] == 'heading':
        n = str(random.randint(1000, 1000000))
        p = Paragraph( self.indexed(field['title'], n), styleH )
        p.bm_title = field['title']
        p.bm_name = n
        together_with_next =  p
        # self.story.append( p )
        self.bm_ables[1].append( n )
      elif field['typ'] == 'doc_paragraph':
        self.story.append( Paragraph( field['content'], styleText ))
      elif field['typ'] == 'pagebreak':
        self.story.append( PageBreak())
      elif field['typ'] == 'typ_specification':
        t = [ [ Paragraph(u'<font face="courier"><b>%s</b></font><br/><font size="-2">(Häufigkeit: %d)</font>' % (field['title'],
                STRUCTURE.frequency.get(field['title'], 0)), styleText),
                Paragraph(u'<a name="typ_%s" />%s' % (field['title'], field['purpose']), styleText) ] ]
        self.story.append( Table(t, typSpecWidths, None, styleTypSpec, splitByRow=1) )
        self.story.append( Spacer(1,0.3*cm) )
      else:
        first2 = [field.get('number', ''), Paragraph( self.indexed(field['title'], fn), styleText )]
        if field['typ'] == 'int':
          to_append = Table( [ first2 + ['numerisch'] ], fieldTop3, None, styleFieldTop3, 0, 0 )
        elif field['typ'] == 'str':
          to_append = Table( [ first2 + ['string'] ], fieldTop3, None, styleFieldTop3, 0, 0 )
        elif field['typ'] in fmts:
        # elif field['typ'] in ('multi_int','multi_bool'):
          p = Paragraph( self.indexed(field['title'], fn), styleText )
          table = []
          if field['typ'] in ('multi_bool', 'multi_int'):
            fl = [ (n,i) for n,i in enumerate(field['allowance'])]
          else:
            fl = field['allowance']
          for n, item in fl:
            table.append( first2 + [ fmts[field['typ']] % (fn,n), Paragraph(item, styleMult), mnames[field['typ']] ] )
          to_append = Table( table, fieldTop5, None, styleFieldTop5, splitByRow=1 )
        elif field['typ'] == 'dropdown':
          p = Paragraph( self.indexed(field['title'], fn), styleN )
          table = [ first2 + [ Paragraph(item + (n==field['default'] and ' *' or ''), styleMult), n - 1  ] for n, item in enumerate(field['allowance']) ]
          to_append = Table( table, fieldTop4, None, styleFieldTop4, splitByRow=1 )
        elif field['typ'] in ('enumber', 'enum'):
          p = Paragraph( self.indexed(field['title'], str(fn)), styleN )
          table = [ first2 + [ Paragraph(item + (value==field['default'] and ' *' or ''), styleMult), value  ] for value, item in field['allowance'] ]
          to_append = Table( table, fieldTop4, None, styleFieldTop4, splitByRow=1 )
        else:
          print('nicht berücksichtigter Typ %s' % field['typ'])

      if to_append:
        # fl = self._get_child_of_keeptogether(to_append)
        fl = to_append
        # if field['typ'] == 'dropdown':
        #   print('dropdown: {0}'.format(inspect.getmro(fl.__class__)))
        fl.bm_title = str('%s - %s' % (field.get('number',''), fn) if field.get('number','') else fn)
        fl.bm_name = str(fn)
        self.bm_ables[2].append( fn )
        t = [
              [ '', 'Variablenname: %s' % fn, '' ],
              [ '', u'Abkürzung: %s' % fn, '' ],
              [ '',  Paragraph(u'Typ: <font name="courier-bold"><a color="blue" href="#typ_%s">%s</a></font>'
                               % (field['typ'], field['typ']), styleMult) ],
              # ['Datentyp: %s' % field['default'].__class__.__name__, field.get('longname')],
              [ '', 'Vorgabe: {0} {1}'.format( str(field['default']),
                                               field['typ'] in ('multi_int','multi_bool') and 'mehrspaltig' or '' )] ]
        if 'remark' in field:
          t[0][0] = Paragraph(field['remark'], styleN)
        t[0][2] = '\n'.join([ '{0}: {1}'.format(l,c) for l,c in [ (l, field['sav_opts'].get(k, '')) for k,l in sav_opts_tr ]])
        table = Table(t, commonWidths, None, styleCommon, splitByRow=1)
        pre = [ together_with_next ] if together_with_next else []
        self.story.append( KeepTogether( pre + [ to_append, table ] ) )
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
  print PdfWriter().write_pdf()
