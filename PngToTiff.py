import os

import glob
from ij import IJ
from ij.plugin.frame import RoiManager
from ij import ImagePlus
from ij.process import FloatProcessor
from ij.plugin import ImageCalculator


SourceDir = '/Users/rando/Downloads/NLM-MontgomeryCXRSet/MontgomerySet/CXR_png'

savedir = '/Users/rando/Downloads/NLM-MontgomeryCXRSet/MontgomerySet/ManualMask/Raw/'




Raw_path = os.path.join(SourceDir, '*png')
X = glob.glob(Raw_path)
axes = 'YX'
for fname in X:
  print(fname)
  IJ.open(fname);
  imp = IJ.getImage()
  width = imp.width
  height = imp.height

  title_left = imp.getTitle();
  
  print(title_left)
  Name = os.path.basename(os.path.splitext(fname)[0])   
  IJ.saveAs(imp, '.tif', savedir +  Name);
  imp.close();
               





