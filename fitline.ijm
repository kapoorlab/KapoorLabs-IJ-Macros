// Calculate average fit parameters for each line profile along x for an image.
// Fit equation is: y = a + bx (Straight Line)

getDimensions(width, height, channels, slices, frames);

a = newArray(height);
b = newArray(height);
x = Array.getSequence(width);

for (i = 0; i < height; i++) {
	makeLine(0, i, width, i);
	profile = getProfile();
	Fit.doFit("Straight Line", x, profile);
	a[i] = Fit.p(0);
	b[i] = Fit.p(1);
	print('a',a[i]);
	print('b',b[i]);
}
run("Select None");

Array.getStatistics(a, min_a, max_a, mean_a, stdDev_a);
Array.getStatistics(b, min_b, max_b, mean_b, stdDev_b);

print("Average parameters for y = a + bx");
print("a:", mean_a, "SD:", stdDev_a);
print("b:", mean_b, "SD:", stdDev_b);