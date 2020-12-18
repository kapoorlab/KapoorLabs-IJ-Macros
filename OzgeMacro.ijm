
SourceDir = getDirectory("Choose Tif Source Directory ");

TargetDir = getDirectory("Choose split Tif Destination Directory ");

list = getFileList(SourceDir);

for(i = 0; i < list.length; i++) {

showProgress(i+1, list.length);
title = SourceDir + list[i];
open(title);
selectWindow(list[i]);

setOption("BlackBackground", false);
run("Make Binary");

saveAs("tiff",TargetDir+list[i]);
close();

}