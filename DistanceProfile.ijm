
imageTitle = newArray(nImages);
for(i = 1; i<=nImages;i++)

{

                selectImage(i);

                imageTitle[i-1] = getTitle();

}
Dialog.create("Distance recorder");
Dialog.addNumber("Pixel Size", 1);
Dialog.addChoice("image to select", imageTitle, imageTitle[0]);

Dialog.show();
TargetDir = getDirectory("Choose Destination Directory ");
Xcalibration = Dialog.getNumber();
choice = Dialog.getChoice()

    selectWindow(choice);
   
    title = getTitle();
    height = getHeight();
    width = getWidth();
    
    Values = newArray(height);
    Xvalues = newArray(width);
    Yvalues = newArray(width);
    Titre="[Distance_Over_Time]";

run("New... ", "name="+Titre+" type=Table");

print(Titre, "[Time\tDistance]");
    
    for(i = 0; i < width; i++){
        for(j = 0; j < height; j++){
        	
                Values[j] = getPixel(i, j);
                bottom = findBottomPeak(Values);
                top = findTopPeak(Values);
                dist = distance(top,bottom,Xcalibration);
                if(dist > 0){
                Xvalues[i] = i;
                Yvalues[i] = dist;
                Rez = ""+Xvalues[i]+"\t"+ Yvalues[i] ;
                print(Titre, Rez) ;
                }
        }
    }
 

                selectWindow("Distance_Over_Time");

   saveAs("Text", TargetDir+File.separator+ choice + ".csv");


   
  Plot.create("Distance over time", "T-location", "Distance", Xvalues, Yvalues);
  Plot.show();

   
 
    


function findBottomPeak(array) {
	for (i = array.length - 1; i >= 0; i--)
		if (array[i] > 0)
			return i;
	return -1;
}

function findTopPeak(array) {
	for (i = 0; i < array.length; i++)
		if (array[i] > 0)
			return i;
	return -1;
}

function distance( ystart, yend, Calibration) {

return abs(yend - ystart) * Calibration;

}


