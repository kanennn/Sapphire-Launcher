import os
import pickle

from MBasiC.downloadstaticlibs import *

def launchcheck():
    if not ifstaticsinstalled():
        downloadstatics()
        
def ifstaticsinstalled():
    if os.path.exists('data/staticsinstalled.dat'):
        with open('data/staticsinstalled.dat','rb') as staticsinst:
            loadedstaticsinst = pickle.load(staticsinst)
            if loadedstaticsinst:
                return True
            elif not loadedstaticsinst:
                return False
    else:
        return False

if __name__ == "__main__":
    launchcheck()