
import os
import imagej 
import glob
from ij import IJ
from ij.plugin.frame import RoiManager


def run():
    roidir = '/Volumes/TRANSCEND/LauraLeopold/Rois/'
    maskdir = '/Volumes/TRANSCEND/LauraLeopold/Mask/'
    originaldir = '/Volumes/TRANSCEND/LauraLeopold/Original/'
    Raw_path = os.path.join(originaldir, '*tif')
    X = glob.glob(Raw_path)
    axes = 'YX'
    for fname in X:
      print(fname)
      IJ.open(fname);
      imp = IJ.getImage()
      Name = os.path.basename(os.path.splitext(fname)[0])
      RoiName = roidir + Name + '.roi'
      Roi = IJ.open(RoiName)
      rm = RoiManager.getInstance()
      if (rm==None):
         rm = RoiManager()
      rm.addRoi(Roi)
      print(fname, RoiName)
      if not rm:
        print "Please first add some ROIs to the ROI Manager"
        return
      impMask = IJ.createImage("Mask", "8-bit grayscale-mode", imp.getWidth(), imp.getHeight(), imp.getNChannels(), imp.getNSlices(), imp.getNFrames())
      IJ.setForegroundColor(255, 255, 255)
      rm.runCommand(impMask,"Deselect")
      rm.runCommand(impMask,"Fill")
      rm.runCommand('Delete')
      IJ.saveAs(impMask, '.tif', maskdir +  Name);
      imp.close();

run()