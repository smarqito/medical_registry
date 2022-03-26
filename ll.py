#!/usr/bin/env python3 
#----------------------------------------------------------------
# Created by: Marco António Sousa
# Created date: 2022-03-26
# Version = '1.0'
#----------------------------------------------------------------
''' ll.py:  '''
#----------------------------------------------------------------
from re import *
import sys
import templates

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'
def reader():
    f = open('assets/emd.csv', 'r')
    lathl = []
    atmp = open('template/athlete/athlete.html', 'r')
    atmpl = atmp.read()
    for l in f.readlines():
        m = match(reg, l)
        if m:
            gd = m.groupdict()
            lathl.append({'id': gd['id'], 'primeiro': gd['primeiro'], 'ultimo': gd['ultimo']})

            t = templates.template(gd, atmpl)
            
            nathl = open(f'www/athlete/{gd["id"]}.html', 'w')
            nathl.write(t)
            nathl.close()

    temps = templates.load_templates('template/athlete/', {'athl_item':'athl_item.html', 'main':'index.html'})

    index = templates.template({'athletes': lathl}, temps)
    open('www/athlete/index.html', 'w').write(index)

reader()