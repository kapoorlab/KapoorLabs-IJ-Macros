from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views

from jarray import zeros  

from  net.imglib2 import FinalInterval;
imp = IJ.getImage()
image = IJF.wrap(imp)

min = zeros(image.numDimensions(),'l')
max = zeros(image.numDimensions(),'l')
min[2] = 0
max[2] =  214
min[0] = 0
max[0] =  4004
min[1] = 0
max[1] =  2127


            
interval = FinalInterval( min, max );        
print(interval)
infinite = Views.extendZero( image );
IJF.show( Views.interval( infinite, interval ) );