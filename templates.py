#!/usr/bin/env python3
# ----------------------------------------------------------------
# Created by: Marco António Sousa
# Created date: 2022-03-26
# Version = '1.0'
# ----------------------------------------------------------------
''' templates.py: Popular uma template com informacao\n
How to:\n
\ttemplate with simple vars: template(info_dict, template)\n
\tTemplate with complex vars - lists(info_dict, templates_dict)\n
\t\ttemplates_dict must have a "main" key which is the main template'''
# ----------------------------------------------------------------
from re import *
import sys
from multipledispatch import dispatch
#import os

def load_templates(rootPath : str, temps: dict) -> dict:
    '''load templates to a dictionary, using root dir'''
    for t_key, t_name in temps.items():
        t = open(f'{rootPath}{t_name}', 'r')
        temps[t_key] = t.read()
        t.close
    return temps

@dispatch(dict, str)
def template(obj: dict, temp: str) -> str:
    '''Utilizar em templates sem listas:\n
    \t obj[key] must match with template {{key}}
    \tWill replace {{key}} w/ obj[key] value
    '''
    for k in obj:
        temp = sub(rf'{{{{{k}}}}}', obj[k], temp)
    return temp

@dispatch(dict, dict)
def template(obj : dict, temps: dict) -> str:
    '''Utilizar em templates com listas\n
        temps -> {'template_name': 'template'}\n
        Estrategia:\n
        \tIf obj[key] is a list, then populate over the template in temps\n
        \t\ttemp should have {{temp_name, key}} to be overriden
        \tIf is not a list, behaves the same way as simple template
    '''
    res = temps['main']
    print(temps['athl_item'])
    for k in obj:
        if type(obj[k]) is list:
            total = ''
            m = search(rf'{{{{(\w+), {k}}}}}', res) # search the key and get template name
            if m:
                for i in obj[k]:
                    tmp = temps[m[1]]
                    for ik in i:
                        tmp = sub(rf'{{{{{ik}}}}}', i[ik], tmp)
                    total += tmp
                res = sub(rf'{{{{(\w+), {k}}}}}', total, res)
        else:
            res = sub(rf'{{{{{k}}}}}', obj[k], res)
    return res

