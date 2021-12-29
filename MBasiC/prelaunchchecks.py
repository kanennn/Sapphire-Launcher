import os
import pickle

import MBasiC.downloadstaticlibs as statics
import MBasiC.initialsetup as initset

def launchcheck(workingDir):
    
    setups(workingDir)

    if not ifstaticsinstalled(workingDir):
        statics.downloadstatics(workingDir)
        
def ifstaticsinstalled(workingDir):
    if os.path.exists(os.path.join(workingDir,'data','staticsinstalled.dat')):
        with open(os.path.join(workingDir,'data','staticsinstalled.dat'),'rb') as staticsinst:
            loadedstaticsinst = pickle.load(staticsinst)
            if loadedstaticsinst:
                return True
            elif not loadedstaticsinst:
                return False
    else:
        return False

def setups(workingDir):
    initset.createworkingdir(workingDir)
    initset.createsubdirectories(workingDir)

if __name__ == "__main__":
    launchcheck()