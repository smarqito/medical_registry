#!/usr/bin/env python3
from re import *
import sys

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

f = open("assets/emd.csv")

def reader():
    inde = open("index.html", "w")
    inde.write('<ul>')
    for l in f.readlines():
        templ = open("template/athlete.html")
        templat = templ.read()
        m = match(reg, l)
        if m:
            gd = m.groupdict()
            inde.write(f'<li><a href="athlete/{gd["id"]}.html">{gd["primeiro"]}, {gd["ultimo"]}</a></li>')
            for k in gd.keys():
                templat = sub(rf'{{{{{k}}}}}', gd[k], templat)
            nathl = open(f'athlete/{gd["id"]}.html', 'w')
            nathl.write(templat)
        templ.close()
    inde.write('</ul>')
    inde.close()

reader()
