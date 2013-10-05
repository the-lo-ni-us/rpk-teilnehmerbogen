#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import TableStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color, white, black, green
from reportlab.lib.units import cm, mm

line_width = 0.3
rightcol_color = Color(0.83,0.88,0.73)
rightcol_text_color = black

fmt_std= {'name': 'Normal',
          'fontName': 'Helvetica',
          'fontSize': 10,
          'leading': 12,
          'leftIndent': 0,
          'rightIndent': 0,
          'firstLineIndent': 0,
          'alignment': TA_LEFT,
          'spaceBefore': 0,
          'spaceAfter': 12,
          'textColor': black,
          'backColor': None}

styleText = ParagraphStyle(**fmt_std)

hanging = 18
fmt_std_tab = {'name': 'Normal',
               'fontName': 'Helvetica',
               'fontSize': 9,
               'leading': 11,
               'leftIndent': hanging,
               'rightIndent': 0,
               'firstLineIndent': -hanging,
               'alignment': TA_LEFT,
               'spaceBefore': 0,
               'spaceAfter': 0,
               'bulletFontName': 'Helvetica',
               'bulletFontSize': 10,
               'bulletIndent': 0,
               'textColor': black,
               'backColor': None}

styleN = ParagraphStyle(**fmt_std_tab)

fmt_mult = fmt_std.copy()
hanging2 = 18
fmt_mult.update(fontSize = 9,
                leading = 11,
                spaceBefore = 2,
                spaceAfter = 2,
                leftIndent = hanging2,
                firstLineIndent = -hanging2)

styleMult = ParagraphStyle(**fmt_mult)

styleH = ParagraphStyle(name='Normal-Heading',
            fontName = 'Helvetica-Bold',
            fontSize = 13,
            leading = 14,
            leftIndent = 0,
            rightIndent = 0,
            firstLineIndent = 0,
            alignment = TA_LEFT,
            spaceBefore = 8 * mm,
            spaceAfter = 6 * mm,
            textColor =  black,
            backColor = None )

spaltenBreiten = [ 8*cm, 10.4*cm ]

spaltenInner = [ 6*cm, 1*cm, 1*cm, 0.6*cm, 1*cm ]

stdTablePadding = (
    ('LEFTPADDING',   (0,0), (-1,-1), 3),
    ('RIGHTPADDING',  (0,0), (-1,-1), 4),
    ('TOPPADDING',    (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0)
)

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

spaltenAllInFour = [ 6*cm, 2.4*cm, 8*cm, 1.6*cm ]

styleAllInFour = [  ('SPAN',          (0,0), (0,-1)), 
                    ('ALIGN',         (0,0), (1,-1), 'LEFT'), 
                    ('VALIGN',        (0,0), (1,-1), 'TOP'),
                    ('ALIGN',         (1,0), (3,-1), 'CENTER'),
                    ('VALIGN',        (1,0), (3,-1), 'MIDDLE'),
                    ('FONTSIZE',      (0,0), (-1,-1), 9 ),
                    # ('BACKGROUND',    (2,0), (3,-1),  Color(0,0.4,0.4)),
                    # ('TEXTCOLOR',     (2,0), (3,-1),  white),
                    ('INNERGRID',     (0,0), (-1,-1), 0.3, black), 
                    ('BOX',           (0,0), (-1,-1), 0.3, black), 
                    ('LEFTPADDING',   (0,0), (-1,-1), 3),
                    ('RIGHTPADDING',  (0,0), (-1,-1), 4),
                    ('TOPPADDING',    (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
                    ('LEFTPADDING',   (0,0), ( 0, 0), 6),
                    ('RIGHTPADDING',  (0,0), ( 0, 0), 6),
                    ('TOPPADDING',    (0,0), ( 0, 0), 3),
                    ('BOTTOMPADDING', (0,0), ( 0, 0), 3) ]

styleAllInFour2 = [ ('SPAN',          (0,0), (0,-1)), 
                    ('SPAN',          (1,0), (1,-1)), 
                    ('ALIGN',         (0,0), (1,-1), 'LEFT'), 
                    ('VALIGN',        (0,0), (1,-1), 'TOP'),
                    ('ALIGN',         (1,0), (3,-1), 'CENTER'),
                    ('FONTSIZE',      (0,0), (-1,-1), 9 ),
                    ('VALIGN',        (1,0), (3,-1), 'MIDDLE'),
                    ('INNERGRID',     (0,0), (-1,-1), 0.3, black), 
                    ('BOX',           (0,0), (-1,-1), 0.3, black), 
                    ('LEFTPADDING',   (0,0), (-1,-1), 3),
                    ('RIGHTPADDING',  (0,0), (-1,-1), 4),
                    ('TOPPADDING',    (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
                    ('LEFTPADDING',   (0,0), ( 0, 0), 6),
                    ('RIGHTPADDING',  (0,0), ( 0, 0), 6),
                    ('TOPPADDING',    (0,0), ( 0, 0), 3),
                    ('BOTTOMPADDING', (0,0), ( 0, 0), 3) ]

spaltenAllInTwo = [ 16.4*cm, 1.6*cm ]

styleAllInTwo = [ ('ALIGN',         (0,0), (0,-1), 'LEFT'), 
                    ('VALIGN',        (0,0), (0,-1), 'TOP'),
                    ('ALIGN',         (1,0), (1,-1), 'CENTER'),
                    ('VALIGN',        (1,0), (1,-1), 'MIDDLE'),
                    ('FONTSIZE',      (0,0), (-1,-1), 9 ),
                    ('INNERGRID',     (0,0), (-1,-1), 0.3, black), 
                    ('BOX',           (0,0), (-1,-1), 0.3, black), 
                    ('LEFTPADDING',   (0,0), (-1,-1), 3),
                    ('RIGHTPADDING',  (0,0), (-1,-1), 4),
                    ('TOPPADDING',    (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
                    ('LEFTPADDING',   (0,0), ( 0, 0), 6),
                    ('RIGHTPADDING',  (0,0), ( 0, 0), 6),
                    ('TOPPADDING',    (0,0), ( 0, 0), 3),
                    ('BOTTOMPADDING', (0,0), ( 0, 0), 3) ]

spaltenAllInThree = [ 8.4*cm, 8*cm, 1.6*cm ]

styleAllInThree = [ ('SPAN',          (0,0), (0,-1)), 
                    ('ALIGN',         (0,0), (1,-1), 'LEFT'), 
                    ('VALIGN',        (0,0), (1,-1), 'TOP'),
                    ('ALIGN',         (1,0), (2,-1), 'CENTER'),
                    ('VALIGN',        (1,0), (2,-1), 'MIDDLE'),
                    ('FONTSIZE',      (0,0), (-1,-1), 9 ),
                    ('INNERGRID',     (0,0), (-1,-1), 0.3, black), 
                    ('BOX',           (0,0), (-1,-1), 0.3, black), 
                    ('LEFTPADDING',   (0,0), (-1,-1), 3),
                    ('RIGHTPADDING',  (0,0), (-1,-1), 4),
                    ('TOPPADDING',    (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0), 
                    ('LEFTPADDING',   (0,0), ( 0, 0), 6),
                    ('RIGHTPADDING',  (0,0), ( 0, 0), 6),
                    ('TOPPADDING',    (0,0), ( 0, 0), 3),
                    ('BOTTOMPADDING', (0,0), ( 0, 0), 3) ]

commonWidths = [ 4.2*cm, 4.2*cm, 9.6*cm ]

styleCommon = ( ('SPAN',          (2,0), (2,-1)), 
                ('ALIGN',         (0,0), (1,-1), 'LEFT'), 
                ('VALIGN',        (0,0), (1,-1), 'TOP'),
                ('ALIGN',         (1,0), (2,-1), 'CENTER'),
                ('VALIGN',        (1,0), (2,-1), 'MIDDLE'),
                ('INNERGRID',     (0,0), (-1,-1), 0.3, black), 
                ('BOX',           (0,0), (-1,-1), 0.3, black), 
                ('FONTSIZE',      (0,0), (-1,-1), 9 ),
                ('LEFTPADDING',   (0,0), ( 0, 0), 6),
                ('RIGHTPADDING',  (0,0), ( 0, 0), 6),
                ('TOPPADDING',    (0,0), ( 0, 0), 3),
                ('BOTTOMPADDING', (0,0), ( 0, 0), 3) )

typSpecWidths = [ 3.5*cm, 14.5*cm ]

styleTypSpec = ( ('SPAN',          (1,0), (1,-1)), 
                ('ALIGN',         (0,0), (1,-1), 'LEFT'), 
                ('VALIGN',        (0,0), (1,-1), 'TOP'),
                # ('ALIGN',         (1,0), (2,-1), 'CENTER'),
                # ('VALIGN',        (1,0), (2,-1), 'MIDDLE'),
                # ('INNERGRID',     (0,0), (-1,-1), 0.3, black), 
                # ('BOX',           (0,0), (-1,-1), 0.3, black), 
                ('FONTSIZE',      (0,0), (-1,-1), 9 ),
                ('LEFTPADDING',   (0,0), ( 0, 0), 6),
                ('RIGHTPADDING',  (0,0), ( 0, 0), 6),
                ('TOPPADDING',    (0,0), ( 0, 0), 3),
                ('BOTTOMPADDING', (0,0), ( 0, 0), 3) )

###################   RAISING   ######################

grid_borders = ( ('INNERGRID', (0,0), (-1,-1), line_width, black), 
                 ('BOX',       (0,0), (-1,-1), line_width, black) )

paddings = (('LEFTPADDING',   (0,0), (-1,-1), 3),
            ('RIGHTPADDING',  (0,0), (-1,-1), 6),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0))

vspan_first2 = ( ('SPAN', (0,0), (0,-1)), 
                 ('SPAN', (1,0), (1,-1)) )

vspan_3 = ( ('SPAN', (2,0), (2,-1)) ,)

span_3_4 = ( ('SPAN', (2,0), (3,-1)) ,)

span_4_5 = ( ('SPAN', (3,0), (4,-1)) ,)

align_right_5 = ( ('ALIGN',  (4,0), (4,-1), 'RIGHT') ,)

align_center_5 = ( ('ALIGN',  (4,0), (4,-1), 'CENTER') ,)

valign_top_c1 = (  ('VALIGN', (0,0), (0,-1), 'TOP') ,)

valign_top_c1_2_3 = (  ('VALIGN', (0,0), (2,-1), 'TOP') ,)

valign_middle_c1 = (  ('VALIGN', (0,0), (0,-1), 'MIDDLE') ,)


colorize_4 = ( ('BACKGROUND', (3,0), (3,-1),  rightcol_color),
               ('TEXTCOLOR',  (3,0), (3,-1),  rightcol_text_color) )

colorize_5 = ( ('BACKGROUND', (4,0), (4,-1),  rightcol_color),
               ('TEXTCOLOR',  (4,0), (4,-1),  rightcol_text_color) )

raiseFirst3 = ( 1*cm, 2*cm, 6*cm )

spaltenRaise4 = raiseFirst3 + ( 10*cm, )

styleRaise4 = vspan_first2 + colorize_4 + grid_borders + paddings

spaltenRaise = raiseFirst3 + ( 7.5*cm, 1.5*cm )

styleRaise_str = vspan_first2 + vspan_3 + valign_top_c1_2_3 + span_4_5 + colorize_4 + grid_borders + paddings + align_center_5

styleRaise_int = vspan_first2 + vspan_3 + valign_top_c1_2_3 + span_3_4 + colorize_5 + grid_borders + paddings + align_center_5

styleRaise = vspan_first2 + vspan_3 + valign_top_c1_2_3 + colorize_5 + grid_borders + paddings + align_center_5

if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4).pprint
    pp(styleRaise_str)
