
Dialog.create("Distance recorder");
Dialog.addNumber("Pixel Size", 1);



Dialog.show();
Xcalibration = Dialog.getNumber();



for (i = 1; i <= nImages; i++) {
    selectImage(i);
    title = getTitle();
    height = getHeight();
    width = getWidth();
    
    Values = newArray(height);
    Xvalues = newArray(width);
    Yvalues = newArray(width);

    for(i = 0; i < width; i++){
        for(j = 0; j < height; j++){
        	
                Values[j] = getPixel(i, j);
                bottom = findBottomPeak(Values);
                top = findTopPeak(Values);
                dist = distance(top,bottom,Xcalibration);
                if(dist > 0){
                Xvalues[i] = i;
                Yvalues[i] = dist;
                }
        }
    }
    
  Plot.create("Distance over time", "T-location", "Distance", Xvalues, Yvalues);
 Plot.show();

   
 
    
}

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


