from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.type.numeric.real import DoubleType
from jarray import zeros  
from java.awt import Color
from ij.gui import PointRoi, OvalRoi , Overlay, Line 
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, Toolbar
from net.imglib2.view import Views
from ij.gui import GenericDialog

imp = IJ.getImage()
IJ.run("Select None")
overlay = imp.getOverlay()
if overlay == None:

				overlay = Overlay();
				imp.setOverlay(overlay);

			
else:
				overlay.clear();

imp.updateAndDraw()
impY = imp.getHeight()
impX = imp.getWidth()
print(impY, impX)
rm = RoiManager.getInstance()
if not rm:
	rm = RoiManager()
rm.runCommand("reset")
WaitForUserDialog("Select the landmark and the second point.").show();
rm.runCommand("Add");



roi_points = rm.getRoisAsArray()

for Roi in roi_points:
        
        xpoints = Roi.getPolygon().xpoints
        ypoints = Roi.getPolygon().ypoints
        print(xpoints, ypoints)
print('Start Landmark',xpoints[0], ypoints[0])
fixedpointX = xpoints[0]
fixedpointY = ypoints[0]
print('End Landmark',xpoints[1], ypoints[1])

IJ.makeLine(xpoints[0], ypoints[0],xpoints[1], ypoints[1])
gui = GenericDialog("Rotation Angle")
gui.addNumericField("ChooseAngle", 15, 0)
gui.showDialog() 
if gui.wasOKed():
    
    rotateangle = gui.getNextNumber()
    print(rotateangle)
    IJ.run("Rotate...", "angle="+str(int(float(rotateangle))));
rm.runCommand("reset")
overlay = imp.getOverlay()  
rm.runCommand("Add");  
roi_points = rm.getRoisAsArray()

for Roi in roi_points:
        xpoints = Roi.getPolygon().xpoints
        ypoints = Roi.getPolygon().ypoints
        print(xpoints, ypoints)

print('Rotated Start Landmark',xpoints[0], ypoints[0])

print('Rotated End Landmark',xpoints[1], ypoints[1])        
slope = (ypoints[1] - ypoints[0])/ (xpoints[1] - xpoints[0] + 1.0E-20)   
intercept = fixedpointY - slope * fixedpointX
print(fixedpointX, fixedpointY)
print('Slope', slope, 'Intercept', intercept)
XwY0 = -intercept/slope
YxwY0 = slope * XwY0 + intercept

XwYmax = (impY -intercept)/slope
YxwYmax = slope * XwYmax + intercept


YwX0 = intercept
XywX0 = (YwX0 - intercept)/slope

YwXmax = impX * slope + intercept
XxwXmax = (YwXmax - intercept)/slope

#rm.runCommand("reset")


  
rm.runCommand("Add");
if XwY0 > 0:
		lineROIA = Line(fixedpointX, fixedpointY,XwY0, YxwY0)
		lineROIB = Line(fixedpointX, fixedpointY,XwYmax, YxwYmax)
		overlay.add(lineROIA)
		overlay.add(lineROIB) 
if XwY0 < 0:
		lineROIA = Line(fixedpointX, fixedpointY,XywX0, YwX0)
		lineROIB = Line(fixedpointX, fixedpointY,XxwXmax, YwXmax)
		overlay.add(lineROIA)
		overlay.add(lineROIB)		

#IJ.makeLine(fixedpointX, fixedpointY,0, YwX0)
  

