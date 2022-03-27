import os

output = 'www'

def create_folder(name):
    global output
    if not os.path.isdir(f'{output}/{name}'):
        os.mkdir(f'{output}/{name}')