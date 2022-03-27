import os

output = 'www'

def create_folder_output(name):
    global output
    if not os.path.isdir(f'{output}/{name}'):
        os.mkdir(f'{output}/{name}')

def create_folder(name):
    if not os.path.isdir(f'{name}'):
        os.mkdir(f'{name}')