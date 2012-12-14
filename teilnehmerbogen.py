#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import os, collections

import resources_rc

from widgets import *
from dialog_prefs import PrefsDialog
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

        self.config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)
        self.use_sqlite = self.config.value(CONFIG_USE_SQLITE_DB) != QtCore.QString(u'false')

        centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(centralWidget)

        self.mainVBox = QtGui.QVBoxLayout()
        self.mainHBox = QtGui.QHBoxLayout()
        centralWidget.setLayout(self.mainVBox)

        self.setWindowTitle(CONFIG_MAIN_NAME)
        self.setWindowIcon(QtGui.QIcon(':icons/python.ico'))
        self.createActions()
        self.createToolBar()
        self.createMainPanel()
        self.mainVBox.addLayout(self.mainHBox)
        self.createRightBox()
        self.createStatusBar()
        self.wire()
        self._reset()
        if self.config.value('geometry'):
            self.restoreGeometry(self.config.value('geometry')) #.toByteArray())
        # QtGui.QMessageBox.information(self,
        #         "Bitte beachten", u"""<p>Dies ist eine Vorabversion, die nicht für den produktiven Einsatz geeignet ist.</p>
        #          <p>Dieses Programm steht unter der <a href='http://www.gnu.org/licenses/gpl-3.0'>GPLv3</a> und die Quellen 
        #          sind auf <a href='https://github.com/the-lo-ni-us/bagrpk-summenbogen'>github.com</a> jedermann zugänglich.</p>
        #          <p>&copy; 2012 Thelonius Kort</p>""")

    def wire(self):
        for w in self.widg_dict.values():
            w.connect_dirty(self.set_dirty)
        self.newButton.clicked.connect(self._reset)
        self.participants_lv.itemClicked.connect(self.load_participant)

    def load_participant(self, item):
        print item.type()

    def set_dirty(self, e=None):
        self.Dirty = True
        # print 'set dirty'

    def _reset(self):
        self.participant = None # currently diplayed Participant() or None when none
                                # Changed attributes will only be saved by a session.commit() if 
                                # session is the same in which the Participant() is created (loaded).
        self.participants_lv.setCurrentIndex(QtCore.QModelIndex()) # sets invalid value (like -1 but much more sophisticated)
        for widg in self.widg_dict.values():
            widg.reset()
        self.Dirty = False
        self.widg_dict['name'].widget.setFocus()
        # print 'set clean'

    def createRightBox(self):
        scrolled = QtGui.QScrollArea(self) 
        scrolled.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrolled.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrolled.setWidgetResizable(True)
        self.mainHBox.addWidget(scrolled)
        self.rightInnerBox = QtGui.QWidget(self)
        self.rightGrid = QtGui.QGridLayout()
        self.rightGrid.setVerticalSpacing(10)
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
        # scrolled.adjustSize()

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
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def askSave(self, message_title='Datensatz speichern?'):
        if not self.Dirty:
            return True
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                message_title, 'Soll gespeichert werden?',
                QtGui.QMessageBox.NoButton, self)
        sb = msgBox.addButton("&Speichern", QtGui.QMessageBox.AcceptRole)
        dsb = msgBox.addButton("&Nicht speichern", QtGui.QMessageBox.DestructiveRole)
        cb = msgBox.addButton("&Abbrechen", QtGui.QMessageBox.NoRole)
        msgBox.setEscapeButton(cb)
        msgBox.exec_()
        reply = msgBox.clickedButton()
        print 'reply: %s' % reply
        if reply == cb:
            return False
        elif reply == sb:
            self._save_participant()
        return True

    def _save_participant(self):
        print 'shoulda be saved'

    def writeSettings(self):
        self.config.setValue('geometry', self.saveGeometry())

    def test(self, event):
        # from composite_col import CompositeCol
        # v = CompositeCol(*[False,True,True,True,True,False,False,False,False])
        print self.widg_dict['jahr'].set_value('2012')

    def years_dict(self):
        """
        Returns an OrderedDict with values None, '', and years as strings (for four years back),
        and the indexes of current year and the year a half year back in the dict.
        """
        now = datetime.date.today()
        half_year_back = now - datetime.timedelta(days=182)
        this_year = now.year
        jahre = [(u'alle erfassten', None),( u'ungewiss', '')]
        jahre += [(str(i), str(i)) for i in reversed(range(this_year-3, this_year+1))]
        return collections.OrderedDict([(QtCore.QString(i[0]),i[1]) for i in jahre]), 2, 2 + (this_year - half_year_back.year)

    def save_pdf(self):
        if not self.askSave():
            return 1
        items, nyi, byi = self.years_dict()
        item, ok = QtGui.QInputDialog.getItem(self, u"Auf Jahr einschränken", u"Auswertung beschränken auf:", items.keys(), byi, False)
        jahr = items[item]
        if not ok:
            return 1

        path = QtGui.QFileDialog.getSaveFileName(self,
                                          "Pdf Auswertung/Zusammenfassung speichern unter...",
                                          os.path.join(str(self.config.value(CONFIG_LAST_SAVE_DIR,'')), 'Summenbogen.pdf'),
                                          "Pdf-Dateien(*.pdf);; Alle Dateien (*)")
        # print '%s - %s' % (path, os.path.dirname(str(path)))
        if path:
            self.config.setValue(CONFIG_LAST_SAVE_DIR, os.path.dirname(str(path)))

    def createActions(self):
        self.prefAct = QtGui.QAction(QtGui.QIcon(':icons/application-pkcs7-signature.png'), 
                                     u"&Institutsangaben eingeben", self, 
                                     statusTip=u"'Name des Unterzeichners' und 'Einrichtungs-Code Nr.' eingeben", triggered=self.dialog_prefs)
        self.savePdfAct = QtGui.QAction(QtGui.QIcon(':icons/application-pdf.png'), 
                                        u"Auswertung als &Pdf", self, 
                                        statusTip=u"Auswertung der Daten im PDF-Format speichern", triggered=self.save_pdf)
        self.saveCsvAct = QtGui.QAction(QtGui.QIcon(':icons/application-vnd.ms-excel.png'), 
                                        u"&CSV exportieren", self, 
                                        statusTip=u"Die Daten im CSV-Format exportieren", triggered=self.test)
        if self.use_sqlite:
            self.saveSqliteAct = QtGui.QAction(QtGui.QIcon(':icons/database.png'), 
                                               u"S&QLite Datei speichern", self, 
                                               statusTip=u"Eine Kopie der internen SQLite Datenbank speichern")
        self.exitAct = QtGui.QAction(QtGui.QIcon(':icons/exit.png'),u"&Beenden", 
                                     self, shortcut="Ctrl+Q",
                                     statusTip=u"Beendet das Programm", triggered=self.close)

        # self.aboutAct = QtGui.QAction("&About", self,
        #         statusTip="Show the application's About box",
        #         triggered=self.about)

    def space_widget(self): # should become a class
        space = QtGui.QWidget(self)
        spacel = QtGui.QHBoxLayout()
        space.setLayout(spacel)
        spacel.addStretch()
        return space

    def createToolBar(self):
        self.mainToolBar = self.addToolBar('main')
        self.mainToolBar.setFloatable(False)
        self.mainToolBar.setMovable(False)
        self.mainToolBar.addAction(self.prefAct)
        self.mainToolBar.addWidget(self.space_widget())
        self.mainToolBar.addAction(self.saveCsvAct)
        if self.use_sqlite:
            self.mainToolBar.addAction(self.saveSqliteAct)
        # self.mainToolBar.addWidget(space)
        self.mainToolBar.addAction(self.savePdfAct)
        self.mainToolBar.addWidget(self.space_widget())
        self.mainToolBar.addAction(self.exitAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def leck(self, event):
        pass

    def dialog_prefs(self, event):
        prefsdialog = PrefsDialog(self.config)
        prefsdialog.exec_()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
