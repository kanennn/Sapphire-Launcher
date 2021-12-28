# (Mostly) Empty initilization module to verify this folder as a package :D
import sys
import os

isFrozen = getattr(sys, 'frozen', False)
path = getattr(sys, '_MEIPASS', os.getcwd())