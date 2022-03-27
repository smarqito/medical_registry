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
        t.close()
    return temps

@dispatch(dict, str)
def template(obj: dict, temp: str) -> str:
    '''Utilizar em templates sem listas:\n
    \t obj[key] must match with template {{key}}
    \tWill replace {{key}} w/ obj[key] value
    '''
    #print("template dict:", obj)
    for k in obj:
        temp = sub(rf'{{{{{k}}}}}', str(obj[k]), temp)
    return temp

@dispatch(list, str)
def template(obj: list, temp: str) -> str:
    res = ''
    for e in obj:
        if type(e) is dict:
            res += template(e, temp)
        else:
            res += sub(r'\{\{\w+\}\}', str(e), temp)
    return res

@dispatch(object, str, dict)
def template(obj, temp, temps: dict) -> str:
    '''Utilizar em templates com listas\n
        temps -> {'template_name': 'template'}\n
        Estrategia:\n
        \tIf obj[key] is a list, then populate over the template in temps\n
        \t\ttemp should have {{temp_name, key}} to be overriden
        \tIf is not a list, behaves the same way as simple template
    '''
    res = temps[temp]
    #print("template:", temp)
    iterable = findall(r'\{\{(\w+), (\w+)\}\}', res)
    
    for t, key in iterable:
        if type(obj) is dict:
            #print("antes dict")
            found = template(obj[key], t, temps) # itera todos os que tem templates
            #print("depois dict")
            res = sub(rf'{{{{{t}, {key}}}}}', found, res) # preenche a template
        elif type(obj) is list:
            found = ''
            for e in obj:
                if type(e) is dict:
                    found += template(e[key], t, temps)
                else:
                    found += template(e, t, temps)
            res = sub(rf'{{{{{t}, {key}}}}}', found, temps[temp])

    res = template(obj, res)

    return res

