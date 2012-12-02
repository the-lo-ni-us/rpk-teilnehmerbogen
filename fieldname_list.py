#!/usr/bin/env python
# coding=utf-8

class FieldnameList(list):

    def __init__(self, liste=[]):
        liste = [i for i in liste if not i.get('disabled', False)]
        list.__init__(self, liste)
        # if len(liste) > 0:
        self.index = {i['fieldname']: i for i in self if 'fieldname' in i}
        self.tab_items = [i for i in self if 'tabulation' in i['appears']]
        self.cap_items = [i for i in self if 'capture' in i['appears']] 
        self.db_items = [i for i in self.cap_items if i['typ'] != 'heading']
        self.all_items = [i for i in self if 'capture' in i['appears'] and 'tabulation' in i['appears']]
        for d in self:
            if 'default' not in d:
                d['default'] = d['allowance']

    def __getitem__(self, key):
        if type(key) == int:
            return list.__getitem__(self, key)
        elif type(key) == str and key in self.index:
            return self.index[key]
        else:
            return None
            

if __name__ == '__main__':
    from structure import structure
    import pprint
    pp = pprint.PrettyPrinter(indent=4).pprint
    l = FieldnameList(structure)
    for schrott in ('tab_items','cap_items','db_items','all_items'):
        print '%s: %d' % (schrott, len(getattr(l, schrott)))
    # print l['f5']
    # print [i['fieldname'] for i in l.db_items]
    # pp(l)
