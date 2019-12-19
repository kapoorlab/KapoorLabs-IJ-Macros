frames = 180;
Original = 'Movie2.tif';
Division = 'DivisionMovie2.tif';
Apoptosis = 'ApoptosisMovie2.tif';
NonMature = 'NonMatureP1Movie2.tif';
Mature = 'MatureP1Movie2.tif';
MacroKitty = 'MacroKittyMovie2.tif'; 


for (i = 1; i <= nImages; i++) {
    selectImage(i);
    run("8-bit");
    run("Properties...", "channels=1 slices=1 frames=frames unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000");
    
    
}
wait(1)
run("Merge Channels...", "c7=DivisionMovie2.tif c2=ApoptosisMovie2.tif c3=NonMatureP1Movie2.tif c4=Movie2.tif c6=MatureP1Movie2.tif c1=MacroKittyMovie2.tif create keep");
    
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