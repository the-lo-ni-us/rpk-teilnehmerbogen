#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The classes here are designed to get_value()/set_value() what the
Participant() ORM-class expects/returns for/from its various kinds
of columns.
"""

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import datetime
from composite_col import CompositeCol
from settings import *

class Fake():
    def __init__(self, parent, parent_grid, **kwargs):
        pass
    def reset(self):
        pass

class GridRow():
    row = 0
    # def __init__(self, grid_layout):
    #     self.row = grid_layout.rowCount()

class Heading():
    def __init__(self, parent, parent_grid, **kwargs):
        self.row = GridRow.row
        self.label = QtGui.QLabel(kwargs['label'], parent, wordWrap=True)
        font = self.label.font()
        font.setPointSize(font.pointSize()+3)
        self.label.setFont(font)
        self.label.setMargin(10)
        # self.label.SetDimensions(0,0,PANEL_WIDTH,0, wx.SIZE_AUTO_HEIGHT)
        parent_grid.addWidget(self.label, self.row, 0, 1, 2)
        GridRow.row += 1

class MultiSpinner():
    def __init__(self, parent, parent_grid, **kwargs):
        self.row = GridRow.row
        self.label = QtGui.QLabel(kwargs['label'], parent, wordWrap=True)
        parent_grid.addWidget(self.label, self.row, 0)
        grid = QtGui.QGridLayout()
        parent_grid.addLayout(grid, self.row, 1)
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
        GridRow.row += 1

    def get_value(self):
        return CompositeCol(*[sp.value() for sp in self.spinners])
    def set_value(self, values):
        [sp.setValue(values[i]) for i,sp in enumerate(self.spinners)]
    def reset(self):
        [sp.setValue(0) for sp in self.spinners]
    def connect_dirty(self, slot):
        [sp.valueChanged.connect(slot) for sp in self.spinners]

class LabeledWidget():
    def __init__(self, parent, parent_grid, **kwargs):
        self.row = GridRow.row
        self.default = kwargs['default']
        self.label = QtGui.QLabel(kwargs['label'], parent, wordWrap=True)
        # self.label.SetDimensions(0,0,LABEL_WIDTH,0, wx.SIZE_AUTO_HEIGHT)
        parent_grid.addWidget(self.label, self.row, 0)
        self.add_widget(parent, **kwargs)
        parent_grid.addWidget(self.widget, self.row, 1)
        GridRow.row += 1
        # self.widget.SetDimensions(0,0,WIDGET_WIDTH,0, wx.SIZE_AUTO_HEIGHT)
    def add_widget(self, parent, **kwargs):
        pass
    def get_value(self):
        return self.widget.value()
    def set_value(self, value):
        self.widget.setValue(value)
    def reset(self):
        self.set_value(self.default)
    def connect_dirty(self, slot):
        self.widget.valueChanged.connect(slot)

class Spinner(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QSpinBox(parent)
        self.widget.setMinimum(-1)

class Text(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QLineEdit(parent)
    def get_value(self):
        return self.widget.text()
    def set_value(self, value):
        self.widget.setText(value)
    def connect_dirty(self, slot):
        self.widget.textEdited.connect(slot)

class Chooser(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QComboBox(parent)
        self.widget.addItems(kwargs['allowance'])
    def get_value(self):
        return self.widget.currentIndex()
    def set_value(self, value):
        self.widget.setCurrentIndex(value)
    def connect_dirty(self, slot):
        self.widget.currentIndexChanged.connect(slot)

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
    def connect_dirty(self, slot):
        self.widget.currentIndexChanged.connect(slot)

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
    def connect_dirty(self, slot):
        self.widget.itemSelectionChanged.connect(slot)

