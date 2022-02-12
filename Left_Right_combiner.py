
import os

import glob
from ij import IJ
from ij.plugin.frame import RoiManager
from ij import ImagePlus
from ij.process import FloatProcessor
from ij.plugin import ImageCalculator

def run():
    leftdir = '/Users/rando/Downloads/NLM-MontgomeryCXRSet/MontgomerySet/ManualMask/leftMask/'
    rightdir = '/Users/rando/Downloads/NLM-MontgomeryCXRSet/MontgomerySet/ManualMask/rightMask/'
    savedir = '/Users/rando/Downloads/NLM-MontgomeryCXRSet/MontgomerySet/ManualMask/BinaryMask/'
    Raw_path = os.path.join(leftdir, '*png')
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
      RightName = rightdir + title_left
   
      IJ.open(RightName) 
      imp_right = IJ.getImage() 
      title_right = imp_right.getTitle()
      print(title_right)
     
      imp_res =  ImageCalculator.run(imp, imp_right, "add create 8-bit");
      title = imp_res.getTitle()
      IJ.saveAs(imp_res, '.tif', savedir +  Name);
      imp.close();
      imp_right.close();
      imp_res.close();

run()