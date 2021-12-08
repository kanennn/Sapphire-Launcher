import sys
import json
from urllib.request import urlopen
import requests
import installversion
import pickle
import os

launcherversion = '0.1.0'

commands = ['quit','launch','install']

def launch(version):
    pass

print('\n# MBasiC Launcher v{} - Use \"?\" for help.\n'.format(launcherversion))

while True:
    prompt= input('[] ')

    if '' == prompt.strip():
        print('! Empty command')
        continue
    
    if commands[0] == prompt.strip():
        print('* Closing...')
        break

    if commands[1] == prompt.rsplit()[0]:
        if 1 < len(prompt.rsplit()): 
            version = prompt.rsplit()[1]
            if os.path.exists('installedversions.dat'):
                with open('installedversions.dat', 'rb') as iV:
                    instversions = pickle.load(iV)
                if version not in instversions:
                    if input('* Version  %s is not installed, would you like to install it? (y/n): ') == 'y':
                        installversion.install(version)
                    else:
                        print('* Returning...')
                        continue
                else:
                    launch(version)
            else:
                if input('* No versions appear to be installed, would you like to install this one? (y/n): ') == 'y':
                    installversion.install(version)
                else:
                    print('* Returning...')
        else:
            print('! No version provided')
        
        continue
    
    if prompt.split() not in commands:
        print('! Not a command')


