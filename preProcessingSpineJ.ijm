close("*");

//Open folders (first for the images you want to analyse, second to save the treshold images and the excel files with the results; you have to save this in a new ordner) 
dir1 = getDirectory("Choose your folder with your raw data (neuron + SYN + PSD-95).");
dir2 = getDirectory("Select a folder to save your analysis data");
list = getFileList(dir1);
print(list.length);

//set Measurement settings
run("Set Measurements...", "area centroid perimeter redirect=None decimal=3");

for (j=0; j<list.length; j++) {
	showProgress(j+1, list.length);
	if(list[j].matches('.*.zip') || list[j].matches('.*.tif') || list[j].matches('.*.czi')) {
		picture = list[j];
		open(""+dir1+picture+"");
	
	//get title for the image
		title = getTitle();

	//split channels 
		run("Split Channels");
		selectWindow ("C1-" + picture);
		rename("PSD");
		selectWindow ("C2-" + picture);
		rename("SYN");
		selectWindow ("C3-" + picture);
		rename("dendrite");
	
	//dendrite processing
	//copy
		selectWindow("dendrite");
		run("Duplicate...", "title=dendrite-1");
		
	//Gaussian Blur
		selectWindow("dendrite-1");
		run("Gaussian Blur...", "sigma=30");
	
	//Image calculator
		imageCalculator("Subtract create stack","dendrite", "dendrite-1");
		selectWindow("Result of dendrite");
		run("Enhance Contrast", "saturated=0.35");
	
	//save image
		selectWindow("Result of dendrite");
		//run("Smooth");
		saveAs("Tiff", dir2 + picture + "_spine");
		
	//Outlining of Holes and measuring of area
		selectWindow("SYN");
		setTool("freehand");
		waitForUser("Please mark the holes in your image, add them to your Roimanager and then press on ok.");
		
		if (roiManager("count") > 0) {
    // Loop through each ROI and clear the area outside it
	    for (r = 0; r < roiManager("count"); r++) {
	        roiManager("select", r);
	        run("Measure");
	    }
	    roiManager('select', "*");
		roiManager("Save", dir2 + title+ "holes_ROI.zip");
		selectWindow("Results");
		saveAs("Measurements", dir2 + title + "-holes.csv");
		run("Close");
		roiManager("reset");
		run("Select None");
		}
		
	//SYN processing
		selectWindow("SYN");
		run("Duplicate...", "title=SYN-1");
	
	//unsharp mask
		selectWindow("SYN");
		run("Unsharp Mask...", "radius=5 mask=0.60");
	
	//Gaussian Blur
		selectWindow("SYN-1");
		run("Gaussian Blur...", "sigma=30");
	
	//Image calculator
		imageCalculator("Subtract create stack","SYN", "SYN-1");
		selectWindow("Result of SYN");
	
	//Thresholding		
		selectWindow("Result of SYN");
		run("Enhance Contrast", "saturated=0.35");
		setAutoThreshold("Otsu dark");
		setOption("BlackBackground", false);
		run("Convert to Mask");
		run("Despeckle");
		run("Watershed");
	//Analyze particles
		run("Analyze Particles...", "size= 0.05-infinity show=Nothing add");
		
	//Measure particle size and count particles
		for (r = 0; r < roiManager("count"); r++) {
		        roiManager("select", r);
		        run("Measure");
		    }
	//Save
		selectWindow("Results");
		saveAs("Measurements", dir2 + title + "-SYN.csv");
		run("Close");
		selectWindow("Result of SYN");
		saveAs("PNG", dir2 + title + "-SYN_treshold.png");
		run("Close");
		roiManager('select', "*");
		roiManager("Save", dir2 + title+ "SYN_ROI.zip");
		
	//cleanup results and roimanager
		roiManager("reset");
		run("Close");
		
	//PSD processing
		selectWindow("PSD");
		run("Duplicate...", "title=PSD-1");
	
	//unsharp mask
		selectWindow("PSD");
		run("Unsharp Mask...", "radius=5 mask=0.60");
	
	//Gaussian Blur
		selectWindow("PSD-1");
		run("Gaussian Blur...", "sigma=30");
	
	//Image calculator
		imageCalculator("Subtract create stack","PSD", "PSD-1");
		selectWindow("Result of PSD");
		
	//Thresholding		
		selectWindow("Result of PSD");
		run("Enhance Contrast", "saturated=0.35");
		setAutoThreshold("Otsu dark");
		setOption("BlackBackground", false);
		run("Convert to Mask");
		run("Despeckle");
		run("Watershed");
	//Analyze particles
		run("Analyze Particles...", "size= 0.05-infinity show=Nothing add");
		
	//Measure particle size and count particles
		for (r = 0; r < roiManager("count"); r++) {
		        roiManager("select", r);
		        run("Measure");
		    }
	//Save
		selectWindow("Results");
		saveAs("Measurements", dir2 + title + "-PSD.csv");
		run("Close");
		selectWindow("Result of PSD");
		saveAs("PNG", dir2 + title + "-PSD_treshold.png");
		run("Close");
		roiManager('select', "*");
		roiManager("Save", dir2 + title+ "PSD_ROI.zip");
		
	//cleanup results and roimanager
		roiManager("reset");
		run("Close");
		

//Clean-up to prepare for next image
	run("Close All");
	close("*");

	if (isOpen("Log")) {
	     selectWindow("Log");
	     run("Close");
	}
	if (isOpen("Summary")) {
	     selectWindow("Summary");
	     run("Close");
	}
	if (isOpen("Results")) {
	     selectWindow("Results");
	     run("Results");
	}
	
  }
}
print("Jeah, finished!");

		


