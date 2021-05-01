#@ Dataset data
#@ Float(label="hMin", required=true, value=42, stepSize=1) hMin
#@ Float(label="thresh", required=true, value=100, stepSize=1) thresh
#@ Float(label="peakFlooding", required=true, value=100, stepSize=1) peakFlooding
#@ Float(label="GaussBlur (pixel)", required=true, value=2, stepSize=0.5) blurradius
#@ Boolean(label='outputMask', value=True) outputMask
#@ Boolean(label='allowSplit', value=True) allowSplit
#@OUTPUT Dataset output
#@OUTPUT Dataset output_skel
#@OUTPUT Dataset output_label
#@ OpService ops
#@ DatasetService ds
#@ UIService ui
# Run a HWatershed filter on all the frames along the TIME axis.
# After the filtering step the image is clipped to match the input type.
# Varun n Claudia Membrane segmentation macro 
from net.imagej.axis import Axes
from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi.labeling import LabelRegions
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.roi import Regions
from net.imglib2.algorithm.neighborhood import HyperSphereShape
from net.imagej.axis import CalibratedAxis
from net.imglib2.view import Views
import os

from net.imagej.axis import Axes
from net.imagej import ImgPlus

name = os.path.basename(os.path.splitext(data.getImgPlus().name)[0])


axes = [Axes.X, Axes.Y, Axes.TIME]
dataImg = ImgPlus(data.getImgPlus().copy(), "Result", axes)


original = ops.convert().float32(dataImg)

converted = ops.filter().gauss(original, blurradius)
imp = IJF.show(converted)
# H-watershed returns a label map as an ImagePlus
labelimage = ops.run("H_Watershed", imp, hMin, thresh, peakFlooding, outputMask, allowSplit )
ui.show(labelimage)
