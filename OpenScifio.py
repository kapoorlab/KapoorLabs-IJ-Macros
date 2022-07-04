#@ LocationService ls
import net.imagej.ImageJ as ImageJ
from ij import IJ;
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
imagepath = '/gpfsdsstore/projects/rech/jsy/uzj81mi/Mari_Data/Dataset2/for_tracking_tiltcorrected_cropped/Varun_tracking_experiments/Experiment_1.tif'
location = ls.resolve(imagepath)
ij = ImageJ();
image = ij.scifio().datasetIO().open(location);
IJF.show(image)