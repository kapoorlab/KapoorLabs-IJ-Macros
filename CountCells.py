# @OpService ops
# @ImgPlus img

# A script to find cells by difference of Gaussian using imglib2.
# Uses as an example the "first-instar-brain.tif" RGB stack availalable
# from Fiji's "Open Samples" menu.

from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.type.numeric.real import DoubleType

# Extract the red channel
interval = ops.run("create.img", [img.dimension(0), img.dimension(1), 1, img.dimension(3)], img.firstElement(), img.factory())
red = ops.run("transform.crop", img, interval)

# Create a variable of the correct type (UnsignedByteType) for the value-extended view
extended = ops.run("transform.extendZeroView", red)

# Run the difference of Gaussian
cell = 5.0 # microns in diameter
min_peak = 40.0 # min intensity for a peak to be considered

dog = DogDetection(extended, red,
                   [img.averageScale(0), img.averageScale(1), img.averageScale(3)],
                   cell / 2, cell,
                   DogDetection.ExtremaType.MINIMA,
                   min_peak, False,
                   DoubleType())

peaks = dog.getPeaks()


print len(peaks)
print peaks
