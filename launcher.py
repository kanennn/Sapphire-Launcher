import sys
import json
from urllib.request import urlopen
import requests
import installversion
import launch
import pickle
import os

def ifwhatversions():
    if os.path.exists('installedversions.dat'):
        with open('installedversions.dat','rb') as iV:
            instversions = pickle.load(iV)
            return instversions
    else: return 'None'

if __name__ == "__main__":
    launcherversion = '0.1.0'

    commands = ['quit','launch','install']

    print('\n# MBasiC Launcher v{} - Use \"?\" for help.\n'.format(launcherversion))

    while True:
        prompt= input('[] ')

        if '' == prompt.strip():
            print('! Empty command')
            continue

        elif prompt.rsplit()[0] not in commands:
            print('! Not a command')
        
        elif commands[0] == prompt.strip():
            print('* Closing...')
            break

        elif commands[1] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()): 
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions()
                if checkversions == 'None':
                    if input('* No versions appear to be installed, would you like to install this one? (y/n): ') == 'y':
                        installversion.install(version)
                    else:
                        print('* Returning...')
                elif version not in checkversions:
                        if input('* Version %s is not installed, would you like to install it? (y/n): ' % version) == 'y':
                            installversion.install(version)
                else:
                    launch.launch(version)

            else:
                print('! No version provided')
            
            continue
        
        elif commands[2] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()):
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions()
                if checkversions == 'None' or version not in checkversions:
                    installversion.install(version)
                else:
                    launch.launch(version)
                

    
    


        


