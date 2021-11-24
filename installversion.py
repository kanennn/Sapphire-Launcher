import os
import multiprocessing
import json
import urllib
from urllib.request import urlopen
import requests
import pickle

#
#
# Main install control function

def install(version):
    versionjson = getversionjson(version)
    allurls = getallurls(versionjson)
    downloadeverything(allurls)
    addinstalledmark(version)
    picklibnames(versionjson, version)

def addinstalledmark(version):
    if os.path.exists('installeversions.dat'):
        with open('installedversions.dat', 'ab') as instversionsfile:
            installedversions = pickle.load(instversionsfile)
            installedversions.append(version)
            pickle.dump(installedversions)
    else:
        installedversions = list(version)
        with open('installeversions.dat', 'wb') as instversionsfile:
            pickle.dump(installedversions)

        

#
#
#   Gets the version json file

def getversionjson(version):

    # Grabbing all versions and their JSON download URLs from the "version-json-downloads.json" file (in the current launcher version)
    with open('version-json-downloads.json', 'r') as versionDict:
        downloadVersionDictionary = json.load(versionDict)

    # Find the corresponding JSON file for that version
    if version in downloadVersionDictionary:
        versionURL = downloadVersionDictionary.get(version)
        versionJSONData = urlopen(versionURL)
    else:
        # Prints an error if that version isn't included in the "version-json-downloads.json" file with a URL definition
        print('!\tThat version could not be found, it is not included in the versions dictionary, it may be inluded in a future update.')
        # Let's the user input their own JSON if they have downloaded one for the version they want to use
        if (input('*\tYou may import a JSON file manually to continue. Would you like to do this? (y/n):\t') == 'y'):
            versionJSONData = input('*\tYou may drag a custom JSON into the window now to try it manually.\nThis file will need to be named "[version you initally tried to launch].json" for it to be accepted.\nThis is not officially supported and is not gauranteed to function properly.\nPlace JSON here:\n ')
        else: 
            print('*\tReturning...')
            exit
    try:
        JSONlibrary = json.load(versionJSONData)
        print ('\n*\tLibrary index found, proceding with downlaod.\n')
    except:
        print ('!\tLibrary index not found, this JSON file is not usable.\n')
        return
    return JSONlibrary

#
#
#   Gets all the urls

def getallurls(versionjson):
    libraryurls = getllibraryurls(versionjson)
    assetindex = getassetindex(versionjson)
    asseturlsanddirectories = getasseturls(assetindex)
    return asseturlsanddirectories, libraryurls

#
#
# Write all the files
    
def downloadeverything(urls):
    startdonwloadassets(urls[0])
    downloadlibraries(urls[1])

#
#
#   Starts the pool to donwload the assets

def startdonwloadassets(asseturls):
    donwnloadpool = multiprocessing.Pool(5)
    donwnloadpool.map(downloadassets, asseturls)

#
#
#           Runs in a pool to get download and write all the asset urls, which is activated by startdownloadassets

def downloadassets(url):
    os.makedirs(os.path.dirname(url[1]), exist_ok=True)
    with open(url[1], "wb") as directory:
        directory.write(requests.get(url[0]).content)

#
#
#   Download all the libraries

def picklibnames(versionjson,installversion):
    libraryurls = getllibraryurls(versionjson)
    names = parselibrarydownloads(libraryurls)
    with open('librarylist_{}.dat'.format(installversion),"wb") as librarylist:
        pickle.dump(names, librarylist)

def parselibrarydownloads(url):
    names = list()
    for i in enumerate(url):
        names.append(url[i[0]].rpartition('/')[2]) 
    return names

def downloadlibraries(url):
    os.makedirs('libraries',exist_ok=True)
    for i in enumerate(url):
        writtenfile = url[i[0]].rpartition('/')[2]
        with open('libraries/{}'.format(writtenfile), "wb") as directory:
            directory.write(requests.get(i[1]).content)
#
#
#       Gets the library jar urls from the version json file

def getllibraryurls(versionjson):
    # Retrieves all download URLs from the JSON file

    jsonurls = list()
    jsondownloads = versionjson['libraries']
    for url in jsondownloads:
        temp = (url['downloads']['artifact']['url'])
        jsonurls.append(temp)
    jsonurls.append(versionjson['downloads']['client']['url'])

    # filters out all lwjgl urls (since they are not needed)
    librarydownlaods = [i for i in jsonurls if "lwjgl" not in i]    
    return librarydownlaods

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
        downloadurls.append(["https://resources.download.minecraft.net/{}".format(hashprefixed),"assets/objects/{}".format(hashprefixed)])
    return downloadurls

if __name__ == "__main__":
    install(input("Version?:"))
