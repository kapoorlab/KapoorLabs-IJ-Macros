from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views

from jarray import zeros  

from  net.imglib2 import FinalInterval;
imp = IJ.getImage()
image = IJF.wrap(imp)

min = zeros(image.numDimensions(),'l')
max = zeros(image.numDimensions(),'l')
min[image.numDimensions()-1] = 0
max[image.numDimensions()-1] =  image.dimension( image.numDimensions()-1 ) - 1
for  d in range(0, image.numDimensions()-1):
            
            min[ d ] =  - 10 ;
            max[ d ] = image.dimension( d ) + 10 ;
interval = FinalInterval( min, max );        
print(interval)
infinite = Views.extendZero( image );
IJF.show( Views.interval( infinite, interval ) );