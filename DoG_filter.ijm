
// Prompt to get sigma values for the Difference of Gaussians filtering
Dialog.create("Choose filter sizes for DoG filtering");
Dialog.addNumber("Gaussian sigma 1", 1);
Dialog.addNumber("Gaussian sigma 2", 2);
Dialog.show();
sigma1 = Dialog.getNumber();
sigma2 = Dialog.getNumber();

// Get the current image
idOrig = getImageID();

// Convert to 32-bit (so we can have negative values)
run("32-bit");

// Duplicate the image, and request the ID of the duplicate
run("Duplicate...", "title=[My duplicated image]");

// Smooth the original & duplicated images
idDuplicate = getImageID();
run("Gaussian Blur...", "sigma="+sigma1);
selectImage(idOrig);
run("Gaussian Blur...", "sigma="+sigma2);

// Subtract one smoothed image from the other
imageCalculator("Subtract create", idDuplicate, idOrig);
