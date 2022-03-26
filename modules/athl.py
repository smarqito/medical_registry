#!/usr/bin/env python3
#----------------------------------------------------------------
# Created by: José Malheiro, Marco Sousa e Miguel Fernandes
# Created date: 2022-03-22
# Version = '1.0'
#----------------------------------------------------------------
""" Gera um indice de atletas por ordem lexicografica do nome """
#----------------------------------------------------------------
from re import *
import sys
from os import mkdir, path

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

f = open("assets/emd.csv")
if not path.isdir('www/athlete'):
    mkdir('www/athlete')

def get_key(match):
    gd = match.groupdict()
    return gd["primeiro"] + " " + gd["ultimo"]

def reader():
    todos = []
    inde = open("www/athlete/index.html", "w")
    inde.write('<ul>')
    for l in f.readlines():
        m = match(reg, l)
        if m:
            todos.append(m)
    ## alinha
    todos.sort(key=get_key)
    
    templ = open("template/athlete.html")
    templat = templ.read()
    
    for m in todos:
        atleta = templat
        gd = m.groupdict()
        
        inde.write(f'<li><a href="athlete/{gd["id"]}.html">{gd["primeiro"]}, {gd["ultimo"]}</a></li>')
        for k in gd.keys():
            atleta = sub(rf'{{{{{k}}}}}', gd[k], atleta)

        nathl = open(f'www/athlete/{gd["id"]}.html', 'w')
        nathl.write(atleta)
    templ.close()
    inde.write('</ul>')
    inde.close()

reader()
