#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summenbögen erfassen...
"""
# On Mon, Sep 6, 2010 at 10:15 PM, Hans-Peter Jansen <hpj at urpla.net> wrote:
# 
# > Start browsing the Qt documentation. Yes, it's a bit arkward to ignore the
# > C++ decoration, but after getting used to, you start to enjoy to be able to
# > ignore all the C++ related complexities and regret all those poor C++
# > hackers: hack, compile, link, crash, hack, compile, link, just for entering
# > the event loop two or three hundred microseconds earlier then us (on an
# > average system) when they finally fixed their self created headaches.

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import resources_rc

from widgets import *
from structure import structure as STRUCTURE
from settings import *

class MainWindow(QtGui.QMainWindow):

    typ2class = {'enum': EnumChooser,      # maps 'typ'-property of STRUCTURE-items to widget-classes
                 'multi_bool': MultiChooser,
                 'multi_int': MultiSpinner,
                 'str': Text,
                 'heading': Heading,
                 'int': Spinner,
                 'date': Fake, # DateChooser,
                 'dropdown': Chooser}

    def __init__(self):
        super(MainWindow, self).__init__()

        # config = wx.Config(CONFIG_MAIN_NAME)
        # use_sqlite = config.Read(CONFIG_USE_SQLITE_DB) == 'True'

        centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(centralWidget)

        self.mainVBox = QtGui.QVBoxLayout()
        self.mainHBox = QtGui.QHBoxLayout()
        centralWidget.setLayout(self.mainVBox)

        self.createActions()
        self.createToolBar()
        self.createMainPanel()
        self.mainVBox.addLayout(self.mainHBox)
        self.createRightBox()
        self.createStatusBar()
        self._reset()

    def _reset(self):
        self.participant = None # currently diplayed Participant() or None if none
                                # Changed attributes will only be saved by a session.commit() if 
                                # the session is the same in which the Participant() is created (loaded).
        self.participants_lv.setCurrentIndex(QtCore.QModelIndex()) # sets invalid value (like -1 but much more sophisticated)
        for widg in self.widg_dict.values():
            widg.reset()
        self.Dirty = False
        self.widg_dict['name'].widget.setFocus()

    def createRightBox(self):
        scrolled = QtGui.QScrollArea(self) 
        scrolled.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrolled.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrolled.setWidgetResizable(True)
        self.mainHBox.addWidget(scrolled)
        self.rightInnerBox = QtGui.QWidget(self)
        self.rightGrid = QtGui.QGridLayout()
        self.rightInnerBox.setLayout(self.rightGrid)
        self.widg_dict = {}

        for field in STRUCTURE.cap_items:
            wid = self.typ2class[field['typ']](self.rightInnerBox, self.rightGrid, 
                                               label=field['title'], allowance=field.get('allowance', None), 
                                               default=field.get('default', None))
            if field['typ'] != 'heading':
                self.widg_dict[field['fieldname']] = wid

        scrolled.setWidget(self.rightInnerBox)
        self.rightGrid.setColumnStretch(0, 15)
        self.rightGrid.setColumnStretch(1, 10)

    def createMainPanel(self):
        self.participants_lv = QtGui.QListWidget(self)
        self.participants_lv.setMinimumHeight(500)
        self.participants_lv.setMaximumWidth(300)
        for l,d in {'bla': 5, 'blubb': 56, 'knusper': 2}.items():
            self.participants_lv.addItem(QtGui.QListWidgetItem(l,None, d))
        # self.participants_lv.setCurrentRow(2)
        leftVBox = QtGui.QVBoxLayout()
        leftVBox.addWidget(self.participants_lv)
        buttonBox = QtGui.QHBoxLayout()
        leftVBox.addLayout(buttonBox)
        self.saveButton = QtGui.QPushButton("Speichern", self)
        buttonBox.addWidget(self.saveButton)
        self.deleteButton = QtGui.QPushButton(u"Löschen", self)
        buttonBox.addWidget(self.deleteButton)
        self.newButton = QtGui.QPushButton("Neu", self)
        buttonBox.addWidget(self.newButton)
        self.mainHBox.addLayout(leftVBox)


    def closeEvent(self, event):
        if self.askSave():
            # self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def askSave(self):
        return True

    def test(self, event):
        # from composite_col import CompositeCol
        # v = CompositeCol(*[False,True,True,True,True,False,False,False,False])
        print self.widg_dict['jahr'].set_value('2012')

    def createActions(self):
        self.prefAct = QtGui.QAction(QtGui.QIcon(':icons/application-pkcs7-signature.png'), 
                                     u"&Institutsangaben eingeben", self, 
                                     statusTip=u"'Name des Unterzeichners' und 'Einrichtungs-Code Nr.' eingeben")
        self.savePdfAct = QtGui.QAction(QtGui.QIcon(':icons/application-pdf.png'), 
                                        u"Auswertung als &Pdf", self, 
                                        statusTip=u"Auswertung der Daten im PDF-Format speichern")
        self.saveCsvAct = QtGui.QAction(QtGui.QIcon(':icons/application-vnd.ms-excel.png'), 
                                        u"&CSV exportieren", self, 
                                        statusTip=u"Die Daten im CSV-Format exportieren", triggered=self.test)
        if True: #self.use_sqlite:
            self.saveSqliteAct = QtGui.QAction(QtGui.QIcon(':icons/database.png'), 
                                               u"S&QLite Datei speichern", self, 
                                               statusTip=u"Eine Kopie der internen SQLite Datenbank speichern")
        self.exitAct = QtGui.QAction(QtGui.QIcon(':icons/exit.png'),u"&Beenden", 
                                     self, shortcut="Ctrl+Q",
                                     statusTip=u"Beendet das Programm", triggered=self.close)

        # self.aboutAct = QtGui.QAction("&About", self,
        #         statusTip="Show the application's About box",
        #         triggered=self.about)

    def createToolBar(self):
        self.mainToolBar = self.addToolBar('main')
        self.mainToolBar.setFloatable(False)
        self.mainToolBar.setMovable(False)
        self.mainToolBar.addAction(self.prefAct)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.savePdfAct)
        self.mainToolBar.addAction(self.saveCsvAct)
        self.mainToolBar.addAction(self.saveSqliteAct)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.exitAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def leck(self, event):
        pass

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
