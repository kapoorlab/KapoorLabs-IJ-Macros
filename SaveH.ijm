SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);

N_Classes = 3

// Takes HDF5 file from Ilastik project and saves C2 class as tif file, change C2 in selectWindow to C1 to save that class instead and so on
for(i = 0; i < list.length; i++) {

     showProgress(i+1, list.length);
     title = SourceDir + list[i];
     run("Load HDF5 File...", "open=" + title);
     waitForUser('Click Ok after making HDF5 selections');
     run("Split Channels"); 
     AppendSaveName = 'Cloud'; 
     selectWindow("C3-"+title + ": /exported_data"); 
     saveAs('.tiff', TargetDir+ AppendSaveName  + list[i]);
     for(j = 0; j < N_Classes; j++)
     close();
  
}