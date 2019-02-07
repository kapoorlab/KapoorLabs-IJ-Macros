SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);

//Rotate images by 15 degrees till 360 degrees and save them

for(i = 0; i < list.length; i++) {

  showProgress(i+1, list.length);
     title = SourceDir + list[i];

     open(title);
     
    
     
     for (j = 1; j < 24; j++) {
     	 AppendSaveName = 'Original' + 'Rotation' + j * 15;
     run("Rotate... ", "angle=15 * j grid=1 interpolation=None stack" );
   
     saveAs('.tiff', TargetDir+ AppendSaveName + list[i]);

     }
     close();
     
	
}
