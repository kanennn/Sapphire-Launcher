import subprocess
import os
import pickle

from MBasiC.authuser import authenticate 

def launch(version, workingDir, isFrozen, resourceDir):
    # Main launch handler
    authdata = authenticateuser(workingDir)

    if authdata.status == 'OK':
        authtoken, username, uuid = authdata.authtoken, authdata.username, authdata.uuid
    elif authdata.status == 'Failed':
         print('! %s'% authdata.error)
         return 'Failed'

    launch = constructcommand(version, authtoken, username, uuid, workingDir, isFrozen, resourceDir)

    launchcommand = subprocess.Popen(launch, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = launchcommand.communicate()
    if launchcommand.returncode != 0:
        print('Launch failed with exit code %s' % launchcommand.returncode)
        print(stderr)
        print(stdout)

def authenticateuser(workingDir):

    def manualcredentials():
        email = input('Email (or legacy username):\t')
        password = input('Password:\t')
        return [email,password]

    if os.path.exists(os.path.join(workingDir,'auth.txt')):
        with open('auth.txt', 'r') as authfile:
            try:
                authargs = authfile.readlines()
                email = authargs[0].strip()
                password = authargs[1].strip()
            except:
                print('! Your auth.txt file was not formatted properly. Please enter your username and password manually to launch.')
                email, password = manualcredentials()

    authrequest = authenticate(email=email, password=password, accounttype='mojang') # The static 'mojang' account type passed will need to be changed to be dynamic when microsoft account support is added
    
    return authrequest

def constructcommand(version, authtoken, username, uuid, workingDir, isFrozen, resourceDir):

    with open(os.path.join(workingDir, 'game','{}_vanilla_install'.format(version),'installdata_{}.dat'.format(version)), 'rb') as installdata:
        installlaunchdata = pickle.load(installdata)

    launchinputlist = [
        installlaunchdata["mainclass"],
        '--username',
        username,
        '--version',
        version,
        '--gameDir',
        os.path.join(workingDir, 'game', 'minecraft'),
        '--assetsDir',
        os.path.join(workingDir, 'game','{}_vanilla_install'.format(version), 'assets'),
        '--assetIndex',
        installlaunchdata["assetindex"],
        '--uuid',
        uuid,
        '--accessToken',
        authtoken,
        'sessionId token:' + authtoken,
        '--userType',
        'mojang', # Will change to be dynamic in the future
        '--versiontype',
        installlaunchdata["versiontype"],
    ]

    command = ['static/zulu-17.jre/Contents/Home/bin/java','-XstartOnFirstThread','-Xms409m','-Xmx2048m','-Duser.language=en','-cp']

    libpathlist = list()
    for lib in installlaunchdata["libraries"]:
        libpathlist.append(os.path.join(workingDir, 'game', '{}_vanilla_install'.format(version),'libraries',lib))
    
    if not isFrozen:
        for l in [os.path.join(workingDir, 'static', 'lwjgl', i) for i in os.listdir(os.path.join(workingDir, 'static', 'lwjgl')) if i.endswith('.jar')]:
            libpathlist.append(l)
        libpathlist.append()
        libpathlist.append(os.path.join(workingDir, 'static', 'apache-log4j-2.16.0-select/log4j-core-2.16.0.jar'))
    else:
        for l in [os.path.join(resourceDir, i) for i in os.listdir(resourceDir) if i.endswith('.jar')]:
            libpathlist.append(l)

    command.append(":".join(libpathlist))

    return command + launchinputlist

if __name__ == "__main__":
    launch(input('Version : '))