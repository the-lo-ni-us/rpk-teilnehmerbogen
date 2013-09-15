#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, wx
import sqlalchemy as sqAl
from settings import *

metadata = sqAl.MetaData()
engine = sqAl.create_engine('sqlite:///%s' % wx.Config(CONFIG_MAIN_NAME).Read(CONFIG_DB_PATH_NAME))
metadata.bind = engine
participants = sqAl.Table(TABLE_NAME, metadata, autoload=True)
db_connection = engine.connect()

outcsv = csv.writer(open('mydump.csv', 'wb'))

select = sqAl.sql.select([participants])
result = db_connection.execute(select)

outcsv.writerow(result.keys())
outcsv.writerows(result)

# print result
