import os
import subprocess
from authuser import *
import pickle

def launch(version):
    # Main launch handler
    authtoken, username, uuid = authenticateuser()

    input = assembleinput(version, authtoken, username, uuid)
    print (input)

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

    return authrequest.authtoken, authrequest.username, authrequest.uuid

def assembleinput(version, authtoken, username, uuid):

    if os.path.exists('{}_vanilla_install/installdata_{}.dat'.format(version,version)):
        with open('{}_vanilla_install/installdata_{}.dat'.format(version,version), 'rb') as installdata:
            installlaunchdata = pickle.load(installdata)

    launchinputlist = [
        'mainClass {}'.format(installlaunchdata["mainclass"]),
        'param --username',
        'param {}'.format(username),
        'param --version',
        'param MultiMC5',
        'param --gameDir',
        'param {}'.format(os.getcwd() + '/minecraft'),
        'param --assetDir',
        'param {}'.format(os.getcwd() + '/{}_vanilla_install/assets'.format(version)),
        'param --assetsDir',
        'param {}'.format(os.getcwd() + '/assets'),
        'param --assetIndex',
        'param {}'.format(installlaunchdata["assetindex"]),
        'param --uuid',
        'param {}'.format(uuid),
        'param --accessToken',
        'param {}'.format(authtoken),
        'param --userType',
        'param mojang', # Will change to be dynamic in the future
        'param --versiontype',
        'param {}'.format(installlaunchdata["versiontype"]),
        'windowTitle MultiMC: Working',
        'windowParams 854x480',
        'traits XR:Initial',
        'traits FirstThreadOnMacOS',
        'launcher onesix'
    ]

    for lib in [i for i in installlaunchdata["libraries"] if 'java-objc-bridge' not in i]:
        launchinputlist.append('cp {}/{}_vanilla_install/libraries/{}'.format(os.getcwd(),version,lib))
    
    launchinputlist.append('ext {}/{}_vanilla_install/libraries/{}'.format(os.getcwd(),version,[i for i in installlaunchdata["libraries"] if 'java-objc-bridge' in i][0]))

    return launchinputlist
if __name__ == "__main__":
    launch('1.17.1')