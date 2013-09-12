#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, sys, md5
from sqlalchemy import *
from settings import *
from participant import Participant

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore

config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)

server_url = '%s://%s:%s@%s:%s/%s' % (config.value(CONFIG_REMOTE_DB_SCHEME),
                                      config.value(CONFIG_REMOTE_DB_USER),
                                      config.value(CONFIG_REMOTE_DB_PASSWORD),
                                      config.value(CONFIG_REMOTE_DB_HOST),
                                      config.value(CONFIG_REMOTE_DB_PORT),
                                      config.value(CONFIG_REMOTE_DB_NAME))
print(server_url)

engine = create_engine(server_url, pool_timeout=10, echo=True)

Participant.__base__.metadata.create_all(engine, checkfirst=True)

