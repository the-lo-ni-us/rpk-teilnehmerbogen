#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, sys, md5
import sqlalchemy as sqAl
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker as sqAl_sessionmaker, composite as sqAl_composite
import ConfigParser
from composite_col import CompositeCol
from settings import *
from structure import structure as STRUCTURE 

def generate_class(name): # Don't know if we really need name

    Base = declarative_base(sqAl.MetaData())

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

    dynclass_dict = {
        'id': sqAl.Column(sqAl.Integer, primary_key=True),
        '__tablename__': 'participants'
        }
    for field in STRUCTURE.cap_items:
        if field['typ'] in ('str','enum'):
            dynclass_dict[field['fieldname']] = sqAl.Column(field['fieldname'], sqAl.String)
        elif field['typ'] in ('multi_bool', 'multi_int'):
            specs = mf_specs[field['typ']]
            sub_fields = []
            for i, item in enumerate(field['allowance']):
                fn = specs['format'] % (field['fieldname'], i)
                cf =  sqAl.Column(fn, specs['db_col_type'], default=specs['default'])
                dynclass_dict[fn] = cf
                sub_fields.append(cf)
            dynclass_dict[field['fieldname']] = sqAl_composite(CompositeCol, *sub_fields)
        elif field['typ'] in ('int', 'dropdown', 'enumber'): 
            dynclass_dict[field['fieldname']] =  sqAl.Column(field['fieldname'], sqAl.Integer, default=-1)

    return type(name, (Base,), dynclass_dict)

Participant = generate_class('Participant')


if __name__ == '__main__':
    engine = sqAl.create_engine('sqlite:///%s' % wx.Config(CONFIG_MAIN_NAME).Read(CONFIG_DB_PATH_NAME), echo=True)
    Session = sqAl_sessionmaker(bind=engine)
    session = Session()

    # t = Participant(name='DynClass V.', 
    #              f29=CompositeCol(True,True,True,False,False,False,False,False,False,False,True,True,True,True),
    #              f32=CompositeCol(14,21,28,0,0,0,0,0))
    # print session.add(t)
    p = session.query(Participant).filter(Participant.id == 2).first()
    p.mtpv = 2
    # p.name = 'Etre Petetre'
    # setattr(p,'f2', 28)
    # results = session.query(Participant).all()
    # for rec in results:
    #     [setattr(rec, f['fieldname'], 0) for f in STRUCTURE.db_items if f['typ'] == 'dropdown' and getattr(rec, f['fieldname']) == -1]
    session.commit()
    # print dir(p)
