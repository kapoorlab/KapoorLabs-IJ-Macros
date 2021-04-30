#@ Float(label="Size(um)", required=true, value=4, stepSize=0.1) cell
#@ Float(label="Min intensity peak", required=true, value=5, stepSize=0.5) min_peak
#@ Boolean(label='Find Maxima', value=True) WhiteBackground
# Varun n Claudia 3D spot detection macro 
from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.type.numeric.real import DoubleType
from jarray import zeros  
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

zero = img.randomAccess().get().createVariable()

if WhiteBackground:
   Type = DogDetection.ExtremaType.MINIMA
else:
   Type = DogDetection.ExtremaType.MAXIMA   
dog = DogDetection(Views.extendValue(img, zero), img,
                   [cal.pixelWidth, cal.pixelHeight, cal.pixelDepth],
                   cell / 2, cell,
                   Type,
                   min_peak, False,
                   DoubleType())

peaks = dog.getPeaks()

roi = OvalRoi(0, 0, cell/cal.pixelWidth, cell/cal.pixelHeight)  

p = zeros(img.numDimensions(), 'i')  
overlay = Overlay()
imp.setOverlay(overlay)
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
