SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);

//Convert image to 16 bit

for(i = 0; i < list.length; i++) {

     title = SourceDir + list[i];

     open(title);
     run("16-bit"); 
     close();
     
	
}
