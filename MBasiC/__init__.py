# (Mostly) Empty initilization module to verify this folder as a package :D
import sys
import os
import MBasiC.__main__

isFrozen = getattr(sys, 'frozen', False)
resourceDir = getattr(sys, '_MEIPASS', os.path.join(os.getcwd(), 'resources'))
if isFrozen:
    workingDir = os.path.join(os.path.expanduser('~'), '.MBasiC')
else:
    workingDir = os.path.join(os.getcwd(), '.MBasiC')