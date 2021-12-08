import os
import subprocess
from authuser import *
import pickle

subprocess.Popen('Echo','Dude')
def launch(version):
    # Main launch handler
    authtoken, username, uuid = authenticateuser()

    input = assembleinput(version)

def authenticateuser():

    def manualcredentials():
        email = input('Email (or legacy username):\t')
        password = input('Password:\t')
        return [email,password]

    if os.path.exists('auth.txt'):
        with open('auth.txt', 'r') as authfile:
            try:
                authargs = authfile.readlines
                email = authargs[0]
                password = authargs[1]
            except:
                print('! Your auth.txt file was not formatted properly. Please enter your username and password manually to launch.')
                email, password = manualcredentials()
    
    authrequest = authenticate(email=email, password=password, accounttype='mojang') # The static 'mojang' account type passed will need to be changed to be dynamic when microsoft account support is added

    return authrequest.authtoken, authrequest.username, authrequest.uuid

def assembleinput(version):

    launchinputlist = list()

    if os.path.exists('librarylist_%s.dat'% version):
        with open('librarylist_%s.dat'% version, 'rb') as librarylist:
            libraries = pickle.load(librarylist)

    mainClass = 'net.minecraft.client.main.Main' # Needs to be dynamic in the future

    launchinputlist.append(mainClass)
    launchinputlist.append(['param --version','param MultiMC5'])
    
    