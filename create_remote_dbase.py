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

<<<<<<< HEAD
engine = create_engine('%s://%s:%s@%s:%s/%s' % (config.value(CONFIG_REMOTE_DB_SCHEME),
                                                config.value(CONFIG_REMOTE_DB_USER),
                                                config.value(CONFIG_REMOTE_DB_PASSWORD),
                                                config.value(CONFIG_REMOTE_DB_HOST),
                                                config.value(CONFIG_REMOTE_DB_PORT),
                                                config.value(CONFIG_REMOTE_DB_NAME)), pool_timeout=10, echo=True)
=======
>>>>>>> b0eaed6e4d64d54890fad9ac51fef6d45fcad3d2

Participant.__base__.metadata.create_all(engine, checkfirst=True)

