#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore
import sqlalchemy as sqAl

import datetime
from pprint import pprint

from structure import structure as STRUCTURE 
from settings import *

class Report():

    def __init__(self, year=None):
        self.year = year
        self.config = QtCore.QSettings(CONFIG_VENDOR_NAME, CONFIG_MAIN_NAME)
        engine = sqAl.create_engine('sqlite:///%s' % self.config.value(CONFIG_DB_PATH_NAME))
        metadata = sqAl.MetaData()
        metadata.bind = engine
        self.participants = sqAl.Table(TABLE_NAME, metadata, autoload=True)
        # self.participants = sqAl.Table(self.config.value(QtCore.QString(CONFIG_DB_TABLE_NAME)), metadata, autoload=True)
        self.db_connection = engine.connect()
        self.result = {}
        self.process_data()

    def _add_common_wheres(self, select):
        if self.year != None:
            select = select.where(self.participants.c.jahr == self.year)
        select = select.where(self.participants.c.mtpv != -1)
        return select

    def process_data(self):

        multi_int_fields = []
        average_fields = []
        multi_bool_fields = []
        choice_fields = []
        for field in STRUCTURE.db_items:
            print(field['fieldname'])
            if field['typ'] == 'multi_int':
                for n, name in enumerate(field['allowance']):
                    fieldname = DB_FMT_MI % (field['fieldname'], n)
                    multi_int_fields.append(fieldname)
                    self.result[fieldname] = [0] * 4
            elif field['typ'] == 'multi_bool':
                for n, name in enumerate(field['allowance']):
                    fieldname = DB_FMT_MB % (field['fieldname'], n)
                    multi_bool_fields.append(fieldname)
                    self.result[fieldname] = [0] * 4
            elif field['typ'] == 'int':
                self.result[field['fieldname']] = [0] * 4
                average_fields.append(field['fieldname'])
            elif field['typ'] == 'enum':
                pass # nicht der Weisheit letzter Schluss
            elif field['typ'] == 'dropdown': 
                self.result[field['fieldname']] = []
                for n in range(4):
                    self.result[field['fieldname']].append([0 for x in field['allowance']])
                choice_fields.append(field['fieldname'])
            elif type(field['allowance']) == datetime.date: 
                self.result[field['fieldname']] = [None] * 4

        for n in [CONFIG_SIGNER_NAME, CONFIG_ZIP_NAME]:
            self.result[n] = [self.config.value(n)] * 4

        mtpv = self.participants.c.mtpv

        self.result['count_participants'] = [0] * 4 
        
        cols = [sqAl.func.count('*').label('count'), mtpv]
        select = sqAl.sql.select(cols, group_by=[mtpv])
        select = self._add_common_wheres(select)
        result = self.db_connection.execute(select)
        for row in result:
            self.result['count_participants'][row['mtpv']] = row['count']
 
        # print self.result
        # # for k in self.result.keys():
        # #     print k
        # print len(self.result.keys())

        # processing sum fields
        cols = [sqAl.func.sum(getattr(self.participants.c, f)).label(f) for f in multi_int_fields]
        cols.append(mtpv)
        select = sqAl.sql.select(cols, group_by=[mtpv])
        select = self._add_common_wheres(select)
        result = self.db_connection.execute(select)
        # print select
        for row in result:
            # print 'mtpv: %d' % row['mtpv'],
            for f in multi_int_fields:
                self.result[f][row['mtpv']] = row[f]
            #     print '%s: %.1f,' % ( f, row[f] ),
            # print ''

        # processing average fields
        for field in average_fields:
            col = getattr(self.participants.c, field)
            cols = [sqAl.func.avg(col).label(field), mtpv]
            # select = sqAl.sql.select(cols, getattr(self.participants.c, field)!=0, group_by=[mtpv])
            select = sqAl.sql.select(cols, group_by=[mtpv]).where(col != -1)
            select = self._add_common_wheres(select)
            result = self.db_connection.execute(select)
            for row in result:
                # print 'mtpv: %d' % row['mtpv'],
                for f in average_fields:
                    self.result[field][row['mtpv']] = row[field]
                    #     print '%s: %.1f,' % ( f, row[f] ),
                  # print ''
        # cols = [sqAl.func.avg(getattr(self.participants.c, f)).label(f) for f in average_fields]
        # cols.append(mtpv)
        # select = sqAl.sql.select(cols, group_by=[mtpv])
        # result = self.db_connection.execute(select)
        # for row in result:
        #     for f in average_fields:
        #         self.result[f][row['mtpv']] = row[f]


        # processing choice fields
        for f in choice_fields:
            col = getattr(self.participants.c, f)
            cols = [sqAl.func.count('*').label('count'), col, mtpv]
            select = sqAl.sql.select(cols, group_by=[col, mtpv]).where(col != -1)
            select = self._add_common_wheres(select)
            result = self.db_connection.execute(select)
            for row in result:
                # print '%d %d %d' % ( row['mtpv'], row[f], row['count'] )
                self.result[f][row['mtpv']][row[f]] = row['count']
            # print '%d %d' % ( row[att], row['mtpv'] )
        # for i in range(4):
        #     print self.result['f5'][i]
        #     print self.result['f6'][i]

        # processing multiple select fields
        # cols = [sqAl.func.count(getattr(self.participants.c, f)).label(f) for f in multi_bool_fields]
        # cols.append(mtpv)
        # select = sqAl.sql.select(cols, group_by=[mtpv])
        # result = self.db_connection.execute(select)
        # for row in result:
        #     for f in multi_bool_fields:
        #         self.result[f][row['mtpv']] = row[f]
        for f in multi_bool_fields:
            cols = [sqAl.func.count('*').label('count'), mtpv]
            select = sqAl.sql.select(cols, group_by=[mtpv]).where(getattr(self.participants.c, f) == True)
            select = self._add_common_wheres(select)
            result = self.db_connection.execute(select)
            for row in result:
                # for n in multi_bool_fields:
                self.result[f][row['mtpv']] = row['count']
        # for i in range(4):
        #     print self.result['f29'][i]
        #     print self.result['f40'][i]


if __name__ == '__main__':
    r = Report('2013')
    pprint(r.result)
