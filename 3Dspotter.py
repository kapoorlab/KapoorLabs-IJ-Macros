# @ImagePlus imp
#@ Float(label="Size(um)", required=true, value=4, stepSize=0.5) radius
#@ Float(label="Min intensity peak", required=true, value=1, stepSize=0.5) threshold
#@ Boolean(label='Median filter image', value=True) doMedian
#@ Boolean(label='Sub pixel peaks', value=True) doSubpixel
# Varun n Claudia 3D spot detection macro based on trackmate
# Imports
from fiji.plugin.trackmate.detection import LogDetector
from net.imglib2.img.display.imagej import ImageJFunctions
from ij.gui import PointRoi, OvalRoi , Overlay
from ij.plugin.frame import RoiManager
from ij.gui import PointRoi
from java.awt import Color 
# Set the parameters for LogDetector
img = ImageJFunctions.wrap(imp)
interval = img
cal = imp.getCalibration()
# Get the calibration from the metadata if exists
calibration = [cal.pixelWidth, cal.pixelHeight, cal.pixelDepth]
overlay = Overlay()
 
 
# Setup spot detector (see http://javadoc.imagej.net/Fiji/fiji/plugin/trackmate/detection/LogDetector.html)
# Trackmate spot detector

 
detector = LogDetector(img, interval, calibration, radius, threshold, doSubpixel, doMedian)
 
# Start processing and display the results
if detector.process():
    # Get the list of peaks found
    peaks = detector.getResult()
    print str(len(peaks)), "peaks were found."
 
    # Add points to ROI manager
    rm = RoiManager.getInstance()
    if not rm:
        rm = RoiManager()
 
    # Loop through all the peak that were found
    for peak in peaks:
        # Print the current coordinates
        print "peaks", peak.getDoublePosition(0), peak.getDoublePosition(1), peak.getDoublePosition(2)
        # Add the current peak to the Roi manager
        roi = PointRoi(peak.getDoublePosition(0) / cal.pixelWidth, peak.getDoublePosition(1) / cal.pixelHeight)
        oval = OvalRoi(int(peak.getDoublePosition(0)/cal.pixelWidth  - 0.5 *radius/cal.pixelWidth), int(peak.getDoublePosition(1)/cal.pixelHeight - 0.5 * radius/cal.pixelHeight),radius/cal.pixelWidth, radius/cal.pixelHeight)
        oval.setColor(Color.RED)
        # Set the Z position of the peak otherwise the peaks are all set on the same slice
        oval.setPosition(int(round(peak.getDoublePosition(2) / cal.pixelDepth))+1)
        roi.setPosition(int(round(peak.getDoublePosition(2) / cal.pixelDepth))+1)
        overlay.add(oval)
        imp.setOverlay(overlay);
        imp.updateAndDraw();
        rm.addRoi(oval)
        rm.addRoi(roi)
	    
   
 
else:
    print "The detector could not process the data."