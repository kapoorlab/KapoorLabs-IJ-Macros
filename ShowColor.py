
#This is a jython script to display image with a lookuptable
#@ ImagePlus imp

import ij.IJ as IJ
from time import sleep
import math
dimensions = imp.getDimensions()

print('Your image dimensions are:', dimensions )

#Choose the Z dimension
Zdim = dimensions[3]
for i in range(0, 100):
 IJ.beep()
 sleep(0.2 * abs(math.sin(i)))
 sleep(0.5 * abs(math.exp(-i + 1)))
 sleep(0.3 * abs(math.cos(i)))
 sleep(0.8 * abs(math.exp(-i + 1)))
#for i in range(0,Zdim):
  #IJ.run("Enhance Contrast", "saturated=0.35");
  
  #IJ.run("glasbey");
  
  #IJ.run("Enhance Contrast", "saturated=0.35");

