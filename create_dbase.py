#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, sys, md5
from sqlalchemy import *
import ConfigParser
from settings import *
from structure import structure as STRUCTURE 

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

metadata = MetaData()

engine = create_engine('sqlite:///%s' % DB_NAME)
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

mytable.create()

config = ConfigParser.ConfigParser()
config.read('versions.ini')

id_list = ['%s\%s'%(c.name,c.type) for c in mytable.c]
config.set('versions', 'db_structure_fingerprint', md5.new('/'.join(sorted(id_list))).hexdigest())
config.write(open('versions.ini','w'))
