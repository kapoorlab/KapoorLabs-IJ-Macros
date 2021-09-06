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

imp = IJ.getImage()
IJ.run("Select None")
overlay = imp.getOverlay()
if overlay == None:

				overlay = Overlay();
				imp.setOverlay(overlay);

			
else:
				overlay.clear();

imp.updateAndDraw()

rm = RoiManager.getInstance()
if not rm:
	rm = RoiManager()
rm.runCommand("reset")
WaitForUserDialog("Select the landmark.").show();
rm.runCommand("Add");

WaitForUserDialog("Select second point.").show();
rm.runCommand("Add");

roi_points = rm.getRoisAsArray()

for Roi in roi_points:
        
        xpoints = Roi.getPolygon().xpoints
        ypoints = Roi.getPolygon().ypoints
        print(xpoints, ypoints)
print('Start Landmark',xpoints[0], ypoints[0])

print('End Landmark',xpoints[1], ypoints[1])

IJ.makeLine(xpoints[0], ypoints[0],xpoints[1], ypoints[1])
   