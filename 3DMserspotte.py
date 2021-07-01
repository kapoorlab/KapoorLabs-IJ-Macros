#@ Float(label="Size(um)", required=true, value=4, stepSize=0.5) radius
#@ Float(label="Min intensity peak", required=true, value=1, stepSize=0.5) threshold
#@ Float(label="Delta", required=true, value=5, stepSize=0.5) delta
#@ Float(label="minSize", required=true, value=5, stepSize=0.5) minSize
#@ Float(label="maxSize", required=true, value=500, stepSize=0.5) maxSize
#@ Float(label="maxVar", required=true, value=0.5, stepSize=0.1) maxVar
#@ Float(label="minDiversity", required=true, value=0.5, stepSize=0.1) minDiversity
#@ Boolean(label='Find Maxima', value=True) WhiteBackground
# Varun n Claudia 3D spot detection macro 


import net.imglib2.algorithm
from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.algorithm.componenttree.mser import MserTree
from net.imglib2.type.numeric.real import DoubleType
from jarray import zeros  
import math
from java.awt import Color
from ij.gui import PointRoi, OvalRoi , Overlay, EllipseRoi
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, Toolbar
from net.imglib2.view import Views
from net.imglib2.img.display.imagej import ImageJFunctions
from ij.gui import PointRoi, OvalRoi , Overlay
from ij.plugin.frame import RoiManager
from ij.gui import PointRoi



img = ImageJFunctions.wrap(imp)
interval = img
cal = imp.getCalibration()
# Get the calibration from the metadata if exists
calibration = [cal.pixelWidth, cal.pixelHeight, cal.pixelDepth]
overlay = Overlay()

if WhiteBackground:
   
   darkToBright = False
else:
     
   darkToBright = True




def getDeltaVariable( inputimg, delta ):
	
		a = inputimg.randomAccess()
		inputimg.min( a )
		deltaT = a.get().createVariable()
		deltaT.setReal( delta )
		return deltaT		                                      
newtree = MserTree.buildMserTree(img, getDeltaVariable( img, delta ), int(minSize), int(maxSize), maxVar,minDiversity,darkToBright )

rootset = newtree.roots()
		
rootsetiterator = rootset.iterator()
ellipselist = []

while rootsetiterator.hasNext():

			rootmser = rootsetiterator.next();

			if rootmser.size() > 0:

				meanandcov = [ rootmser.mean()[0], rootmser.mean()[1], rootmser.cov()[0],
						rootmser.cov()[1], rootmser.cov()[2] ]
				ellipselist.append(meanandcov)
				

			


for index in range( 0,len(ellipselist)):
				
				
				
				mean = [ ellipselist[index][0], ellipselist[index][1] ]
				cov = [ ellipselist[index][2], ellipselist[index][3],
						ellipselist[index][4] ];
				a = cov[0];
				b = cov[1];
				c = cov[2];
				d = math.sqrt(a * a + 4 * b * b - 2 * a * c + c * c)
				scale1 = math.sqrt(0.5 * (a + c + d)) * 3
				scale2 = math.sqrt(0.5 * abs((a + c - d))) * 3
				
				if scale1 > 0:
						theta = 0.5 * math.atan2((2 * b), (a - c))
						x = mean[0]
						y = mean[1]
						
						dx = scale1 * math.cos(theta)
						dy = scale1 * math.sin(theta)
						oval = EllipseRoi(x - dx, y - dy, x + dx, y + dy, scale2 / scale1)
						oval.setColor(Color.GREEN)
						overlay.add(oval)   