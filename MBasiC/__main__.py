import os
import pickle

import MBasiC.installversion as inst
import MBasiC.launch as lnch
import MBasiC.prelaunchchecks as check

def main(workingDir,isFrozen,resourceDir):
    check.launchcheck(workingDir)
    launcherversion, commands = info()
    interactiveloop(commands, launcherversion, workingDir, isFrozen, resourceDir)

def info():
    launcherversion = '0.2.0.b2' 
    commands = ['quit','launch','install',['help','?']]
    return launcherversion, commands

def ifwhatversions(workingDir):
    if os.path.exists(os.path.join(workingDir, 'data', 'installedversions.dat')):
        with open(os.path.join(workingDir, 'data', 'installedversions.dat'),'rb') as iV:
            instversions = pickle.load(iV)
            return instversions
    else: return 'None'

def helpinfo(commands):
    print(
        'Commands : {}\n'.format(', '.join(commands)) + \
        'Refer to the GitHub README.md or a wiki (when we have one) at https://github.com/Pyrotex7/MBasiC for further info.\n'

    )

def interactiveloop(commands, launcherversion, workingDir, isFrozen, resourceDir):

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

        elif prompt.strip() in commands[3]:
            print(helpinfo(commands))

        elif commands[1] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()): 
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions(workingDir)
                if checkversions == 'None':
                    if input('* No versions appear to be installed, would you like to install this one? (y/n): ') == 'y':
                        inst.install(version,workingDir,resourceDir)
                    else:
                        print('* Returning...')
                elif version not in checkversions:
                        if input('* Version %s is not installed, would you like to install it? (y/n): ' % version) == 'y':
                            inst.install(version, workingDir, resourceDir)
                else:
                    lnch.launch(version, workingDir, isFrozen, resourceDir)

            else:
                print('! No version provided')
            
            continue
        
        elif commands[2] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()):
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions(workingDir)
                if checkversions == 'None' or version not in checkversions:
                    inst.install(version, workingDir, resourceDir)
                else:
                    lnch.launch(version, workingDir, isFrozen, resourceDir)
                

    

        


