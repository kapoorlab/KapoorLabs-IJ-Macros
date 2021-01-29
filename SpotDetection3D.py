# A script to find cells by difference of Gaussian using imglib2.
# Uses as an example the "first-instar-brain.tif" RGB stack availalable
#@ File(label='Choose Nuclei Roi directory', style='directory') Nucleiroidir


#@ File(label='Choose OriginalImage directory', style='directory') originaldir
#@ String(label='File types', value='tif') file_type_image
#@ String(label='Filter', value='._') filter_image
#@ Boolean(label='Recursive search', value=True) do_recursive
#@ File(label='Choose SaveSpotSegmentation directory', style='directory') SpotSegdir


from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.type.numeric.real import DoubleType
from jarray import zeros  
from java.awt import Color
from ij.gui import PointRoi, OvalRoi , Overlay 
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, Toolbar
import os
from java.io import File

from ij import IJ
from ij.plugin.frame import RoiManager
from ij import WindowManager as wm

def batch_open_images(pathImage, pathRoi, pathMask, file_typeImage=None,  name_filterImage=None,  recursive=False):
    '''Open all files in the given folder.
    :param path: The path from were to open the images. String and java.io.File are allowed.
    :param file_type: Only accept files with the given extension (default: None).
    :param name_filter: Reject files that contain the given string (default: wild characters).
    :param recursive: Process directories recursively (default: False).
    '''
    # Converting a File object to a string.
    if isinstance(pathImage, File):
        pathImage = pathImage.getAbsolutePath()

    def check_type(string):
        '''This function is used to check the file type.
        It is possible to use a single string or a list/tuple of strings as filter.
        This function can access the variables of the surrounding function.
        :param string: The filename to perform the check on.
        '''
        if file_typeImage:
            # The first branch is used if file_type is a list or a tuple.
            if isinstance(file_typeImage, (list, tuple)):
                for file_type_ in file_typeImage:
                    if string.endswith(file_type_):
                        # Exit the function with True.
                        return True
                    else:
                        # Next iteration of the for loop.
                        continue
            # The second branch is used if file_type is a string.
            elif isinstance(file_typeImage, string):
                if string.endswith(file_typeImage):
                    return True
                else:
                    return False
            return False
        # Accept all files if file_type is None.
        else:
            return True

    def dog_detection(overlay,img, imp, cal):

                 # Create a variable of the correct type (UnsignedByteType) for the value-extended view
				 zero = img.randomAccess().get().createVariable()
				
				 # Run the difference of Gaussian
				 cell = 8.0 # microns in diameter
				 min_peak = 2.0 # min intensity for a peak to be considered
				 dog = DogDetection(Views.extendValue(img, zero), img,
				                   [cal.pixelWidth, cal.pixelHeight,cal.pixelDepth],
				                   cell / 2, cell,
				                   DogDetection.ExtremaType.MINIMA, 
				                   min_peak, False,
				                   DoubleType())
				
				 peaks = dog.getPeaks()
				 roi = OvalRoi(0, 0, cell/cal.pixelWidth, cell/cal.pixelHeight)  
				 print ('Number of cells = ', len(peaks))
			 	 p = zeros(img.numDimensions(), 'i')  
			 	
				 boundRect = imp.getRoi()
				 for peak in peaks:  
				    # Read peak coordinates into an array of integers  XYZ location of spots
				    peak.localize(p)  
				    print(p)
				    if(boundRect is not None and boundRect.contains(p[0], p[1])):
						    oval = OvalRoi(p[0], p[1],cell/cal.pixelWidth,  cell/cal.pixelHeight)
						    oval.setColor(Color.RED)
						    overlay.add(oval) 

    def check_filter(string):
        '''This function is used to check for a given filter.
        It is possible to use a single string or a list/tuple of strings as filter.
        This function can access the variables of the surrounding function.
        :param string: The filename to perform the filtering on.
        '''
        if name_filterImage:
            # The first branch is used if name_filter is a list or a tuple.
            if isinstance(name_filterImage, (list, tuple)):
                for name_filter_ in name_filterImage:
                    if name_filter_ in string:
                        # Exit the function with True.
                        
                        return True
                    else:
                        # Next iteration of the for loop.
                        continue
            # The second branch is used if name_filter is a string.
            elif isinstance(name_filterImage, string):
                if name_filterImage in string:
                    return True
                else:
                    return False
            return False
        else:
        # Accept all files if name_filter is None.
            return True

   

    # We collect all files to open in a list.
    path_to_Image = []
    # Replacing some abbreviations (e.g. $HOME on Linux).
    path = os.path.expanduser(pathImage)
    path = os.path.expandvars(pathImage)
    # If we don't want a recursive search, we can use os.listdir().
    if not recursive:
        for file_name in os.listdir(pathImage):
            full_path = os.path.join(pathImage, file_name)
            if os.path.isfile(full_path):
                if check_type(file_name):
                    if check_filter(file_name):
                        path_to_Image.append(full_path)
    # For a recursive search os.walk() is used.
    else:
        # os.walk() is iterable.
        # Each iteration of the for loop processes a different directory.
        # the first return value represents the current directory.
        # The second return value is a list of included directories.
        # The third return value is a list of included files.
        for directory, dir_names, file_names in os.walk(pathImage):
            # We are only interested in files.
            for file_name in file_names:
                # The list contains only the file names.
                # The full path needs to be reconstructed.
                full_path = os.path.join(directory, file_name)
                # Both checks are performed to filter the files.
                if check_type(file_name):
                    if check_filter(file_name) is False:
                        # Add the file to the list of images to open.
                        path_to_Image.append([full_path, os.path.basename(os.path.splitext(full_path)[0])])
    # Create the list that will be returned by this function.
    Images = []
    Rois = []
    for img_path, file_name in path_to_Image:
        # IJ.openImage() returns an ImagePlus object or None.
        imp = IJ.openImage(img_path)
        imp.show()
        print(img_path)
        if check_filter(file_name):
         continue;
        else: 
         print(file_name  ,  pathRoi)
        RoiName = str(pathRoi) + '/'+ file_name + '_rois' + '.zip'
        
        if os.path.exists(RoiName):
		         Roi = IJ.open(RoiName)
		         imp = IJ.getImage()
		         cal= imp.getCalibration()# in microns
		         img = IJF.wrap(imp)
		         print('Image Dimensions', img.dimensions, 'Calibration', cal)
		         print(Roi)
		         # An object equals True and None equals False.
		         rm = RoiManager.getInstance()
		         if (rm==None):
		            rm = RoiManager()
		         try:   
		           rm.runCommand('Delete')   
		         except:
		           pass  
		         rm.runCommand("Open", RoiName)
		         rois = rm.getRoisAsArray()
		         overlay = Overlay()
				 for (i in range(0,len(rois))):
					overlay.add(rois[i])
				 setOverlay(imp, overlay)
				 
				 
				 
				 
  
def split_string(input_string):
    '''Split a string to a list and strip it
    :param input_string: A string that contains semicolons as separators.
    '''
    string_splitted = input_string.split(';')
    # Remove whitespace at the beginning and end of each string
    strings_striped = [string.strip() for string in string_splitted]
    return strings_striped

if __name__ in ['__builtin__','__main__']:
    # Run the batch_open_images() function using the Scripting Parameters.
    images = batch_open_images(originaldir,Nucleiroidir ,SpotSegdir,
                               split_string(file_type_image),
                             
                               split_string(filter_image),
                       
                               do_recursive
                              )

