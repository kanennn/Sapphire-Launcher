import os
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
                    if file.endswith(os.sep):
                        os.makedirs(os.path.join(workingDir, 'jre', *re.search('zulu17.30.15-ca-jre17.0.1-macosx_aarch64/zulu-17.jre/(.*)', file).group(1).split(os.pathsep)), exist_ok=True)
                    else:
                        zip.extract(file, path=os.path.join(workingDir, 'jre', *re.search('zulu17.30.15-ca-jre17.0.1-macosx_aarch64/zulu-17.jre/(.*)', file).group(1).split(os.pathsep)))
    print('\tDone!\n')
    

    

def downloadstatics(workingDir):
    download = downloads()

    downloadjre(download['jre'], workingDir)

    if not os.path.exists(os.path.join(workingDir, 'data', 'staticsinstalled.dat')):
        with open(os.path.join(workingDir, 'data', 'staticsinstalled.dat'),'wb') as staticsinst:
            pickle.dump(True, staticsinst)
