
#This is a jython script to display image with a lookuptable


import ij.IJ as IJ
from time import sleep
import math


for i in range(0, 100):
 if IJ.escapePressed():
    break
 IJ.beep()
 sleep(0.25 * abs(math.sin(i)))
 sleep(0.55 * abs(math.exp(-i + 1)))
 sleep(0.35 * abs(math.cos(i)))
 sleep(0.65 * abs(math.exp(-i + 1)))
