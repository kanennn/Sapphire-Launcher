import os
from re import sub
import subprocess
from sys import stdout
from authuser import *
import pickle

def launch(version):
    # Main launch handler
    authdata = authenticateuser()

    if authdata.status == 'OK':
        authtoken, username, uuid = authdata.authtoken, authdata.username, authdata.uuid
    elif authdata.status == 'Failed':
         print('! %s'% authdata.error)
         return 'Failed'

    launch = constructcommand(version, authtoken, username, uuid)

    launchcommand = subprocess.Popen(launch, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = launchcommand.communicate()
    if launchcommand.returncode != 0:
        print('Launch failed with exit code %s' % launchcommand.returncode)
        print(stderr)
        print(stdout)

def authenticateuser():

    def manualcredentials():
        email = input('Email (or legacy username):\t')
        password = input('Password:\t')
        return [email,password]

    if os.path.exists('auth.txt'):
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

def constructcommand(version, authtoken, username, uuid):

    with open('{}_vanilla_install/installdata_{}.dat'.format(version,version), 'rb') as installdata:
        installlaunchdata = pickle.load(installdata)

    launchinputlist = [
        installlaunchdata["mainclass"],
        '--username',
        username,
        '--version',
        version,
        '--gameDir',
        os.getcwd() + '/minecraft',
        '--assetsDir',
        os.getcwd() + '/{}_vanilla_install/assets'.format(version),
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

    command = ['zulu-17.jdk/Contents/Home/bin/java','-Dlog4j2.formatMsgNoLookups=true','-XstartOnFirstThread','-Xms409m','-Xmx2048m','-Duser.language=en','-cp']

    libpathlist = list()
    for lib in installlaunchdata["libraries"]:
        libpathlist.append(os.getcwd() + '/{}_vanilla_install/libraries/{}'.format(version,lib))
    for l in [os.getcwd() + '/lwjgl/' + i for i in os.listdir(os.getcwd() + '/lwjgl/') if i.endswith('.jar')]:
        libpathlist.append(l)
    libpathlist.append(os.getcwd() + '/apache-log4j-2.16.0-select/log4j-api-2.16.0.jar')
    libpathlist.append(os.getcwd() + '/apache-log4j-2.16.0-select/log4j-core-2.16.0.jar')

    command.append(":".join(libpathlist))

    return command + launchinputlist

if __name__ == "__main__":
    launch(input('Version : '))