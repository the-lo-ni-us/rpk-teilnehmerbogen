#!/usr/bin/env python
# -*- coding: utf-8 -*-

import savReaderWriter
import sqlalchemy as sqAl
from sqlalchemy.orm import sessionmaker as sqAl_sessionmaker
from settings import *
from participant import Participant
from structure import structure

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore

config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)

if config.value(CONFIG_USE_SQLITE_DB, True, type=bool):
    engine = sqAl.create_engine('sqlite:///%s' % config.value(CONFIG_DB_PATH_NAME))
else:
    engine = sqAl.create_engine('%s://%s:%s@%s:%s/%s' % (config.value(CONFIG_REMOTE_DB_SCHEME),
                                                         config.value(CONFIG_REMOTE_DB_USER),
                                                         config.value(CONFIG_REMOTE_DB_PASSWORD),
                                                         config.value(CONFIG_REMOTE_DB_HOST),
                                                         config.value(CONFIG_REMOTE_DB_PORT),
                                                         config.value(CONFIG_REMOTE_DB_NAME)), pool_timeout=10)
# session = sqAl_sessionmaker(bind=engine)()

metadata = sqAl.MetaData()
metadata.bind = engine
participants = sqAl.Table(TABLE_NAME, metadata, autoload=True)
db_connection = engine.connect()

select = sqAl.sql.select([participants])
result = db_connection.execute(select)

# result = session.query(Participant).all()

mf_specs = { # specifics of the multi-column fields 
    'multi_bool': {
        'format': DB_FMT_MB,
        'db_col_type': sqAl.Boolean,
        'default': False
    },
    'multi_int': {
        'format': DB_FMT_MI,
        'db_col_type': sqAl.Integer,
        'default': 0
    }
}

var_types = {'id': 1}
formats = {}
for f in structure.db_items:
    if f['typ'] in mf_specs:
        for n in range(len(f['allowance'])):
            fn = mf_specs[f['typ']]['format'] % (f['fieldname'], n)
            var_types[fn]  = f['sav_opts']['var_type']
            if 'format' in f['sav_opts']:
                formats[fn] = f['sav_opts']['format']
    else:
        var_types[f['fieldname']] = f['sav_opts']['var_type']
        if 'format' in f['sav_opts']:
            formats[f['fieldname']] = f['sav_opts']['format']
    # if f['typ'] in ('int','dropdown'):
    #     formats[f['fieldname']] = 'F2.0'

with savReaderWriter.SavWriter('teil.sav', result.keys(), var_types, ioUtf8=True, formats=formats) as writer:
    for record in result:
        writer.writerow(list(record))


# print result
if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4).pprint
    # pp(result.first())
    # pp(result.keys())
    # pp(var_types)
    # pp(formats)
