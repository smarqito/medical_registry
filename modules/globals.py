import os
import sys
import getopt
from re import *

output = 'www'
input = ''

args_filter = 'o:dgirflm'

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
    print("in c_type",arg)

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

def handle_args():
    optlist, args = getopt.getopt(sys.argv[1:], args_filter)
    if args:
        sys.stdin = open(args[0], 'r')
    if optlist:
        
        for opt, val in optlist:
            if val:
                opts_handler[opt](val)
            else:
                opts_handler[opt](search(r'(?<=-)\w', opt)[0])
            