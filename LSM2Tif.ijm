SourceDir = getDirectory("Choose LSM Source Directory ");

TargetDir = getDirectory("Choose Tif Destination Directory ");

list = getFileList(SourceDir);

//Convert LSM images to TIF files

for(i = 0; i < list.length; i++) {

     showProgress(i+1, list.length);

     if(filter(i, list[i])) {
     title = SourceDir + list[i];
     open(title);
     
   
     saveAs('.tiff', TargetDir + list[i]);
     
     close();

     }
	
}

function filter(i, name) {

    // is lsm?
    if (!endsWith(name,".lsm")) return false;

  

    return true;
}