# @ImagePlus imp

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
rm = RoiManager.getInstance()
if not rm:
        rm = RoiManager()
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
peakslist = []
peakscovarlist = []

while rootsetiterator.hasNext():

			rootmser = rootsetiterator.next();

			if rootmser.size() > 0:
			    peaks = rootmser.mean()
			    peakscovar = rootmser.cov()
			    peakslist.append(meanandcov)
			    peakscovarlist.append(peakscovar)

			


for index in range( 0,len(peakslist)):
				
			
				
				mean = peakslist[index]
				cov = peakscovarlist[index];
				a = cov[0];
				b = cov[1];
				c = cov[2];
				d = math.sqrt(a * a + 4 * b * b - 2 * a * c + c * c)
				scale1 = math.sqrt(0.5 * (a + c + d)) * 3
				scale2 = math.sqrt(0.5 * abs((a + c - d))) * 3
				print(a)
				if scale1 > 0:
						theta = 0.5 * math.atan2((2 * b), (a - c))
						x = mean[0]/ cal.pixelWidth
						y = mean[1]/cal.pixelHeight
						
						dx = scale1 * math.cos(theta)/ cal.pixelWidth
						dy = scale1 * math.sin(theta)/cal.pixelHeights
						oval = EllipseRoi(x - dx, y - dy, x + dx, y + dy, scale2 / scale1)
						oval.setColor(Color.GREEN)
						oval.setPosition(int(round(mean[2] / cal.pixelDepth))+1)
						overlay.add(oval)   
						rm.addRoi(oval)