for (i = 1; i <= nImages; i++) {
    selectImage(i);
    run("8-bit");
    run("Properties...", "channels=1 slices=1 frames=180 unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000");
    
    
}
wait(1)
run("Merge Channels...", "c1=DivisionSmallPatch.tif c2=ApoptosisSmallPatch.tif c3=NonMatureP1SmallPatch.tif c4=SmallPatch.tif c5=MatureP1SmallPatch.tif c7=MacroKittySmallPatch.tif create keep");
    
    run("RGB Color", "frames");
    selectWindow("MacroKittySmallPatch.tif");
    close();
    selectWindow("DivisionSmallPatch.tif");
    close();
    selectWindow("ApoptosisSmallPatch.tif");
    close();
    selectWindow("NonMatureP1SmallPatch.tif");
    close();
    selectWindow("MatureP1SmallPatch.tif");
    close();