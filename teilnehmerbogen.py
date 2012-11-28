#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summenbögen erfassen...
"""


# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import resources_rc

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createToolBar()
        self.createStatusBar()

    def closeEvent(self, event):
        if self.askSave():
            # self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def askSave(self):
        return True

    def createActions(self):
        self.prefAct = QtGui.QAction(QtGui.QIcon(':icons/application-pkcs7-signature.png'), 
                                     u"&Institutsangaben eingeben", self, 
                                     statusTip=u"'Name des Unterzeichners' und 'Einrichtungs-Code Nr.' eingeben")
        self.savePdfAct = QtGui.QAction(QtGui.QIcon(':icons/application-pdf.png'), 
                                        u"Auswertung als &Pdf", self, 
                                        statusTip=u"Auswertung der Daten im PDF-Format speichern")
        self.saveCsvAct = QtGui.QAction(QtGui.QIcon(':icons/application-vnd.ms-excel.png'), 
                                        u"&CSV exportieren", self, 
                                        statusTip=u"Die Daten im CSV-Format exportieren")
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
        self.mainToolBar = self.addToolBar("Main")
        self.mainToolBar.addAction(self.prefAct)
        self.mainToolBar.addAction(self.savePdfAct)
        self.mainToolBar.addAction(self.saveCsvAct)
        self.mainToolBar.addAction(self.saveSqliteAct)
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
