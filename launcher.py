import sys
import json
from urllib.request import urlopen
import requests
import installversion
import pickle
import os

def launch(version):
    pass

for line in sys.stdin:
    if 'quit' == line.rstrip:
        print('closing')
        break
    if 'launch' == line.rsplit()[0]:
        try:
            version = line.rsplit()[1]
            print(version)
            if os.path.exists('installed-versions.dat'):
                with open('installed-versions.dat', 'rb') as iV:
                    instversions = pickle.load(iV)
                if version not in instversions:
                    if input('* Version  %s is not installed, would you like to install it? (y/n)') == 'y':
                        installversion.install(version)
                    else:
                        print('returning...')
                else:
                    launch(version)
            else:
                if input('* No versions appear to be installed, would you like to install one? (y/n):\t') == 'y':
                    installversion.install(version)
                else:
                    print('returning')
        except:
            print('! No version provided')


