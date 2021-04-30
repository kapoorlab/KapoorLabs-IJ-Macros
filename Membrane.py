#@ Dataset data
#@ Float(label="Sigma 1 (pixel)", required=true, value=4.2, stepSize=0.1) sigma1
#@ Float(label="Sigma 2 (pixel)", required=true, value=1.25, stepSize=0.1) sigma2
#@ Integer(label="Min Size (pixel)", required=true, value=2, stepSize=1) size
#@OUTPUT Dataset output
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
# Convert data to float 32
converted = ops.convert().float32(data.getImgPlus())
 
# Allocate output memory (wait for hybrid CF version of slice)
dog = ops.create().img(converted)
 
# Create the op
dog_op = ops.op("filter.dog", converted, sigma1, sigma2)
 
# Setup the fixed axis
t_dim = data.dimensionIndex(Axes.TIME)
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

output = ds.create(output_binary)
# call connected components to label each connected region
labeling=ops.labeling().cca(output_binary, StructuringElement.EIGHT_CONNECTED)

# get the index image (each object will have a unique gray level)
labelingIndex=labeling.getIndexImg()
IJF.show(labelingIndex)
# get the collection of regions and loop through them
regions=LabelRegions(labeling)
for region in regions:
	# get the size of the region
	size=region.size()

	# get the intensity by "sampling" the intensity of the input image at the region pixels
	intensity=ops.stats().mean(Regions.sample(region, converted)).getRealDouble()

	print "size",size,"intensity",intensity
    
   