
SourceDir = getDirectory("Choose Tif Source Directory ");

TargetDir = getDirectory("Choose split Tif Destination Directory ");

list = getFileList(SourceDir);
print(list.length)
for(i = 0; i < list.length; i++) {

     showProgress(i+1, list.length);

     if(filter(i, list[i])) {
     title = SourceDir + list[i];
     open(title);
     run("Stack to Images");
   
     n = nImages();
print(n);     
for (j = 0; j < n; ++j){
 saveAs('.tiff', TargetDir +  list[i]  + j);
close();	
}
     }
	
}



function filter(i, name) {

    // is tif?
    if (!endsWith(name,".tif")) return false;

  

    return true;
}