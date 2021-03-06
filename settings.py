#!/usr/bin/env python
# -*- coding: utf-8 -*-

LABEL_WIDTH = 300
WIDGET_WIDTH = 300
PANEL_WIDTH = LABEL_WIDTH + WIDGET_WIDTH
DIALOG_FIELD_WIDTH = 150
DIALOG_FIELD_HEIGHT = 25

CONFIG_VENDOR_NAME = 'Thelonius'
CONFIG_MAIN_NAME = 'Teilnehmerbogen'
CONFIG_DB_PATH_NAME = 'DatabaseFilePath'
CONFIG_DB_TABLE_NAME = 'DatabaseTable'
CONFIG_USE_SQLITE_DB = 'UseSQLiteDB'
CONFIG_REMOTE_DB_SCHEME = 'RemoteDBKind'
CONFIG_REMOTE_DB_HOST = 'RemoteDBHost'
CONFIG_REMOTE_DB_PORT = 'RemoteDBPort'
CONFIG_REMOTE_DB_USER = 'RemoteDBUser'
CONFIG_REMOTE_DB_PASSWORD = 'RemoteDBPassword'
CONFIG_REMOTE_DB_NAME = 'RemoteDBName'
CONFIG_SIGNER_NAME = 'Signer'
CONFIG_ZIP_NAME = 'ZipCode'
CONFIG_LAST_SAVE_DIR = 'LastSaveDir'
CONFIG_LAST_SAVE_NAME = 'LastSaveName'
CONFIG_LAST_TAB_YEAR = 'LastTabYear'

DB_NAME = 'data.sqlite'
TABLE_NAME = 'participants'
DB_FMT_MI = '%s_mi_%d'
DB_FMT_MB = '%s_mb_%d'
DB_FMT_MS = '%s_%s'
DB_FMT_MN = '%s_%s'
DB_MC_PECS = {   # peculiarities of multi-column fields
    'multi_bool': {
        'format': u'{0}_mb_{1}',
        'db_col_type': 'Boolean'
    },
    'multi_int': {
        'format': u'{0}_mi_{1}',
        'db_col_type': 'Integer'
    },
    'multi_select': {
        'format': u'{0}_{1}',
        'db_col_type': 'Integer'
    },
    'multi_numeric': {
        'format': u'{0}_{1}',
        'db_col_type': 'Integer'
    }
}

PDF_TITLE = u"BAG der RPKs Summenbogen - Auswertung für %s"
DOC_TITLE = u"Technische Dokumentation RPK Teilnehmerbogen (Stand %s)"
