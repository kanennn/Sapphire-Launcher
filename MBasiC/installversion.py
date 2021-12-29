# Due to time constraints in the making of this project, many pieces of this code do not have any comments and may not be organized well
# This will hopefully be improved in the future

import pickle
import requests
import os
import json
import multiprocessing
from urllib.request import urlopen

#
#
# Main install control function

def install(version, workingDir, resourceDir):

    result = getversionjson(version, workingDir, resourceDir)
    if result != 'failed':
        versionjson = result
    else:
        return 'failed'
    installdir = setupinstalldir(version, workingDir)
    allurls = getallurls(versionjson)
    writeassetindex(allurls[2], versionjson, workingDir, installdir)
    downloadeverything(allurls,installdir, workingDir)
    addinstalledmark(version, workingDir)
    writeinstalldata(versionjson, version, installdir, workingDir)


def addinstalledmark(version, workingDir):
    if os.path.exists(os.path.join(workingDir, 'data', 'installedversions.dat')):
        with open(os.path.join(workingDir, 'data', 'installedversions.dat'), 'r+b') as instversionsfile:
            installedversions = pickle.load(instversionsfile)
            installedversions.append(version)
            pickle.dump(installedversions, instversionsfile)
    else:
        with open(os.path.join(workingDir, 'data', 'installedversions.dat'), 'wb') as instversionsfile:
            pickle.dump([version], instversionsfile)

def setupinstalldir(version, workingDir):
    installdir = os.path.join(workingDir,'game','{}_vanilla_install'.format(version))
    os.makedirs(installdir, exist_ok=True)
    return installdir

def writeassetindex(assetindexurl, versionjson, workingDir, installdir):
    assetversion = versionjson["assets"]
    os.makedirs(os.path.join(workingDir, 'game',installdir,'assets','indexes'), exist_ok=True)
    with open(os.path.join(workingDir, 'game',installdir,'assets','indexes','{}.json'.format(assetversion)), 'w') as assetindexfile:
        data = requests.get(assetindexurl)
        assetindexfile.write(data.text)

#
#
#   Gets the version json file

def getversionjson(version,workingDir, resourceDir):

    # Grabbing all versions and their JSON download URLs from the "version-json-downloads.json" file (in the current launcher version)
    with open(os.path.join(resourceDir, 'version-json-downloads.json'), 'r') as versionDict:
        downloadVersionDictionary = json.load(versionDict)

    # Find the corresponding JSON file for that version
    if version in downloadVersionDictionary:
        versionURL = downloadVersionDictionary.get(version)
        versionJSONData = urlopen(versionURL)
    else:
        # Prints an error if that version isn't included in the "version-json-downloads.json" file with a URL definition
        print('! That version could not be found, it is not included in the versions dictionary, it may be inluded in a future update.')
        # Let's the user input their own JSON if they have downloaded one for the version they want to use
        if (input('* You may import a JSON file manually to continue. Would you like to do this? (y/n): ') == 'y'):
            versionJSONData = input('* You may drag a custom JSON into the window now to try it manually.\nThis file will need to be named "[version you initally tried to launch].json" for it to be accepted.\nThis is not officially supported and is not gauranteed to function properly.\nPlace JSON here:\n ')
        else: 
            print('* Returning...')
            return 'failed'
    try:
        JSONlibrary = json.load(versionJSONData)
        print ('\n* Library index found, proceding with downlaod.\n')
    except:
        print ('! Library index not found, this JSON file is not usable.\n')
        return 'failed'
    return JSONlibrary

#
#
#   Gets all the urls

def getallurls(versionjson):
    libraryurls = getllibraryurls(versionjson)
    assetindex = getassetindex(versionjson)
    asseturlsanddirectories = getasseturls(assetindex)
    return asseturlsanddirectories, libraryurls, assetindex



#
#
# Write all the files
    
def downloadeverything(urls,installdir, workingDir):
    startdonwloadassets(urls[0],installdir, workingDir)
    downloadlibraries(urls[1],installdir, workingDir)

#
#
#   Starts the pool to donwload the assets

def startdonwloadassets(asseturls,installdir,workingDir):
    combineddata = list()
    for url in asseturls:
        combineddata.append([url, installdir, workingDir])
    donwnloadpool = multiprocessing.Pool(5)
    donwnloadpool.map(downloadassets, combineddata)

#
#
#           Runs in a pool to get download and write all the asset urls, which is activated by startdownloadassets

def downloadassets(combineddata):
    os.makedirs(os.path.join(combineddata[2],combineddata[1],os.path.dirname(combineddata[0][1])), exist_ok=True)
    with open(os.path.join(combineddata[2],combineddata[1],combineddata[0][1]), "wb") as directory:
        directory.write(requests.get(combineddata[0][0]).content)

#
#
#   Download all the libraries

def writeinstalldata(versionjson, installversion, installdir, workingDir):
    # Getting libraryurls for parsing in next function call (parselibrarydownloads)
    libraryurls = getllibraryurls(versionjson)

    # Getting arguments to pickle for later use when launching..
    names = parselibrarydownloads(libraryurls)
    mainclass = versionjson["mainClass"]
    versiontype = versionjson["type"]
    assetindex = versionjson["assets"]
    
    # Adding these arguments to a dictionary 
    installdata = dict()
    installdata["mainclass"] = mainclass
    installdata["versiontype"] = versiontype
    installdata["assetindex"] = assetindex
    installdata["libraries"] = names

    # Writing this dictionary to a pickle .dat file for later use when launching...
    with open(os.path.join(workingDir, 'game', installdir, 'installdata_{}.dat'.format(installversion)),'wb') as installdatafile:
        pickle.dump(installdata, installdatafile)

def parselibrarydownloads(url):
    names = list()
    for i in enumerate(url):
        names.append(url[i[0]].rpartition('/')[2]) 
    return names

def downloadlibraries(url,installdir, workingDir):
    os.makedirs(os.path.join(installdir,'libraries'),exist_ok=True)
    for i in enumerate(url):
        writtenfile = url[i[0]].rpartition('/')[2]
        with open(os.path.join(workingDir, installdir, 'libraries', writtenfile), "wb") as directory:
            directory.write(requests.get(i[1]).content)
#
#
#       Gets the library jar urls from the version json file

def getllibraryurls(versionjson):
    # Retrieves all download URLs from the JSON file

    jsonurls = list()
    jsondownloads = versionjson['libraries']
    # Makes sure there are not duplicates and sorts out the lwjgl libraries
    [jsonurls.append(u['downloads']['artifact']['url']) for u in jsondownloads if u['downloads']['artifact']['url'] not in jsonurls and "lwjgl" not in u['downloads']['artifact']['url'] and 'log4j' not in u['downloads']['artifact']['url']]

    jsonurls.append(versionjson['downloads']['client']['url'])
    return jsonurls

#
#
# All this does is get the asset index json file for the getasseturls function


def getassetindex(versionjson):
    # Grabs asset index to pass to asset downlaod
    assetindex = versionjson['assetIndex']['url']
    return assetindex

#
#
#       Gets the urls for all the assets, and the directories to write them to

def getasseturls(assetindex):
    assets = json.load(urlopen(assetindex))
    objects = assets["objects"]
    downloadurls = list()
    writedirectories = list()
    for i in objects:
        hash = objects[i]["hash"]
        hashprefixed = '{}/{}'.format(hash[:2],hash)
        downloadurls.append(["https://resources.download.minecraft.net/{}".format(hashprefixed),os.path.join('assets', 'objects', hashprefixed)])
    return downloadurls

if __name__ == "__main__":
    install(input("Version?:"))
