#@ Dataset input_img
#@ OpService ops
#@ DatasetService ds
#@ DisplayService display
#@ File(label='Choose OriginalImage directory', style='directory') originaldir
#@ String(label='File types', value='TIF') file_type_image
#@ File(label='Choose SaveImage directory', style='directory') savedir

from net.imagej import Dataset
from fr.pasteur.iah.localzprojector.process import LocalZProjectionOp
from fr.pasteur.iah.localzprojector.process import ReferenceSurfaceParameters
from fr.pasteur.iah.localzprojector.process.ReferenceSurfaceParameters import Method
from fr.pasteur.iah.localzprojector.process import ExtractSurfaceParameters
from fr.pasteur.iah.localzprojector.process.ExtractSurfaceParameters import ProjectionMethod

#Macro to do local Z projection @Jean Yvez Tinnevez, Varun Kapoor, Cyrill Kana

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



def batch_open_images(pathImage, split_string(file_type_image)):

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

     Images = []
    
     for img_path, file_name in path_to_Image:
         imp = IJ.openImage(img_path)
         Images.append(imp)
        
    return Images       

if __name__ in ['__builtin__','__main__']:

     # Put the images to process in a list.
     images_to_process, file_names = batch_open_images(originaldir, file_typeImage)
     # Loop over each image.
     for img in images_to_process:

			# Execute local Z projection.
			local_proj = lzp_op.calculate( img )
		
			# Display results.
			local_proj_output = ds.create( local_proj )
			local_proj_output.setName( 'LocalProjOf_' + img.getName() )
			#display.createDisplay( local_proj_output )
            IJ.saveAs(local_proj_output, '.tif', str(savedir) + "/"  +  local_proj_output.getName());        
