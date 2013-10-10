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
        self.label = QtGui.QLabel(kwargs['title'], parent, wordWrap=True)
        font = self.label.font()
        font.setPointSize(font.pointSize()+3)
        self.label.setFont(font)
        self.label.setMargin(10)
        parent_grid.addWidget(self.label, self.row, 0, 1, 3)
        GridRow.row += 1

class MultiSpinner(object):
    def __init__(self, parent, parent_grid, **kwargs):
        self.row = GridRow.row
        self.n_label = QtGui.QLabel(kwargs.get('number', ''), parent, wordWrap=False)
        parent_grid.addWidget(self.n_label, self.row, 0, QtCore.Qt.AlignTop)
        self.label = QtGui.QLabel(kwargs['title'], parent, wordWrap=True)
        parent_grid.addWidget(self.label, self.row, 1, QtCore.Qt.AlignTop)
        grid = QtGui.QGridLayout()
        parent_grid.addLayout(grid, self.row, 2)
        font = self.label.font()
        font.setPointSize(font.pointSize()-1)
        self.spinners = []
        for i, name in enumerate(kwargs['allowance']):
            label = QtGui.QLabel(name)
            label.setFont(font)
            grid.addWidget(label, i, 0)
            spinner = QtGui.QSpinBox(parent)
            spinner.setMinimum(-1)
            spinner.setMaximum(1000)
            grid.addWidget(spinner, i, 1)
            self.spinners.append(spinner)
        GridRow.row += 1

    def get_value(self):
        return CompositeCol(*[sp.value() for sp in self.spinners])
    def set_value(self, values):
        for i,sp in enumerate(self.spinners):
            old_state = sp.blockSignals(True)
            sp.setValue(values[i])
            sp.blockSignals(old_state)
    def reset(self):
        [sp.setValue(0) for sp in self.spinners]
    def connect_dirty(self, slot):
        [sp.valueChanged.connect(slot) for sp in self.spinners]

class LabeledWidget():
    def __init__(self, parent, parent_grid, **kwargs):
        self.row = GridRow.row
        self.default = kwargs['default']
        self.n_label = QtGui.QLabel(kwargs.get('number', ''), parent, wordWrap=False)
        parent_grid.addWidget(self.n_label, self.row, 0, QtCore.Qt.AlignTop)
        self.label = QtGui.QLabel(kwargs['title'], parent, wordWrap=True)
        parent_grid.addWidget(self.label, self.row, 1, QtCore.Qt.AlignTop)
        self.add_widget(parent, **kwargs)
        parent_grid.addWidget(self.widget, self.row, 2, QtCore.Qt.AlignTop)
        GridRow.row += 1
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
        self.widget.setMaximum(1000)

class Text(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QLineEdit(parent)
    def get_value(self):
        return unicode(self.widget.text())
    def set_value(self, value):
        self.widget.setText(value)
    def connect_dirty(self, slot):
        self.widget.textEdited.connect(slot)

class Chooser(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QComboBox(parent)
        self.widget.addItems(kwargs['allowance'])
    def get_value(self):
        return self.widget.currentIndex() - 1
    def set_value(self, value):
        self.widget.setCurrentIndex(value + 1)
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

class MultiSelect(LabeledWidget):
    def add_widget(self, parent, **kwargs):
        self.widget = QtGui.QListWidget(parent)
        self.widget.addItems([l for n,l in kwargs['allowance']])
        self.widget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.widget.itemSelectionChanged.connect(self.check_missing)
        self._missing_state = (1,) + tuple(-1 for i in range(1, len(kwargs['allowance'])))
        self.allow_all_zero = kwargs.get('allow_all_zero', False)
        # print(kwargs)
    def get_value(self):
        if self._missing:
            vals = self._missing_state
        else:
            vals = [self.widget.item(i).isSelected() and 1 or 0 for i in range(self.widget.count())]
        return CompositeCol(*vals)
    def set_value(self, values):
        old_state = self.widget.blockSignals(True)
        for i,v in enumerate(values):
            self.widget.item(i).setSelected(v==1)
        self.widget.blockSignals(old_state)
        self._missing = True if tuple(values) == self._missing_state else False
    def reset(self):
        self._missing = True
        old_state = self.widget.blockSignals(True)
        for i,v in enumerate(self._missing_state):
            self.widget.item(i).setSelected(v==1)
        self.widget.blockSignals(old_state)
    def connect_dirty(self, slot):
        self.widget.itemSelectionChanged.connect(slot)
    def check_missing(self):
        set_missing = len(self.widget.selectedItems()) == 0 and not self.allow_all_zero
        # print('set_missing: {0}'.format(set_missing))
        # print('   _missing: {0} -- len(selected): {1}'.format(self._missing, len(self.widget.selectedItems())))
        if self._missing:
            self._missing = set_missing
            old_state = self.widget.blockSignals(True)
            self.widget.item(0).setSelected(set_missing)
            self.widget.blockSignals(old_state)
        elif self.widget.item(0).isSelected() or set_missing:
            self.reset()

class MultiNumeric(MultiSpinner):
    def __init__(self, parent, parent_grid, **kwargs):
        self.row = GridRow.row
        self.n_label = QtGui.QLabel(kwargs.get('number', ''), parent, wordWrap=True)
        parent_grid.addWidget(self.n_label, self.row, 0, QtCore.Qt.AlignTop)
        self.label = QtGui.QLabel(kwargs['title'], parent, wordWrap=True)
        self.allow_all_zero = kwargs.get('allow_all_zero', False)
        parent_grid.addWidget(self.label, self.row, 1, QtCore.Qt.AlignTop)
        grid = QtGui.QGridLayout()
        parent_grid.addLayout(grid, self.row, 2)
        font = self.label.font()
        font.setPointSize(font.pointSize()-1)
        self.spinners = []
        for i, tup in enumerate(kwargs['allowance']):
            label = QtGui.QLabel(tup[1])
            label.setFont(font)
            grid.addWidget(label, i, 0)
            spinner = QtGui.QSpinBox(parent)
            spinner.setMinimum(-1)
            spinner.setMaximum(1000)
            grid.addWidget(spinner, i, 1)
            spinner.valueChanged.connect(self.check_missing)
            self.spinners.append(spinner)
        GridRow.row += 1

    def set_value(self, values):
        for i,sp in enumerate(self.spinners):
            old_state = sp.blockSignals(True)
            sp.setValue(values[i])
            sp.blockSignals(old_state)
        self._missing = set(values) == {-1}
    def reset(self):
        self._missing = True
        for sp in self.spinners:
            old_state = sp.blockSignals(True)
            sp.setValue(-1)
            sp.blockSignals(old_state)
    def connect_dirty(self, slot):
        for sp in self.spinners:
            sp.valueChanged.connect(slot)
    def _zeroify(self):
        for sp in self.spinners:
            if sp.value() == -1:
                old_state = sp.blockSignals(True)
                sp.setValue(0)
                sp.blockSignals(old_state)
    def check_missing(self, value):
        if self._missing:
            zero = None
            if not(self.allow_all_zero):
                vals = self.get_value()
                if vals.count(0):
                  zero = vals.index(0)
            self._zeroify()
            if zero != None:
                old_state = self.spinners[zero].blockSignals(True)
                self.spinners[zero].setValue(1)
                self.spinners[zero].blockSignals(old_state)
            self._missing = False
        else:
            uniq = set(sp.value() for sp in self.spinners)
            if uniq == {-1, 0} or (uniq == {0} and not self.allow_all_zero):
                self.reset()
            elif len(uniq) > 2 and -1 in uniq:
                self._zeroify()
