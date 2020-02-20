frames = 121;
Original = 'TestA.tif';
Division = 'ONETDivisionTestA.tif';
Apoptosis = 'ONETApoptosisTestA.tif';
NonMature = 'ONETNonMatureTestA.tif';
Mature = 'ONETMatureTestA.tif';
MacroKitty = 'ONETMacroKittyTestA.tif'; 

for (i = 1; i <= nImages; i++) {
    selectImage(i);
    run("8-bit");
    run("Properties...", "channels=1 slices=1 frames=frames unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000");
    
    
}

wait(1)
run("Merge Channels...", "c2=ONETDivisionTestA.tif c7=ONETApoptosisTestA.tif c6=ONETNonMatureTestA.tif c4=TestA.tif c3=ONETMatureTestA.tif c1=ONETMacroKittyTestA.tif create keep");
    run("RGB Color", "frames");
    selectWindow(MacroKitty);
    close();
    selectWindow(Division);
    close();
    selectWindow(Apoptosis);
    close();
    selectWindow(NonMature);
    close();
    selectWindow(Mature);
    close();