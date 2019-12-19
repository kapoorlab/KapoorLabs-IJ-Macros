//manual segmentation helper

// Choose the save directory for ROI SET
TargetDir = getDirectory("Choose Destination Directory To Save RoiSet ");

//pour chaque tranche
for(slice=1;slice<=nSlices;slice++)
{
	if(slice==1)
	{
		run("Select None");
		setTool("freehand");	
		getDimensions(width, height, channels, slices, frames);
		raw=getTitle();
		newImage("mask_"+raw, "8-bit black", width, height, slices);
		selectWindow(raw);
		waitForUser("please draw the first ROI and click OK");
		selectWindow("mask_"+raw);
		setSlice(1);
		run("Restore Selection");
		setForegroundColor(255, 255, 255);
		run("Fill", "slice");
		selectWindow(raw);
		roiManager("Add");
		
	}
		
	else 
	{
		selectWindow(raw);
		setSlice(slice);
		size = 15;  
    	setTool("brush");
    	call("ij.gui.Toolbar.setBrushSize", size); 
		run("Restore Selection");
		waitForUser("["+slice+"] please adjust ROI with brush tool and click OK");
		selectWindow("mask_"+raw);
		setSlice(slice);
		run("Restore Selection");
		setForegroundColor(255, 255, 255);
		run("Fill", "slice");
		selectWindow(raw);
		roiManager("Add");
	}


}


        roiManager("Deselect");
        roiManager("Save", TargetDir+ raw + "RoiSet" + ".zip");
        print(TargetDir +replace(raw, ".tif","" ) + "RoiSet");
        waitForUser("DONE");