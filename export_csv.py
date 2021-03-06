#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sqlalchemy as sqAl
from sqlalchemy.orm import sessionmaker as sqAl_sessionmaker
from settings import *
from participant import Participant

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

outcsv = csv.writer(open('mydump.csv', 'wb'))

# print dir(Participant)


outcsv.writerow(result.keys())
outcsv.writerows(result)

# print result
if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4).pprint
    pp(result)
