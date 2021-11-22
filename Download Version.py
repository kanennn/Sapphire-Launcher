import json
import downloadAssets
import urllib
import sys
from urllib.request import urlopen

def installVersion (version):

    # Grabbing all versions and their JSON download URLs from the "version-json-downloads.json" file (in the current launcher version)
    with open('version-json-downloads.json', 'r') as versionDict:
        downloadVersionDictionary = json.load(versionDict)

    # Find the corresponding JSON file for that version
    try:
        versionURL = downloadVersionDictionary.get(version)
        versionJSONData = urlopen(versionURL)
    except:
        # Prints an error if that version isn't included in the "version-json-downloads.json" file with a URL definition
        print('That version could not be found, it is not included in the versions dictionary, it may be inluded in a future update.')
        # Let's the user input their own JSON if they have downloaded one for the version they want to use
        if (input('You may import a JSON file manually to continue. Would you like to do this?\n') == 'Yes'):
            versionJSONData = input('You may drag a custom JSON into the window now to try it manually.\nThis file will need to be named "[version you initally tried to launch].json" for it to be accepted.\nThis is not officially supported and is not gauranteed to function properly.\nPlace JSON here:\n ')
    try:
        JSONlibrary = json.load(versionJSONData)
        print ('\nLibrary found, proceding with downlaod.\n')
    except:
        print ('Library not found, this JSON file is not useable.')
        exit

    # Retrieves all download URLs from the JSON file

    JSONurls = list()
    JSONdownloads = JSONlibrary['libraries']
    for url in JSONdownloads:
        temp = (url['downloads']['artifact']['url'])
        JSONurls.append(temp)
    JSONurls.append(JSONlibrary['downloads']['client']['url'])
        # removes all lwjgl urls (since they are not needed)
    AllLibraryDownloads = [i for i in JSONurls if "lwjgl" not in i]

    # Grabs asset index to pass to asset downlaod
    assets = JSONlibrary['assetIndex']['url']

    # Downloads Assets

    downloadAssets.downloadassets(assetsjson=assets)

    #for url in JSONlibrary['libraries']:
    #    print (url['downloads']['artifact']['url'])