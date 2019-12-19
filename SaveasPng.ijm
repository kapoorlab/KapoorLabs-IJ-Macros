SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);

//Save asPng

for(i = 0; i < list.length; i++) {

     title = SourceDir + list[i];


     open(title);
     if(endsWith(title, ".tif")){
     saveAs('.png', TargetDir + list[i]);
     close();
     }
	
}