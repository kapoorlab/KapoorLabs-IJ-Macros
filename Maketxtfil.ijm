SourceDir = getDirectory("Choose Source Directory ");



list = getFileList(SourceDir);



file = File.open("LocalizationRotatedBoring" + '.txt');
for(i = 0; i < list.length; i++) {

     showProgress(i+1, list.length);
  
     title = SourceDir + list[i];

   open(title);
   
 
if(endsWith(list[i], ".tif")){
     
     
     print(file, list[i] + "  , " + 5 + " ,"  + getHeight()/ 2 + ", " + getWidth()/ 2);
    
     
     close();
     
};
File.close(file);
	
}
