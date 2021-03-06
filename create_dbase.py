#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, sys, md5
from sqlalchemy import *
import ConfigParser
from settings import *
from participant import Participant
from structure import structure as STRUCTURE

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)


engine = create_engine('sqlite:///%s' % DB_NAME, echo=True)

Participant.__base__.metadata.create_all(engine, checkfirst=True)

config = ConfigParser.ConfigParser()
config.read('versions.ini')

id_list = ['{0}\{1}\{2}'.format(c.name,c.type,STRUCTURE[c.name] and STRUCTURE[c.name].get('typ') or 'None') 
           for c in Participant.__table__.c]
config.set('versions', 'db_structure_fingerprint', md5.new('/'.join(sorted(id_list))).hexdigest())
config.set('versions', '64bit', sys.maxsize > 2**32)
config.write(open('versions.ini','w'))

with open('defines.nsh', 'w') as f:
    f.write('!define INSTALLER_NAME teilnehmer-{0}-{1}.exe'.format(
        config.get('versions', 'app_version'), 'x64' if sys.maxsize > 2**32 else 'x86'))
