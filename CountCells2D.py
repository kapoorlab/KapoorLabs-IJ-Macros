# A script to find cells by difference of Gaussian using imglib2.
# Uses as an example the "first-instar-brain.tif" RGB stack availalable
# from Fiji's "Open Samples" menu.

from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.type.numeric.real import DoubleType


# Fetch the "first-instar-brain.tif" file
#imp = IJ.openImage("http://downloads.imagej.net/fiji/snapshots/samples/first-instar-brain.zip")
imp = IJ.getImage()
cal = imp.getCalibration() # in microns

img = IJF.wrap(imp)

# Extract the red channel


# Create a variable of the correct type (UnsignedByteType) for the value-extended view
zero = img.randomAccess().get().createVariable()

# Run the difference of Gaussian
cell = 5.0 # microns in diameter
min_peak = 40.0 # min intensity for a peak to be considered
dog = DogDetection(Views.extendValue(img, zero), img,
                   [cal.pixelWidth, cal.pixelHeight, cal.pixelDepth],
                   cell / 2, cell,
                   DogDetection.ExtremaType.MINIMA,
                   min_peak, False,
                   DoubleType())

peaks = dog.getPeaks()

# Should print 27, but prints zero!
print len(peaks)
