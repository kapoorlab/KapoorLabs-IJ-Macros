# A script to find cells by difference of Gaussian using imglib2.
# Uses as an example the "first-instar-brain.tif" RGB stack availalable
# from Fiji's "Open Samples" menu.

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
rm.addRoi(boundRect)



imp = IJ.getImage()
cal = imp.getCalibration() # in microns

img = IJF.wrap(imp)

print(img.dimensions)
# Create a variable of the correct type (UnsignedByteType) for the value-extended view
zero = img.randomAccess().get().createVariable()

# Run the difference of Gaussian
cell = 30.0 # microns in diameter
min_peak = 10.0 # min intensity for a peak to be considered
dog = DogDetection(Views.extendValue(img, zero), img,
                   [cal.pixelWidth, cal.pixelHeight],
                   cell / 2, cell,
                   DogDetection.ExtremaType.MAXIMA, #MAXIMA
                   min_peak, False,
                   DoubleType())

peaks = dog.getPeaks()
roi = OvalRoi(0, 0, cell/cal.pixelWidth, cell/cal.pixelHeight)  
print ('Number of cells = ', len(peaks))
p = zeros(img.numDimensions(), 'i')  
overlay = Overlay()
imp.setOverlay(overlay)
for peak in peaks:  
  # Read peak coordinates into an array of integers  
  peak.localize(p)  
  if(boundRect.contains(p[0], p[1])):
      oval = OvalRoi(p[0], p[1],cell/cal.pixelWidth, cell/cal.pixelHeight)
      oval.setColor(Color.RED)
      overlay.add(oval)  
  
