import os
import sys
import getopt
from re import *

output = 'www'
input = ''

args_filter = 'o:dgirflm'

opts = {}

def create_folder_output(name):
    global output
    if not os.path.isdir(f'{output}/{name}'):
        os.mkdir(f'{output}/{name}')

def create_folder(name):
    if not os.path.isdir(f'{name}'):
        os.mkdir(f'{name}')

def c_output(arg):
    global output
    output = arg

def c_type(arg):
    opts[arg] = True

def get_opts():
    global opts
    return opts

def get_output():
    return output

opts_handler = {
    '-o': c_output,
    '-d': c_type,
    '-g': c_type,
    '-i': c_type,
    '-r': c_type,
    '-f': c_type,
    '-l': c_type,
    '-m': c_type
}

def mode(bool: bool):
    for arg in findall(r'\w(?!:)', args_filter):
        opts[arg] = bool

def show_help():
    f = open('manual.txt', 'r')
    print(f.read())
    f.close()

def handle_args():
    mode(True)
    '''inicia as opts todas a true'''
    optlist, args = getopt.getopt(sys.argv[1:], args_filter, ['help'])
    if ('--help', '') in optlist:
        show_help()
        sys.exit()
    if args:
        sys.stdin = open(args[0], 'r')
    if optlist:
        '''passa tudo para false e assume a linha de comandos'''
        for opt,val in optlist:
            if opt != '-o': 
                mode(False)
        for opt, val in optlist:
            if val:
                opts_handler[opt](val)
            else:
                opts_handler[opt](search(r'(?<=-)\w', opt)[0])
            