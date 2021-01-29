#@ File(label='Choose Roi directory', style='directory') roidir

#@ String(label='File types', value='zip') file_type_Roi
#@ String(label='Filter', value='._') filter_Roi
#@ Boolean(label='Recursive search', value=False) do_recursive


import os
from java.io import File
from ij.measure import ResultsTable
from ij import IJ
from ij.plugin.frame import RoiManager
from ij import WindowManager as wm

def batch_open_Rois(pathRoi, file_typeRoi=None,  name_filterRoi=None,  recursive=False):
    '''Open all files in the given folder.
    :param path: The path from were to open the Rois. String and java.io.File are allowed.
    :param file_type: Only accept files with the given extension (default: None).
    :param name_filter: Reject files that contain the given string (default: wild characters).
    :param recursive: Process directories recursively (default: False).
    '''
    # Converting a File object to a string.
    if isinstance(pathRoi, File):
        pathRoi = pathRoi.getAbsolutePath()
    
    def check_type(string):
        '''This function is used to check the file type.
        It is possible to use a single string or a list/tuple of strings as filter.
        This function can access the variables of the surrounding function.
        :param string: The filename to perform the check on.
        '''
        if file_typeRoi:
            # The first branch is used if file_type is a list or a tuple.
            if isinstance(file_typeRoi, (list, tuple)):
                for file_type_ in file_typeRoi:
                    if string.endswith(file_type_):
                        # Exit the function with True.
                        return True
                    else:
                        # Next iteration of the for loop.
                        continue
            # The second branch is used if file_type is a string.
            elif isinstance(file_typeRoi, string):
                if string.endswith(file_typeRoi):
                    return True
                else:
                    return False
            return False
        # Accept all files if file_type is None.
        else:
            return True




   

    # We collect all files to open in a list.
    path_to_Roi = []
    # Replacing some abbreviations (e.g. $HOME on Linux).
    path = os.path.expanduser(pathRoi)
    # If we don't want a recursive search, we can use os.listdir().
    if not recursive:
        for file_name in os.listdir(pathRoi):
            full_path = os.path.join(pathRoi, file_name)
            if os.path.isfile(full_path):
                if check_type(file_name):
                    path_to_Roi.append(full_path)
    # For a recursive search os.walk() is used.
    else:
        # os.walk() is iterable.
        # Each iteration of the for loop processes a different directory.
        # the first return value represents the current directory.
        # The second return value is a list of included directories.
        # The third return value is a list of included files.
        for directory, dir_names, file_names in os.walk(pathRoi):
            # We are only interested in files.
            for file_name in file_names:
                # The list contains only the file names.
                # The full path needs to be reconstructed.
                full_path = os.path.join(directory, file_name)
                # Both checks are performed to filter the files.
                if check_type(file_name):
                        # Add the file to the list of Rois to open.
                        path_to_Roi.append([full_path, os.path.basename(os.path.splitext(full_path)[0])])
                        
    # Create the list that will be returned by this function.
    RoisX = []
    RoisY = []
    print('path',path_to_Roi)
    for roi_path in path_to_Roi:
                
		        print('path',roi_path)
		        # An object equals True and None equals False.
		        rm = RoiManager.getInstance()
		        if (rm==None):
		            rm = RoiManager()
		        Roi = IJ.open(roi_path)
		        roi_points = rm.getRoisAsArray()
		           
    table = ResultsTable()
    
    for Roi in roi_points:
        
        xpoints = Roi.getPolygon().xpoints
        ypoints = Roi.getPolygon().ypoints
    for i in range(len(xpoints)):    
            table.incrementCounter()
            table.addValue("Index", i)
            table.addValue("X", xpoints[i])
            table.addValue("Y", ypoints[i])
    table.show("XY-Coordinates")	
    
    
    return roi_points

def split_string(input_string):
    '''Split a string to a list and strip it
    :param input_string: A string that contains semicolons as separators.
    '''
    string_splitted = input_string.split(';')
    # Remove whitespace at the beginning and end of each string
    strings_striped = [string.strip() for string in string_splitted]
    return strings_striped

if __name__ in ['__builtin__','__main__']:
    # Run the batch_open_Rois() function using the Scripting Parameters.
    Rois = batch_open_Rois(roidir ,
                               split_string(file_type_Roi),
                             
                               split_string(filter_Roi),
                       
                               do_recursive
                              )
    

