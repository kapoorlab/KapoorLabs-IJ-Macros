#@ Dataset data
#@ Float(label="Sigma 1 (pixel)", required=true, value=4.2, stepSize=0.1) sigma1
#@ Float(label="Sigma 2 (pixel)", required=true, value=1.25, stepSize=0.1) sigma2
#@ Float(label="GaussBlur (pixel)", required=true, value=2, stepSize=0.5) blurradius
#@ Integer(label="Min Size (pixel)", required=true, value=2, stepSize=1) size
#@OUTPUT Dataset output
#@OUTPUT Dataset output_skel
#@OUTPUT Dataset output_label
#@ OpService ops
#@ DatasetService ds
 
# Run a DOG filter on all the frames along the TIME axis.
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
# Convert data to float 32

name = os.path.basename(os.path.splitext(data.getImgPlus().name)[0])


axes = [Axes.X, Axes.Y, Axes.TIME]
dataImg = ImgPlus(data.getImgPlus().copy(), "Result", axes)


original = ops.convert().float32(dataImg)

converted = ops.filter().gauss(original, blurradius)

# Allocate output memory (wait for hybrid CF version of slice)
dog = ops.create().img(converted)
 
# Create the op
dog_op = ops.op("filter.dog", converted, sigma1, sigma2)
 
# Setup the fixed axis
t_dim = dataImg.dimensionIndex(Axes.TIME)

fixed_axis = [d for d in range(0, data.numDimensions()) if d != t_dim]
 
# Run the op
ops.slice(dog, converted, dog_op, fixed_axis)
 
# Clip image to the input type
clipped = ops.create().img(dog, data.getImgPlus().firstElement())
clip_op = ops.op("convert.clip", data.getImgPlus().firstElement(), dog.firstElement())
ops.convert().imageType(clipped, dog, clip_op)

targetCursor = clipped.localizingCursor()

 
# Iterate over each pixels of the datasets
while targetCursor.hasNext():
    targetCursor.fwd()
 
    if targetCursor.get().get() < 0:
        targetCursor.get().set(0) 
    else:
        targetCursor.get().set(1) 
           

shape = HyperSphereShape(size)        
# Create output Dataset


output_binary = ops.run("convert.bit", clipped)

output_binary = ops.morphology().erode(output_binary, [shape])

skel = ops.run("thinMorphological", None, output_binary)


#Create two outputs
output = ds.create(output_binary)
output_skel = ds.create(skel)



copy_output_skel = output_skel.copy()
invert_copy_output_skel = copy_output_skel.copy()
copy_output_skel = ops.morphology().dilate(copy_output_skel, HyperSphereShape(3))

inversetargetCursor = copy_output_skel.localizingCursor()
outputinversetargetRan = invert_copy_output_skel.randomAccess()
while inversetargetCursor.hasNext():
     inversetargetCursor.fwd()

     outputinversetargetRan.setPosition(inversetargetCursor)
     if (inversetargetCursor.get().get() == 1):
          value = 0
     if (inversetargetCursor.get().get() == 0):
          value = 1
     outputinversetargetRan.get().set(value)   
 
     
    


# call connected components to label each connected region
labeling=ops.labeling().cca(invert_copy_output_skel, StructuringElement.EIGHT_CONNECTED)

# get the index image (each object will have a unique gray level)
labelingIndex=labeling.getIndexImg()

# get the collection of regions and loop through them
regions=LabelRegions(labeling)
for region in regions:
	# get the size of the region
	size=region.size()

	# get the intensity by "sampling" the intensity of the input image at the region pixels
	intensity=ops.stats().mean(Regions.sample(region, original)).getRealDouble()

	print "size",size,"intensity",intensity

    
output_label = ds.create(labelingIndex)   