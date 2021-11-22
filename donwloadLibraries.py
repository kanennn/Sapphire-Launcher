import json
import downloadAssets
import urllib
import sys
from urllib.request import urlopen

def installVersion (libjson):
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