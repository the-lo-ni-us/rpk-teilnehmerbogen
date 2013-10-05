#!/usr/bin/env python
# coding=utf-8

from reportlab.platypus.doctemplate import BaseDocTemplate, _doNothing
from reportlab.pdfgen import canvas

class DokuTemplate(BaseDocTemplate):
    "eeehhhh..."

    outline_levels = (None, 0, 1, 2, 3, 4, 5)
    last_outline_level = None

    def afterFlowable(self, flowable):
        # print("'ve been called for {0}".format(flowable.__class__))
        c = self.canv
        if hasattr(flowable, 'bm_name'):
            # print('    it has attr bm_name: {0}'.format(flowable.bm_name))
            for l,fl in enumerate(self.bm_ables):
                if flowable.bm_name in fl:
                    
                    self._fill_missing_outline_levels(l, flowable.bm_name)
                    
                    c.addOutlineEntry(flowable.bm_title, flowable.bm_name, level=l, closed=l>=1)
                    self.last_outline_level = l

    def _fill_missing_outline_levels(self, level, target):
        cl = self.outline_levels.index(self.last_outline_level)
        while self.outline_levels.index(level) - cl > 1:
            self.canv.addOutlineEntry('-', target, level=cl, closed=cl>=1)
            cl += 1

    def multiBuild(self, flowables,onFirstPage=_doNothing, onLaterPages=_doNothing, canvasmaker=canvas.Canvas):
        BaseDocTemplate.multiBuild(self,flowables, canvasmaker=canvasmaker) 
