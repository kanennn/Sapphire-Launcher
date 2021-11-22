import json
import urllib
from urllib.request import urlopen
import multiprocessing as mp

def download(o):
    h = o[1]["hash"]
    print('Hash:', h)
    filename = "{}/{}".format(h[:2], h)
    print ('filename:', filename)
    dirname = "assets/objects/{}".format(filename)
    print ('"dirname"', dirname)
    url = "https://resources.download.minecraft.net/{}".format(filename)
    print('url:', url)

if __name__ == "__main__":
    index = json.load(urlopen("https://launchermeta.mojang.com/v1/packages/e5af543d9b3ce1c063a97842c38e50e29f961f00/1.17.json"))
    obj = index["objects"]
    o = [[x[0], obj[x[1]]] for x in enumerate(obj.keys())]
    pool = mp.Pool(20)
    pool.map(download, o)
