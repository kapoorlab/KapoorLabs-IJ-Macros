SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);


for(i = 0; i < list.length; i++) {

	showProgress(i+1, list.length);
	
     if(endsWith(list[i], ".png"))
     
     {

     title = SourceDir + list[i];
     open(title);

     run("RGB Color");
     run("RGB to Luminance");
     saveAs('.tiff', TargetDir+ list[i]);
     close(title);
                   
     }

 close();



}