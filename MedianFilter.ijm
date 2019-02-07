SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);

//Applys Median FIlter to a stack of images in chosen directory and saves them in target directory, appeands an additional String called
//AppendSaveName before saving the stack

for(i = 0; i < list.length; i++) {

  showProgress(i+1, list.length);
     title = SourceDir + list[i];

     open(title);
     
     AppendSaveName = 'MedianFilterR5'
     run("Median...", "radius=5 stack");
   
     saveAs('.tiff', TargetDir+ AppendSaveName + list[i]);

     close();
	
}
