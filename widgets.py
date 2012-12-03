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

class Heading(QtGui.QHBoxLayout):
    def __init__(self, parent, parent_box, **kwargs):
        QtGui.QHBoxLayout.__init__(self)
        self.label = QtGui.QLabel(kwargs['label'], parent, wordWrap=True)
        font = self.label.font()
        font.setPointSize(font.pointSize()+3)
        self.label.setFont(font)
        self.label.setMargin(10)
        # self.label.SetDimensions(0,0,PANEL_WIDTH,0, wx.SIZE_AUTO_HEIGHT)
        self.addWidget(self.label)
        parent_box.addLayout(self)

class MultiSpinner(QtGui.QHBoxLayout):
    def __init__(self, parent, parent_box, **kwargs):
        QtGui.QHBoxLayout.__init__(self)
        self.label = QtGui.QLabel(kwargs['label'], parent, wordWrap=True)
        self.addWidget(self.label)
        grid = QtGui.QGridLayout()
        self.addLayout(grid)
        font = self.label.font()
        font.setPointSize(font.pointSize()-1)
        self.spinners = []
        for i, name in enumerate(kwargs['allowance']):
            label = QtGui.QLabel(name)
            label.setFont(font)
            grid.addWidget(label, i, 0)
            spinner = QtGui.QSpinBox(parent)
            grid.addWidget(spinner, i, 1)
            self.spinners.append(spinner)
        parent_box.addLayout(self)

    def get_value(self):
        return CompositeCol(*[sp.value() for sp in self.spinners])
    def set_value(self, values):
        [sp.setValue(values[i]) for i,sp in enumerate(self.spinners)]
    def reset(self):
        [sp.setValue(0) for sp in self.spinners]

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
        self.widget = QtGui.QSpinBox(parent)
        self.widget.setMinimum(-1)

class Chooser(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QComboBox(parent)
        self.widget.addItems(kwargs['allowance'])
    def get_value(self):
        return self.widget.currentIndex()
    def set_value(self, value):
        self.widget.setCurrentIndex(value)

class EnumChooser(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.values = [i[0] for i in kwargs['allowance']]
        labels = [i[1] for i in kwargs['allowance']]
        self.widget = QtGui.QComboBox(parent)
        self.widget.addItems(labels)
    def get_value(self):
        return self.values[self.widget.currentIndex()]
    # def get_value_tuple(self):
    #     return self.values[self.widget.GetSelection()],self.widget.GetStringSelection()
    def set_value(self, value):
        self.widget.setCurrentIndex(self.values.index(value))

class MultiChooser(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QListWidget(parent)
        self.widget.addItems(kwargs['allowance'])
        self.widget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    def get_value(self):
        return CompositeCol(*[self.widget.item(i).isSelected() for i in range(self.widget.count())])
    def set_value(self, values):
        [self.widget.item(i).setSelected(v) for i,v in enumerate(values)]
    def reset(self):
        [self.widget.item(i).setSelected(False) for i in range(self.widget.count())]

