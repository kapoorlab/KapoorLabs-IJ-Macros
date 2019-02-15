SourceDir = getDirectory("Choose Source Directory ");



list = getFileList(SourceDir);



for(i = 0; i < list.length; i++) {

     showProgress(i+1, list.length);
  
     title = SourceDir + list[i];

   open(title);
   
 
if(endsWith(list[i], ".tif")){
     savename = replace(title,".tif",""); 
     file = File.open(savename + '.txt');
     print(file, "Filename" + "  \t " + "Time" + "  \t"  + "X" + " " + "Y");
     print(file, list[i] + "  \t " + 3 + "  \t"  + getHeight()/ 2 + " " + getWidth()/ 2);
    
     
     close();
     File.close(file);
};
	
}
