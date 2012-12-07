#!/usr/bin/env python
# -*- coding: utf-8 -*-


# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import datetime
from settings import *

class PrefsDialog(QtGui.QDialog):
    def __init__(self, config, parent=None):
        super(PrefsDialog, self).__init__(parent)

        self.config = config

        self.conf_widgs = {}

        self.tabWidget = QtGui.QTabWidget()
        self.add_gtab()
        self.add_dtab()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.close)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Einstellungen")


    def add_gtab(self):

        mainLayout = QtGui.QFormLayout()

        for name,label in ((CONFIG_SIGNER_NAME, '"Unterzeichner"'),
                           (CONFIG_ZIP_NAME, 'Postleitzahl')):
            self.conf_widgs[name] = QtGui.QLineEdit(self.config.value(name))
            mainLayout.addRow(label, self.conf_widgs[name])

        tab_widg = QtGui.QWidget()
        tab_widg.setLayout(mainLayout)
        self.tabWidget.addTab(tab_widg, "Allgemein")

    def add_dtab(self):

        radioLayout = QtGui.QHBoxLayout()

        self.sqliteRadioButton = QtGui.QRadioButton('SQLite')
        radioLayout.addWidget(self.sqliteRadioButton)
        self.sqliteRadioButton.toggled.connect(self.db_change)
        remoteRadioButton = QtGui.QRadioButton('Server')
        radioLayout.addWidget(remoteRadioButton)

        remoteLayout = QtGui.QFormLayout()

        for name,label in ((CONFIG_REMOTE_DB_SCHEME, '"Schema"'),
                           (CONFIG_REMOTE_DB_HOST, 'Host'),
                           (CONFIG_REMOTE_DB_PORT, 'Port'),
                           (CONFIG_REMOTE_DB_USER, 'Benutzer'),
                           (CONFIG_REMOTE_DB_PASSWORD, u'Paßwort'),
                           (CONFIG_REMOTE_DB_NAME, 'Datenbank')):
            self.conf_widgs[name] = QtGui.QLineEdit(self.config.value(name))
            remoteLayout.addRow(label, self.conf_widgs[name])

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(radioLayout)
        self.remoteGroup = QtGui.QGroupBox('Server')
        self.remoteGroup.setLayout(remoteLayout)
        mainLayout.addWidget(self.remoteGroup)

        tab_widg = QtGui.QWidget()
        tab_widg.setLayout(mainLayout)
        self.tabWidget.addTab(tab_widg, "Datenbank")

        {QtCore.QString(u'true'): self.sqliteRadioButton,      # QSettings-class is a little undecided about boolean type.
         True: self.sqliteRadioButton, 
         None: self.sqliteRadioButton, 
         False: remoteRadioButton, 
         QtCore.QString(u'false'): remoteRadioButton}\
            [self.config.value(CONFIG_USE_SQLITE_DB)].setChecked(True)
        self.db_change()

    def db_change(self):
        self.remoteGroup.setDisabled(self.sqliteRadioButton.isChecked())

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def writeSettings(self):
        for name,line_ed in self.conf_widgs.items():
            self.config.setValue(name,line_ed.text())
        self.config.setValue(CONFIG_USE_SQLITE_DB,self.sqliteRadioButton.isChecked())

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)

    prefsdialog = PrefsDialog(config)
    sys.exit(prefsdialog.exec_())
