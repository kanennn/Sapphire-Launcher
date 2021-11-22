import sys
import json
from urllib.request import urlopen
import requests
import downloadeverything

def installversion(version):
    libnames = downloadeverything.install(version)
    return libnames
    

for line in sys.stdin:
    if 'quit' == line.rstrip:
        print('closing')
        break
    if 'launch' == line.rsplit()[0]:
        
        try:
            version = line.rsplit()[1]
        except:
            print('! No version provided')
        with open('installed-versions') as iV:
            instVersion = json.load(iV)
        if version not in instVersion['versions']:
            if input('Version  %s is not installed, would you like to install it?') == 'Yes' or 'yes':
                installversion(version)
        else:
            launch(version)

def launch(version):
    pass


