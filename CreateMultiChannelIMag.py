
import os
import imagej 
import glob
from ij import IJ
from ij.plugin.frame import RoiManager
from ij import WindowManager as wm

def run():
    Ch0dir = '/Volumes/TRANSCEND/Claudia/LGR5SegmentationTraining/DeformOriginalCh0/'
    Ch1dir = '/Volumes/TRANSCEND/Claudia/LGR5SegmentationTraining/DeformOriginalCh1/'
    DoubleChdir = '/Volumes/TRANSCEND/Claudia/LGR5SegmentationTraining/DeformDoubleChannelOriginal/'
    Raw_path = os.path.join(Ch0dir, '*tif')
    X = glob.glob(Raw_path)
    axes = 'YX'
    for fname in X:
      print(fname)
      IJ.open(fname);
      imp = IJ.getImage()
      Name = os.path.basename(os.path.splitext(fname)[0])
      Ch1Name = Ch1dir + Name + '.tif'
      IJ.open(Ch1Name);
      impCh1 = IJ.getImage()
      IJ.run("Merge Channels...", "c1="+imp.getTitle()+ " c2="+impCh1.getTitle()+ " create");
      IJ.saveAs('.tif', DoubleChdir +  Name);
      imp.close();
      impCh1.close();
      composite = wm.getFrontWindow()
      if composite is not None: done = composite.close()
run()