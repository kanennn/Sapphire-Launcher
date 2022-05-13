# (Mostly) Empty initilization module to verify this folder as a package :D
import sys
import os
from multiprocessing import freeze_support

import Sapphire.__main__

freeze_support()

isFrozen = getattr(sys, "frozen", False)
resourceDir = getattr(sys, "_MEIPASS", os.path.join(os.getcwd()))
if isFrozen:
    workingDir = os.path.join(os.path.expanduser("~"), ".Sapphire")
else:
    workingDir = os.path.join(os.getcwd(), ".Sapphire")
