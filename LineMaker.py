#@ File(label='Choose OriginalImage directory', style='directory') originaldir
#@ String(label='File types', value='tif') file_type_image
#@ File(label='Choose SaveImage directory', style='directory') savedir
#@ String(label='Filter', value='._') filter_image
#@ OpService ops
#@ DatasetService ds
#@ DisplayService display
from ij import IJ
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imglib2.view import Views
from net.imglib2.converter import Converters
from net.imglib2.algorithm.dog import DogDetection
from net.imglib2.type.numeric.real import DoubleType
from jarray import zeros  
from java.awt import Color
from ij.gui import PointRoi, OvalRoi , Overlay, Line 
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, Toolbar
from net.imglib2.view import Views
from ij.gui import GenericDialog
from java.io import File
from net.imagej.axis import Axes
from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi.labeling import LabelRegions

from net.imglib2.roi import Regions
from net.imglib2.algorithm.neighborhood import HyperSphereShape
from net.imagej.axis import CalibratedAxis
from net.imglib2.view import Views
import os

from net.imagej.axis import Axes
from net.imagej import ImgPlus

def split_string(input_string):
    '''Split a string to a list and strip it
    :param input_string: A string that contains semicolons as separators.
    '''
    string_splitted = input_string.split(';')
    # Remove whitespace at the beginning and end of each string
    strings_striped = [string.strip() for string in string_splitted]
    return strings_striped
def batch_open_images(pathImage,file_typeImage, name_filterImage=None ):

     if isinstance(pathImage, File):
        pathImage = pathImage.getAbsolutePath()

        
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
     # We collect all files to open in a list.
     path_to_Image = []
     # Replacing some abbreviations (e.g. $HOME on Linux).
     path = os.path.expanduser(pathImage)
     path = os.path.expandvars(pathImage)
     # If we don't want a recursive search, we can use os.listdir().
     
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
     Images = []
     
     for img_path, file_name in path_to_Image:

            imp =  IJ.openImage(img_path)
            maskimage = ops.run("create.img", imp)
            cursor = maskimage.localizingCursor()
            imp.show()
            IJ.run("Select None")
            overlay = imp.getOverlay()
            if overlay == None:

                overlay = Overlay()
                imp.setOverlay(overlay)
            else:
            
               overlay.clear();

            imp.updateAndDraw()
            impY = imp.getHeight()
            impX = imp.getWidth()
            print(impY, impX)
            rm = RoiManager.getInstance()
            if not rm:
                rm = RoiManager()

            rm.runCommand("reset")
            WaitForUserDialog("Select the landmark and the second point").show();
            rm.runCommand("Add");
            roi_points = rm.getRoisAsArray()
            for Roi in roi_points:
                    
                    xpoints = Roi.getPolygon().xpoints
                    ypoints = Roi.getPolygon().ypoints
                    print(xpoints, ypoints)

            print('Start Landmark', xpoints[0], ypoints[0])
            fixedpointX = xpoints[0]
            fixedpointY = ypoints[0]
            print('End Landmark', xpoints[1], ypoints[1])
            IJ.makeLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1])
            gui = GenericDialog("Rotation Angle")
            gui.addNumericField("Choose Angle", 15, 0)
            gui.showDialog();
            if gui.wasOKed():
                
                rotateangle = gui.getNextNumber()
                IJ.run("Rotate...", "angle="+str(int(float(rotateangle))));

            rm.runCommand("reset")
            overlay = imp.getOverlay()
            rm.runCommand("Add")
            roi_points = rm.getRoisAsArray()
            
            for Roi in roi_points:
                     xpoints = Roi.getPolygon().xpoints
                     ypoints = Roi.getPolygon().ypoints
                     print(xpoints, ypoints)
            
            print('Rotated Start Landmark',xpoints[0], ypoints[0])
            print('Rotated End Landmark',xpoints[1], ypoints[1])
            slope = (ypoints[1] - ypoints[0])/ (xpoints[1] - xpoints[0] + 1.0E-20)
            intercept = fixedpointY - slope * fixedpointX
            print(fixedpointX, fixedpointY)
            print('Slope', slope, 'Intercept', intercept)
            XwY0 = -intercept/slope
            YxwY0 = slope * XwY0 + intercept

            XwYmax = (impY -intercept)/slope
            YxwYmax = slope * XwYmax + intercept

            YwX0 = intercept
            XywX0 = (YwX0 - intercept)/slope
            YwXmax = impX * slope + intercept
            XxwXmax = (YwXmax - intercept)/slope
            rm.runCommand("reset")
            
            if XwY0 > 0:
                    lineROIA = Line(fixedpointX, fixedpointY,XwY0, YxwY0)
                    lineROIB = Line(fixedpointX, fixedpointY,XwYmax, YxwYmax)
                    overlay.add(lineROIA)
                    
                    overlay.add(lineROIB)
                    
                    
                         
                    
                     
            if XwY0 < 0:
                    lineROIA = Line(fixedpointX, fixedpointY,XywX0, YwX0)
                    lineROIB = Line(fixedpointX, fixedpointY,XxwXmax, YwXmax)
                    overlay.add(lineROIA)
                    
                    overlay.add(lineROIB)

            while cursor.hasNext():
                            cursor.fwd()
                            X = cursor.getDoublePosition(0)
                            Y = cursor.getDoublePosition(1)
                            if abs(Y - slope * X - intercept) <= 4:
                                   cursor.get().set(0)
                            else:
                                   cursor.get().set(1)       
            labeling=ops.labeling().cca(maskimage, StructuringElement.EIGHT_CONNECTED)

            # get the index image (each object will have a unique gray level)
            labelingIndex=labeling.getIndexImg()

            # get the collection of regions and loop through them
            regions=LabelRegions(labeling)
            for region in regions:
                # get the size of the region
                size=region.size()

                

                print "size",size   

            display.createDisplay( labelingIndex )
            
            
            
            WaitForUserDialog("hold").show();

            
            
if __name__ in ['__builtin__','__main__']:             
      
       batch_open_images(originaldir,split_string(file_type_image), split_string(filter_image) )