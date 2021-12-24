import os
import pickle

from MBasiC.installversion import *
from MBasiC.launch import *
from MBasiC.downloadstaticlibs import *

def main():
    prelaunchchecks()
    launcherversion, commands = info()
    interactiveloop(commands, launcherversion)

def prelaunchchecks():
    if os.path.exists('data/installed.dat'):
        pass

def info():
    launcherversion = '0.2.0.b1' 
    commands = ['quit','launch','install','help']
    return launcherversion, commands

def ifwhatversions():
    if os.path.exists('installedversions.dat'):
        with open('installedversions.dat','rb') as iV:
            instversions = pickle.load(iV)
            return instversions
    else: return 'None'

def interactiveloop(commands,launcherversion):

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
                        install(version)
                    else:
                        print('* Returning...')
                elif version not in checkversions:
                        if input('* Version %s is not installed, would you like to install it? (y/n): ' % version) == 'y':
                            install(version)
                else:
                    launch(version)

            else:
                print('! No version provided')
            
            continue
        
        elif commands[2] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()):
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions()
                if checkversions == 'None' or version not in checkversions:
                    install(version)
                else:
                    launch(version)
                

    
    


        

