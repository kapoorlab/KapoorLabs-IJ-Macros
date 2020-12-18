#@ File(label='Choose OriginalImage directory', style='directory') originaldir
#@ String(label='File types', value='tif') file_type_image
#@ String(label='Filter', value='._') filter_image
#@ Boolean(label='Recursive search', value=True) do_recursive
#@ File(label='Choose Mask directory', style='directory') maskdir

import os
from java.io import File

from ij import IJ
from ij.plugin.frame import RoiManager
from ij.plugin import StackCombiner, RGBStackMerge
from ij import WindowManager as wm

def batch_open_images(pathImage, pathMask, file_typeImage=None,  name_filterImage=None,  recursive=False):
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
    Masks = []
    for img_path, file_name in path_to_Image:
        # IJ.openImage() returns an ImagePlus object or None.
        imp = IJ.openImage(img_path)
        imp.show()
        IJ.run("8-bit")
        print(img_path)
        if check_filter(file_name):
         continue;
        else: 
         # An object equals True and None equals False.
         
         MaskName = str(pathMask) + '/'+  "Mask"  + file_name + '.tif'
         Mask = IJ.openImage(MaskName)
         Mask.show()
         IJ.run("8-bit")
         IJ.run("Find Edges")
         IJ.selectWindow(file_name + ".tif");
         IJ.selectWindow("Mask" + file_name  + ".tif" );
         Mask.changes = False;
         imp.changes = False;

         impResult = RGBStackMerge.mergeChannels([imp, Mask], False)
         impResult.show()
         IJ.saveAs(impResult, '.tif', str(pathMask) + "/"  +  file_name);
         imp.close()
         Mask.close()
         
         #print(img_path, RoiName)
         Images.append(imp)
    return Images

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
    images = batch_open_images(originaldir ,maskdir,
                               split_string(file_type_image),
                             
                               split_string(filter_image),
                       
                               do_recursive
                              )
    for image in images:
        # Call the toString() method of each ImagePlus object.
        print(image)
