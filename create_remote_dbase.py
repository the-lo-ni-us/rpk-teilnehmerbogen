#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, sys, md5
from sqlalchemy import *
from settings import *
from structure import structure as STRUCTURE 

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore

config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)

metadata = MetaData()

server_url = '%s://%s:%s@%s:%s/%s' % (config.value(CONFIG_REMOTE_DB_SCHEME),
                                      config.value(CONFIG_REMOTE_DB_USER),
                                      config.value(CONFIG_REMOTE_DB_PASSWORD),
                                      config.value(CONFIG_REMOTE_DB_HOST),
                                      config.value(CONFIG_REMOTE_DB_PORT),
                                      config.value(CONFIG_REMOTE_DB_NAME))
print server_url

engine = create_engine(server_url, pool_timeout=10)
metadata.bind = engine

mytable = Table(TABLE_NAME, metadata,
                Column('id', Integer, primary_key=True)
           )

for field in STRUCTURE.cap_items:
    if field['typ'] in ('str','enum'):
        mytable.append_column(Column(field['fieldname'], String, default=''))
    elif field['typ'] == 'multi_bool':
        for i, item in enumerate(field['allowance']):
            mytable.append_column(Column(DB_FMT_MB % (field['fieldname'], i), Boolean))
    elif field['typ'] == 'multi_int':
        for i, item in enumerate(field['allowance']):
            mytable.append_column(Column(DB_FMT_MI % (field['fieldname'], i), Integer))
    elif field['typ'] in ('int','dropdown'): 
        mytable.append_column(Column(field['fieldname'], Integer))
    # elif type(field['allowance']) == datetime.date: 
    #     mytable.append_column(Column(field['fieldname'], Date))

# mytable.drop(checkfirst=True)
mytable.create(checkfirst=True)

# config = ConfigParser.ConfigParser()
# config.read('versions.ini')

# id_list = ['%s\%s'%(c.name,c.type) for c in mytable.c]
# config.set('versions', 'db_structure_fingerprint', md5.new('/'.join(sorted(id_list))).hexdigest())
# config.write(open('versions.ini','w'))
