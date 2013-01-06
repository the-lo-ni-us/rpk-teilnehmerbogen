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

import sqlalchemy as sqAl
from sqlalchemy.orm import sessionmaker as sqAl_sessionmaker

import resources_rc

from widgets import *
from dialog_prefs import PrefsDialog
from structure import structure as STRUCTURE
from participant import Participant
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
        self.use_sqlite = self.config.value(CONFIG_USE_SQLITE_DB, True, type=bool)

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
        self.initialize_db()
        self.list_participants()
        self._reset()
        if self.config.value('geometry'):
            self.restoreGeometry(self.config.value('geometry')) #.toByteArray())
        # QtGui.QMessageBox.information(self,
        #         "Bitte beachten", u"""<p>Dies ist eine Vorabversion, die nicht für den produktiven Einsatz geeignet ist.</p>
        #          <p>Dieses Programm steht unter der <a href='http://www.gnu.org/licenses/gpl-3.0'>GPLv3</a> und die Quellen 
        #          sind auf <a href='https://github.com/the-lo-ni-us/bagrpk-summenbogen'>github.com</a> jedermann zugänglich.</p>
        #          <p>&copy; 2012 Thelonius Kort</p>""")

    def initialize_db(self):
        if self.use_sqlite:
            engine = sqAl.create_engine('sqlite:///%s' % self.config.value(CONFIG_DB_PATH_NAME))
        else:
            engine = sqAl.create_engine('%s://%s:%s@%s:%s/%s' % (self.config.value(CONFIG_REMOTE_DB_SCHEME),
                                                                 self.config.value(CONFIG_REMOTE_DB_USER),
                                                                 self.config.value(CONFIG_REMOTE_DB_PASSWORD),
                                                                 self.config.value(CONFIG_REMOTE_DB_HOST),
                                                                 self.config.value(CONFIG_REMOTE_DB_PORT),
                                                                 self.config.value(CONFIG_REMOTE_DB_NAME)), pool_timeout=10)
        self.session = sqAl_sessionmaker(bind=engine)()
        # print self.session.connection().info

    def wire(self):
        for w in self.widg_dict.values():
            w.connect_dirty(self.set_dirty)
        self.newButton.clicked.connect(self._reset)
        self.saveButton.clicked.connect(self.save_participant)
        self.deleteButton.clicked.connect(self.delete_participant)
        QtGui.QShortcut(QtGui.QKeySequence(self.tr("Ctrl+S")), self, member=self.save_participant)
        self.participants_lv.itemClicked.connect(self.load_participant)

    def list_participants(self):
        self.participants_lv.clear()
        try:
            result = self.session.query(Participant.id, Participant.name).order_by(sqAl.func.lower(Participant.name)).all()
            for p in result:
                wi = QtGui.QListWidgetItem(p.name)
                wi.setData(QtCore.Qt.UserRole, p.id)
                self.participants_lv.addItem(wi)
            self.rightInnerBox.setEnabled(True)
        except (sqAl.exc.OperationalError, sqAl.exc.ProgrammingError) as e:
            self.rightInnerBox.setEnabled(False)
            QtGui.QMessageBox.information(self,
                "Fehler", "<p>Datenbankserver nicht erreichbar</p><p><small>%s</small></p>" % e)

    def new_participant(self, event):
        if not self.ask_save('Neuen Teilnehmer anlegen'):
            return
        self._reset()

    def save_participant(self, event=None):
        if not self.Dirty:
            QtGui.QMessageBox.information(self, 
                                          u'Teilnehmerdatensatz speichern...', 
                                          u'Es wurde nichts geändert')
            return False
        self._save_participant()
        self.statusBar().showMessage("Teilnehmer gespeichert")
        self._highlight_participant()

    def _save_participant(self):
        if not self.participant:
            self.participant = Participant()
        message = ""
        for name, widg in self.widg_dict.items():
            setattr(self.participant, name, widg.get_value())
        if not self.participant.id:
            self.session.add(self.participant)
        self.session.commit()
        self.Dirty = False
        self.list_participants()

    def _highlight_participant(self):
        if self.participant:
            for i in range(self.participants_lv.count()):
                if self.participants_lv.item(i).data(QtCore.Qt.UserRole) == self.participant.id:
                    self.participants_lv.setCurrentRow(i)

    def load_participant(self, item):
        newly_current_participant_id = item.data(QtCore.Qt.UserRole)
        if not(newly_current_participant_id): # How can this ever happen?
            return False
        elif not(self.askSave()):
            if self.participant:
                self._highlight_participant()
            return False
        self.participant = self.session.query(Participant).filter(Participant.id == newly_current_participant_id).first()
        for f, widg in self.widg_dict.items():
            widg.set_value(getattr(self.participant, f))
        self._highlight_participant()
        self.Dirty = False
        self.statusBar().showMessage('')

    def delete_participant(self, event):
        if self.participant:
            reply = QtGui.QMessageBox.critical(self, u'Teilnehmerdatensatz löschen',
                                     u'Wirklich "%s" löschen?' % self.participant.name,
                                     QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Yes)
            if reply == QtGui.QMessageBox.Yes:
                self.session.delete(self.participant)
                self.session.commit()
                self._reset()
                self.list_participants()
        else:
            QtGui.QMessageBox.information(self, 
                                          u'Teilnehmerdatensatz löschen', 
                                          u'Kein Teilnehmer ausgewählt')

###########################################################################

    def set_dirty(self, e=None):
        self.Dirty = True
        self.statusBar().showMessage("")
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
        self.rightInnerBox.setEnabled(False)
        # scrolled.adjustSize()

    def createMainPanel(self):
        self.participants_lv = QtGui.QListWidget(self)
        self.participants_lv.setMinimumHeight(500)
        self.participants_lv.setMaximumWidth(300)

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
        record_descr = (u"'%s'" % self.participant.name) if self.participant else u'der neue Datensatz'
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                message_title, u'Soll %s gespeichert werden?' % record_descr,
                QtGui.QMessageBox.NoButton, self)
        # sb = msgBox.addButton("&Speichern", QtGui.QMessageBox.AcceptRole)
        # dsb = msgBox.addButton("&Nicht speichern", QtGui.QMessageBox.DestructiveRole)
        sb = msgBox.addButton("&Speichern", QtGui.QMessageBox.NoRole)
        dsb = msgBox.addButton("&Nicht speichern", QtGui.QMessageBox.NoRole)
        cb = msgBox.addButton("&Abbrechen", QtGui.QMessageBox.NoRole)
        msgBox.setEscapeButton(cb)
        msgBox.setDefaultButton(sb)
        msgBox.exec_()
        reply = msgBox.clickedButton()
        # print 'reply: %s' % reply
        if reply == cb:
            return False
        elif reply == sb:
            self._save_participant()
        return True

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
        self.prefAct = QtGui.QAction(QtGui.QIcon(':icons/preferences-32.png'), 
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
        self.statusBar() # .showMessage("Ready")

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
