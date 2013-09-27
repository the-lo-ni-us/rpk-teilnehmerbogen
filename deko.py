#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication

modies = { 'shift': Qt.ShiftModifier,
           'control': Qt.ControlModifier,
           'alt': Qt.AltModifier,
           'meta': Qt.MetaModifier }

def check_modifiers(org_meth):
    """Add modifiers kwarg to a method that contains a tuple of currently pressed modifiers."""

    def check_modifiers(*args, **kwargs):
        curr = QApplication.keyboardModifiers()
        kwargs['modifiers'] = tuple( name for name, which in modies.items() if curr & which == which )

        org_meth.__call__(*args, **kwargs)

    return check_modifiers


if __name__ == '__main__':

    import sip
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore

    class MainWindow(QtGui.QMainWindow):

        def __init__(self):
            super(MainWindow, self).__init__()


            centralWidget = QtGui.QWidget(self)
            layout = QtGui.QHBoxLayout(centralWidget)
            self.setCentralWidget(centralWidget)
            self.clickButton = QtGui.QPushButton("click", centralWidget)
            self.clickButton.clicked.connect(self.klick)
            layout.addWidget(self.clickButton)
            self.statusBar()

        @check_modifiers
        def klick(self, event, modifiers):
            self.statusBar().showMessage( repr(modifiers) + " has been pressed")
            
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
