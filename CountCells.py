#@ Float(label="Size(um)", required=true, value=4, stepSize=0.1) cell
#@ Float(label="Min intensity peak", required=true, value=5, stepSize=0.5) min_peak
#@ Float(label="Delta", required=true, value=5, stepSize=0.5) delta
#@ Float(label="minSize", required=true, value=5, stepSize=0.5) minSize
#@ Float(label="maxSize", required=true, value=500, stepSize=0.5) maxSize
#@ Float(label="maxVar", required=true, value=0.5, stepSize=0.1) maxVar
#@ Float(label="minDiversity", required=true, value=0.5, stepSize=0.1) minDiversity
#@ Boolean(label='Find Maxima', value=True) WhiteBackground
# Varun n Claudia 3D spot detection macro 


from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.algorithm.componenttree.mser import buildMserTree
from net.imglib2.type.numeric.real import DoubleType
from jarray import zeros  
import math
from java.awt import Color
from ij.gui import PointRoi, OvalRoi , Overlay 
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, Toolbar
from net.imglib2.view import Views
#remove all the previous ROIS
imp = IJ.getImage()
rm = RoiManager.getInstance()
if not rm:
	rm = RoiManager()
rm.runCommand("reset")

#ask the user to define a selection and get the bounds of the selection
IJ.setTool(Toolbar.RECTANGLE)
WaitForUserDialog("Select the area,then click OK.").show();
boundRect = imp.getRoi()
imp.setRoi(boundRect)

#open a XYZ image (split the channels for now)
imp = IJ.getImage()
cal = imp.getCalibration() # in microns

img = IJF.wrap(imp)
print(img.numDimensions())
zero = img.randomAccess().get().createVariable()
overlay = Overlay()
imp.setOverlay(overlay)
if WhiteBackground:
   Type = DogDetection.ExtremaType.MINIMA
   darkToBright = True
else:
   Type = DogDetection.ExtremaType.MAXIMA  
   darkToBright = False
if img.numDimensions() == 3:    

		dog = DogDetection(Views.extendMirrorSingle(img), img,
		                   [cal.pixelWidth, cal.pixelHeight, cal.pixelDepth],
		                   cell / 2, cell,
		                   Type,
		                   min_peak, False,
		                   DoubleType())
elif img.numDimensions() == 2:  
       dog = DogDetection(Views.extendMirrorSingle(img), img,
		                   [cal.pixelWidth, cal.pixelHeight],
		                   cell / 2, cell,
		                   Type,
		                   min_peak, False,
		                   DoubleType())		

		                                      
newtree = buildMserTree(Views.extendMirrorSingle(img), delta, minSize, maxSize, maxVar,minDiversity,darkToBright )

rootset = newtree.roots()
		
rootsetiterator = rootset.iterator()
meanandcovlist = []

while rootsetiterator.hasNext():

			rootmser = rootsetiterator.next();

			if rootmser.size() > 0:

				meanandcov = { rootmser.mean()[0], rootmser.mean()[1], rootmser.cov()[0],
						rootmser.cov()[1], rootmser.cov()[2] }
				meanandcovlist.add(meanandcov)

			
meanandcovchildlist = []	
ellipselist = []	
treeiterator = newtree.iterator();
	       
	       while treeiterator.hasNext():

				mser = treeiterator.next();

				if mser.getChildren().size() > 0:

					for index in range( 0,mser.getChildren().size()) :

						meanandcovchild = { mser.getChildren().get(index).mean()[0],
								mser.getChildren().get(index).mean()[1], mser.getChildren().get(index).cov()[0],
								mser.getChildren().get(index).cov()[1], mser.getChildren().get(index).cov()[2] }

						meanandcovchildlist.add(meanandcovchild)
						ellipselist.add(meanandcovchild)

for index in range( 0,ellipselist.size()):
				
				
				
				
				mean = { ellipselist.get(index)[0], ellipselist.get(index)[1] };
				cov = { ellipselist.get(index)[2], ellipselist.get(index)[3],
						ellipselist.get(index)[4] };
				a = cov[0];
				b = cov[1];
				c = cov[2];
				d = math.sqrt(a * a + 4 * b * b - 2 * a * c + c * c);
				scale1 = math.sqrt(0.5 * (a + c + d)) * 3;
				scale2 = math.sqrt(0.5 * (a + c - d)) * 3;
				theta = 0.5 * math.atan2((2 * b), (a - c));
				x = mean[0];
				y = mean[1];
				dx = scale1 * math.cos(theta)
				dy = scale1 * math.sin(theta)
				oval = EllipseRoi(x - dx, y - dy, x + dx, y + dy, scale2 / scale1)
				oval.setColor(Color.GREEN)
                overlay.add(oval)						
						
				
peaks = dog.getPeaks()

roi = OvalRoi(0, 0, cell/cal.pixelWidth, cell/cal.pixelHeight)  

p = zeros(img.numDimensions(), 'i')  

regionpeak = 0 
for peak in peaks:  
  print(peak)
  # Read peak coordinates into an array of integers  
  peak.localize(p)  
  if(boundRect.contains(p[0], p[1])):
      oval = OvalRoi(p[0] - 0.5 * cell/cal.pixelWidth, p[1] - 0.5 * cell/cal.pixelHeight,cell/cal.pixelWidth,  cell/cal.pixelHeight)
      oval.setColor(Color.RED)
      overlay.add(oval)  
      regionpeak= regionpeak + 1
      rm.addRoi(oval)
print ('Number of cells in region = ', regionpeak, 'Total cells in the image = ', len(peaks)) 
