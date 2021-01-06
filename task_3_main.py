#-----------------------------------------------------------------------------
#PHY3054
#Assignment 1
#Student: 6463360
#Task 3
#---Programme Description-----------------------------------------------------
#This programme reads in dark, flat and sky fits files from the 
#Yale La Silla-QUEST Kuiper Belt survey, provided by Professor Marla Geha at 
#Yale University, as part of the Yale Astronomy research techniques course.

#The flats and sky fits are bias corrected and dark subtracted.
#The images have been examined in DS9 to determine the overcan region.
#The sky fits are then flattened, sky subtracted and shifted into a common
#plane.

#The outputs of the programme are;
#the normalised flat fits file,
#science (sky images) corrected fits files,
#the second and third science images shifted,
#And finally the combined science fits file.
#-----------------------------------------------------------------------------


#---Import useful libraries---
import os #This is used to create directories and ensure the programme works
          #with all directory conventions.
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.stats import mode
from scipy.ndimage import interpolation


#---Bias Correction Function---
def bias_cor(X):
    biasPerRow = np.zeros(2400) #BiasPerRow of the overscan region.
    for j in range(2400):
        biasPerRow[j] = np.median(X[j, 600:640], axis=0)
    cor = X[:, :600] #Trim overscan off data.
    for j in range(2400):
        cor[j, :] = X[j, :600] - biasPerRow[j] #Correct each rows.
    return cor


#---Create base directory---
#The directory to the QUEST data is defined here for neatness throughout.
QUEST = os.path.join(os.getcwd(), "QUESTdata")


#---Darks---------------------------------------------------------------------
#The dark data is already bias corrected. Here it simply needs to be read in.
dark_dir = os.path.join(QUEST, "darks") #Define the directory.
dark_files = [10, 180] #File names to distinguish between the exposure times.
darkD = [] #Packaging the dark data together to be used later.
darkH = []
for i in dark_files:
    darkFile = fits.open(os.path.join(dark_dir, "dark_%i.C22.fits" %i), \
                         output_verify='ignore')
    darkData = darkFile[0].data
    darkHeader = darkFile[0].header
    dark_resized = darkData[:, :600] #Make the same size as the biar corrected
                                    #images later.
    darkD.append(dark_resized)
    darkH.append(darkHeader)
    #Close files now we're done with them.
    darkFile.close() #Prevent the file being stuck in memory.

print("") #Adds some space to the terminal output for neatness.


#---Flats---------------------------------------------------------------------
#The flats fits files need to be read in, bias corrected and dark subtracted.
flats_dir = os.path.join(QUEST, "flats") #Define the directory.
#A list of filenames is read in to give values to the fits.open file path in
#the fore loop.
flats_files = np.loadtxt(os.path.join(flats_dir, "flat.list"), \
                         usecols=(0,), delimiter='.', dtype=str)
flatsD = [] #Need the flat data later. This will populate with the flats.fits.
for i in flats_files:
    flatsFile = fits.open(os.path.join(flats_dir, "%s.C22.fits" %i), \
                          output_verify='ignore')
    flatsData = flatsFile[0].data
    flatsHeader = flatsFile[0].header
    #---Do the bias correction---
    flatsCor = bias_cor(flatsData)
    #---subtract Dark---
    flatsCor -= darkD[0] #Subtract the dark_10 data from the flats.
    #---Append to all sci list---
    flatsD.append(flatsCor) #Append to list for use later.
    #Close files now we're done with them.
    flatsFile.close() #Prevent the file getting stuck in memory.

#Check exposure time for flats to match with correct dark file.
#Print to user.
print("Exposure time of", flatsHeader['IMAGETYP'], "files =", \
      '%.0f' %flatsHeader['EXPTIME'], "s")
print("Exposure time of dark_10 file =", '%.0f' %darkH[0]['EXPTIME'], "s")
print("The dark_10 fits file is for the flats files.")


#---Create master flat and normalise---
mflat = np.median(np.array(flatsD), axis=0) #Make master flat array from all
                                              #flat data.
nflat = mflat / np.median(mflat.flatten()) #Normalising the flat.
#Adding a header to the master flat file.
hdu = fits.PrimaryHDU(nflat)
hdu.header.add_comment("Normalised median of flat fieldexposures")
#Write the master-normalised flat to a fits.
fits.writeto("normalised_flats.fits", hdu.data, hdu.header, \
             output_verify='ignore', overwrite=True)


#---Plot the pixel values as a histogram---
#To check the values of the flats we check the value of the normalised flat.
#We see from the histogram that the average values of a picel is 1.0.
plt.hist(nflat.flatten(), bins=300, range=(0.5, 1.5))
plt.title("Normalised Flat File Plotted - Shows Average Flat Pixel Value", \
          fontweight='bold')
plt.xlabel("Pixel Value", fontweight='bold')
plt.ylabel("Frequency", fontweight='bold')
plt.xlim(0.925, 1.075)
plt.show()
print("The average pixel value is around 1.00.")
print("") #Adds some space to the terminal output for neatness.


#---Science-------------------------------------------------------------------
#The science fits need the same treatment as the flats.
#Define paths to files.
sci_dir = os.path.join(QUEST, "science") #Define the directory.
sci_files = [20130910234901, 20130911020246, 20130911040543]
#Create 'all' lists for science data and headers for later use.
sciD = []
sciH = []
#Loop through every science file, appending to 'all' list each time.
for i in sci_files:
    sciFile = fits.open(os.path.join(sci_dir, "%ss.C22.fits" %i), \
                        output_verify='ignore')
    sciData = sciFile[0].data.astype(np.float64) #Float matches other data.
    sciHeader = sciFile[0].header
    #---Do the bias correction---
    sciCor = bias_cor(sciData)    
    #---subtract Dark---
    sciCor -= darkD[-1] #Subtract the dark_180 data from the flats.
    #---Append to all sci list---
    sciD.append(sciCor) #Append to lists for use later.
    sciH.append(sciHeader)
    sciFile.close() #Prevent the file getting stuck in memory.

#Check exposure time for flats to match with correct dark file.
#Print to user.
print("Exposure time of", sciHeader['IMAGETYP'], "files =", \
      '%.0f' %sciHeader['EXPTIME'], "s")
print("Exposure time of dark_180 file =", '%.0f' %darkH[-1]['EXPTIME'], "s")
print("The dark_180 fits file is for the science files.")
print("") #Adds some space to the terminal output for neatness.


#---Flatten science data---
#The science data is flattened by dividing by the master-normalised flat.
sciFlat = sciD / nflat


#---Sky correction------------------------------------------------------------
#The average value of the sky images will be calculated and subtracted from
#the science data.
#Get min and max values of pixel intensity.
minp = min(sciFlat.flatten())
maxp = max(sciFlat.flatten())

sciSky = []
print("The sky correction may take up to an hour. Please wait.")
for i in range(3):
    print("") #Adds some space to the terminal output for neatness.
    #Get the mode x-value using scipy.stats.mode
    print("Calculating mode value...")
    skyval, loc = mode(sciFlat[i].flatten())
    skySub = sciFlat[i] - skyval #Subtract the average sky value.
    sciSky.append(skySub)

print("") #Adds some space to the terminal output for neatness.

#Save all reduced images.
for i in range(3):
    j = sci_files[i]
    fits.writeto("science_corrected_%ss.fits" %j, sciSky[i], \
                     sciH[i], output_verify='ignore', overwrite=True)
    print("The fully corrected science file - science_corrected_%ss.fits" \
          %j, "has been saved.")    

print("") #Adds some space to the terminal output for neatness.


#---Shift and Combine Images--------------------------------------------------
#Shifts the second and third science images into the same frame as the first.
#The positions of several stars were noted between all frames and the changes
#in their positions were noted. This is used to reverse the shift affect.
#Values of the shift for the second and third image respectively are below.
shiftV = [(16.5, -3.75), (39.5, -6.25)]
j = 0 #Initialising for inside the loop.
for i in sci_files:
    if i == sci_files[0]: #Read in the reference file (first science fits).
        refFile = fits.open(os.path.join(os.getcwd(), \
                  "science_corrected_%ss.fits" %i), output_verify='ignore')
        refData = refFile[0].data
        combine = refData #First value of combine array to combine all fits.
        #Close files now we're done with them.
        refFile.close() #Prevent the file getting stuck in memory.
    if i in (sci_files[1], sci_files[2]): #Shift second and third fits.
        shiftFile = fits.open(os.path.join(os.getcwd(), \
                  "science_corrected_%ss.fits" %i), output_verify='ignore')
        shiftData = shiftFile[0].data
        shiftHeader = shiftFile[0].header
        newShift = interpolation.shift(shiftData, shiftV[j]) #Shift the data.
        fits.writeto("science_shifted_%ss.fits" %i, newShift, shiftHeader, \
                     output_verify='ignore', overwrite=True)
        print("Shifted science file - science_shifted_%ss.fits was saved" %i)
        combine = combine + newShift #Combine the images.
        shiftFile.close() #Prevent the file getting stuck in memory.
        j = j + 1 #Increase value for next loop.

#Write combined image to a fits file.
fits.writeto("science_combined.fits", combine, output_verify='ignore', \
             overwrite=True)
print("Combined science file - science_combined.fits was saved")
