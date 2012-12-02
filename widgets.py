#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import datetime
from composite_col import CompositeCol
from settings import *

class Fake():
    def __init__(self, parent, parent_box, **kwargs):
        pass
    def reset(self):
        pass


class LabeledWidget(QtGui.QHBoxLayout):
    def __init__(self, parent, parent_box, **kwargs):
        QtGui.QHBoxLayout.__init__(self)
        self.default = kwargs['default']
        self.label = QtGui.QLabel(kwargs['label'], parent, wordWrap=True)
        # self.label.SetDimensions(0,0,LABEL_WIDTH,0, wx.SIZE_AUTO_HEIGHT)
        self.addWidget(self.label)
        self.add_widget(parent, **kwargs)
        self.addWidget(self.widget)
        # self.widget.SetDimensions(0,0,WIDGET_WIDTH,0, wx.SIZE_AUTO_HEIGHT)
        parent_box.addLayout(self)
    def add_widget(self, parent, **kwargs):
        pass
    def get_value(self):
        return self.widget.value()
    def set_value(self, value):
        self.widget.setValue(value)
    def reset(self):
        self.set_value(self.default)

class Text(LabeledWidget):
    def __init__(self, parent, parent_sizer, **kwargs):
        LabeledWidget.__init__(self, parent, parent_sizer, **kwargs)
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QLineEdit(parent)
    def get_value(self):
        return self.widget.text()
    def set_value(self, value):
        self.widget.setText(value)

class Spinner(LabeledWidget):
    def __init__(self, parent, parent_sizer, **kwargs):
        LabeledWidget.__init__(self, parent, parent_sizer, **kwargs)
    def add_widget(self, parent, **kwargs):
        # self.widget = QtGui.QSpinBox(parent, -1, value=str(kwargs['value']), min=-1, max=1000000000)
        self.widget = QtGui.QSpinBox(parent)
        self.widget.setMinimum(-1)

class Chooser(LabeledWidget):
    def __init__(self, parent, parent_sizer, **kwargs):
        LabeledWidget.__init__(self, parent, parent_sizer, **kwargs)
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QComboBox(parent)
        # self.widget = QtGui.QListWidget(parent)
        self.widget.addItems(kwargs['allowance'])
    def get_value(self):
        return self.widget.currentIndex()
    def set_value(self, value):
        self.widget.setCurrentIndex(value)

