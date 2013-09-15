#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import TableStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color, white, black, green
from reportlab.lib.units import cm, mm

styleN = ParagraphStyle(name='Normal',
            fontName = 'Helvetica',
            fontSize = 11,
            leading = 12,
            leftIndent = 0,
            rightIndent = 0,
            firstLineIndent = 0,
            alignment = TA_LEFT,
            spaceBefore = 0,
            spaceAfter = 0,
            bulletFontName = 'Helvetica',
            bulletFontSize = 10,
            bulletIndent = 0,
            textColor =  black,
            backColor = None )

styleH = ParagraphStyle(name='Normal',
            fontName = 'Helvetica-Bold',
            fontSize = 13,
            leading = 14,
            leftIndent = 0,
            rightIndent = 0,
            firstLineIndent = 0,
            alignment = TA_LEFT,
            spaceBefore = 8 * mm,
            spaceAfter = 2 * mm,
            textColor =  black,
            backColor = None )

spaltenBreiten = [ 8*cm, 10.4*cm ]

spaltenInner = [ 6*cm, 1*cm, 1*cm, 1*cm, 1*cm ]

styleInnerHeading = [  ('SPAN',         (1,0), (2,0)), 
                       ('SPAN',         (3,0), (4,0)),
                       ('ALIGN',        (0,0), (-1,-1), 'CENTER'), 
                       ('INNERGRID',    (1,0), ( 4,-1), 0.25, black), 
                       ('LEFTPADDING', 	(0,0), (-1,-1), 0),
                       ('RIGHTPADDING', (0,0), (-1,-1), 0),
                       ('TOPPADDING',   (0,0), (-1,-1), 0),
                       ('BOTTOMPADDING',(0,0), (-1,-1), 2),
                       ('FONT',	        (0,0), (-1,-1), 'Helvetica', 8, 8 )]

styleInner = [  ('ALIGN',         (0,0), (0,-1), 'LEFT'), 
                ('ALIGN',         (1,0), (4,-1), 'RIGHT'),
                ('INNERGRID',     (0,0), (-1,-1), 0.25, black), 
                ('BOX',           (0,0), (-1,-1), 0.25, black), 
                ('LEFTPADDING',   (0,0), (-1,-1), 3),
                ('RIGHTPADDING',  (0,0), (-1,-1), 6),
                ('TOPPADDING',    (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0) ]

styleOuter = [  ('ALIGN', (0,0),(0,-1), 'LEFT'), 
                ('ALIGN', (1,0),(1,-1), 'RIGHT'),
                ('VALIGN',(0,0), (-1,-1), 'TOP'),
                # ('INNERGRID',     (0,0), (-1,-1), 0.25, black), 
                # ('BOX',           (0,0), (-1,-1), 0.25, black), 
                ('TOPPADDING',(0,0), (0,-1), 2), # since reportlab 2.3 for cells with a paragraph
                ]

spaltenAllInSix = [ 6*cm, 8*cm, 1*cm, 1*cm, 1*cm, 1*cm ]

styleAllInSix = [  ('SPAN',          (0,0), (0,-1)), 
                   ('ALIGN',         (0,0), (1,-1), 'LEFT'), 
                   ('VALIGN',        (0,0), (1,-1), 'TOP'),
                   ('ALIGN',         (2,0), (5,-1), 'RIGHT'),
                   ('VALIGN',        (2,0), (5,-1), 'MIDDLE'),
                   ('BACKGROUND',    (2,0), (5,-1),  Color(0,0.4,0.4)),
                   ('TEXTCOLOR',     (2,0), (5,-1),  white),
                   ('INNERGRID',     (0,0), (-1,-1), 1, black), 
                   ('BOX',           (0,0), (-1,-1), 1, black), 
                   ('LEFTPADDING',   (0,0), (-1,-1), 3),
                   ('RIGHTPADDING',  (0,0), (-1,-1), 6),
                   ('TOPPADDING',    (0,0), (-1,-1), 0),
                   ('BOTTOMPADDING', (0,0), (-1,-1), 0) ]

