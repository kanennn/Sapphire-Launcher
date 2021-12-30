import os
import sys
import stat
import pickle
import requests
import zipfile
import tempfile
import re

def downloads():
    return {
        'jre':'https://cdn.azul.com/zulu/bin/zulu17.30.15-ca-jre17.0.1-macosx_aarch64.zip',
        'lwjgl':'https://github.com/LWJGL/lwjgl3/releases/download/3.3.0/lwjgl-3.3.0.zip'

    }

def downloadjre(download, workingDir):
    print('# Downloading JRE...', end='',flush=True)
    data = requests.get(download)
    with tempfile.TemporaryFile(mode='w+b') as filetemp:
        filetemp.write(data.content)
        with zipfile.ZipFile(filetemp,mode='r',compression=zipfile.ZIP_STORED,allowZip64=True,compresslevel=None,strict_timestamps=True) as zip:

            for file in zip.namelist():
                if file.startswith('zulu17.30.15-ca-jre17.0.1-macosx_aarch64/zulu-17.jre/'):
                    trimfile = re.search('zulu17.30.15-ca-jre17.0.1-macosx_aarch64/zulu-17.jre/(.*)', file).group(1)

                    # To write directories or files according to the conditions of the if statement, 
                    # in the jre folder in the working directory (.MBasiC folder)

                    # ? I use this instead of extract() or extractall() so I can filter out the first two parent directories.
                    # ? I know I could still use extract() but I wrote this while fighting some issues with extract() 
                    # ? - (due to executable binary permission issues, which I did fix in a different section), and I just decided to keep it.

                    if file.endswith(os.sep):
                        os.makedirs(os.path.join(workingDir, 'jre',*trimfile.split(os.pathsep)), exist_ok=True)
                    else:
                        with open(os.path.join(workingDir, 'jre', *trimfile.split(os.pathsep)), 'wb') as writtenfile:
                            writtenfile.write(zip.open(file, mode='r').read())

                    # This will write a data file to be referenced later by launch.py, for the directory of the java executable
                    
                    if trimfile.endswith('java'):
                        with open(os.path.join(workingDir, 'data', 'javapath.dat'), 'wb') as javapath:
                            pickle.dump([workingDir, 'jre', *trimfile.split(os.pathsep)], javapath)

            # This will make the executables in bin/ have executable permissions so java can be called later in launch.py to launch minecraft 

            for root, dirs, files in os.walk(os.path.join(workingDir, 'jre')):
                if 'bin' in root:
                    for file in files:
                        os.chmod(os.path.join(workingDir, root, file), stat.S_IRWXU)

    # Notify the user that the JRE is done downloading!            

    print('\tDone!')
    

    

def downloadstatics(workingDir):
    download = downloads()

    downloadjre(download['jre'], workingDir)

    if not os.path.exists(os.path.join(workingDir, 'data', 'staticsinstalled.dat')):
        with open(os.path.join(workingDir, 'data', 'staticsinstalled.dat'),'wb') as staticsinst:
            pickle.dump(True, staticsinst)
