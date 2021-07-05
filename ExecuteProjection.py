
#@ OpService ops
#@ DatasetIOService dio
#@ LocationService ls
#@ ConvertService convertService
#@ DatasetService ds
#@ DisplayService display
#@ File(label='Choose OriginalImage directory', style='directory') originaldir
#@ String(label='File types', value='tif') file_type_image
#@ File(label='Choose SaveImage directory', style='directory') savedir
#@ String(label='Filter', value='._') filter_image
from net.imagej import Dataset
from fr.pasteur.iah.localzprojector.process import LocalZProjectionOp
from fr.pasteur.iah.localzprojector.process import ReferenceSurfaceParameters
from fr.pasteur.iah.localzprojector.process.ReferenceSurfaceParameters import Method
from fr.pasteur.iah.localzprojector.process import ExtractSurfaceParameters
from fr.pasteur.iah.localzprojector.process.ExtractSurfaceParameters import ProjectionMethod
from java.io import File
import os
from net.imagej import ImgPlus
from  net.imglib2.img import ImagePlusAdapter
from net.imagej.axis import Axes
from ij import IJ;
import ij.ImagePlus;
import net.imagej.Dataset;
import net.imagej.ImageJ;
from net.imglib2.img.display.imagej import ImageJFunctions;
#Macro to do local Z projection @Jean Yvez Tinnevez, Varun Kapoor, Cyrill Kana




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

         image =  IJ.openImage(img_path)
        
         dataset = ds.create(ImageJFunctions.convertFloat(image))
         axes = [Axes.X, Axes.Y, Axes.Z, Axes.TIME, Axes.CHANNEL]
         dataImg = ds.create(ImgPlus(dataset.getImgPlus().copy(), file_name, axes))
         
         Images.append(dataImg)
        
     return Images       

if __name__ in ['__builtin__','__main__']:
     #------------------
	 # Parameters.
	 #------------------
	
	
	 # What channel to use to create the reference surface?
	 channel = 0
	
	 # Reference surface parameters.
	 #params_ref_surface = ReferenceSurfaceParameters.deserialize( param_file_1 )
	 params_ref_surface = ReferenceSurfaceParameters.create() \
					.method( Method.MAX_OF_STD ) \
					.zMin( 0 ) \
					.zMax( 100000 ) \
					.filterWindowSize( 21 ) \
					.binning( 4 ) \
					.gaussianPreFilter( 0.1 ) \
					.medianPostFilterHalfSize( 20 ) \
					.targetChannel( channel ) \
					.get()
	
	 # Local projection parameters.
	 params_proj = ExtractSurfaceParameters.create() \
      					.zOffset( 0, 0 ) \
					.zOffset( 1, +8 ) \
					.deltaZ( 0, 3 ) \
					.deltaZ( 1, 3 ) \
					.projectionMethod( 0, ProjectionMethod.MIP ) \
					.projectionMethod( 1, ProjectionMethod.MIP ) \
					.get()
	
	
	
	 #------------------
	 # Execute.
	 #------------------
	
	 # Create op, specifying only input type and the two parameters.
	 lzp_op = ops.op( LocalZProjectionOp, Dataset, params_ref_surface, params_proj )
	 images_to_process = batch_open_images(originaldir,split_string(file_type_image), split_string(filter_image) )
	 print('Images to project',len(images_to_process))
	 for img in images_to_process:
            
            local_proj = lzp_op.calculate( img )
            local_proj_output = ds.create( local_proj )
            
            location = ls.resolve(str(savedir) + '/' +  img.getName() + '.tif')
            dio.save(local_proj_output, location)
                    
