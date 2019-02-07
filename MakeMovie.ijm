SourceDir = getDirectory("Choose Source Directory ");

TargetDir = getDirectory("Choose Destination Directory ");

list = getFileList(SourceDir);

// Takes a directory containing sub-directories with seperate images, loads them in sorted order and saves them as ImageStacks in destination directory
for(i = 0; i < list.length; i++) {



     showProgress(i+1, list.length);
     subdir = SourceDir + list[i];
     run("Image Sequence...", "open=subdir sort");
     title = getTitle();
     saveAs('.tiff', TargetDir + title);
     close();

	
}
