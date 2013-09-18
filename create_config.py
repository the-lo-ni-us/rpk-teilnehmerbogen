#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore
import os
from settings import *

config =  QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)

if os.name == 'nt':
    config.setValue(CONFIG_DB_PATH_NAME, '%s\\%s\\data.sqlite' % (os.environ['APPDATA'], CONFIG_MAIN_NAME))
    config.setValue(CONFIG_LAST_SAVE_DIR, os.environ['USERPROFILE'])
elif os.name == 'posix':
    config.setValue(CONFIG_DB_PATH_NAME, '%s/.%s.d/data.sqlite' % (os.environ['HOME'], CONFIG_MAIN_NAME))
    config.setValue(CONFIG_LAST_SAVE_DIR, os.environ['HOME'])

data_dir = os.path.dirname(str(config.value(CONFIG_DB_PATH_NAME)))
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

config.setValue(CONFIG_USE_SQLITE_DB, 'True')
config.setValue(CONFIG_REMOTE_DB_SCHEME, 'postgresql')
config.setValue(CONFIG_REMOTE_DB_HOST, 'dbhost')
config.setValue(CONFIG_REMOTE_DB_PORT, '5432')
config.setValue(CONFIG_REMOTE_DB_USER, 'dbuser')
config.setValue(CONFIG_REMOTE_DB_PASSWORD, 'dbpass')
config.setValue(CONFIG_REMOTE_DB_NAME, 'teilnehmerbogen')

config.setValue(CONFIG_DB_TABLE_NAME, 'participants')
