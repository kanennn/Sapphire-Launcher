import os

def createworkingdir(workingDir):
    if not os.path.exists(workingDir):
        os.makedirs(workingDir,exist_ok=True)

def createsubdirectories(workingDir):
    if not os.path.exists(os.path.join(workingDir, 'data')):
        os.makedirs(os.path.join(workingDir, 'data'), exist_ok=True)