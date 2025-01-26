# Purpose 

The purpose of this tool is to help landowners assess the vegetation of a target area over time. This tool is designed to use multispectral data, specifically the Red and NIR bands, to calculate the Normalized Difference Vegetation Index (NDVI). Then, using the NDVI rasters, the tool will then calculate and return the area of healthy vegetation.

# Input 

This tool takes 7 inputs. The first input is the file path to a folder that contains the input raster bands as well as the output folder. 

The next 2 inputs are the file paths to the Red and NIR bands for the target area. These must be rasters. The second 2 inputs are also the file paths to the Red and NIR bands for the target area, but this is data collected at a different time for the purposes of comparing the amount of healthy vegetation across time. 

I have provided sample LANDSAT data clipped to the extent of the section of the Sawtooth National Forest located in Utah. 

The next input is the threshold value for healthy vegetation. The USGS defines dense vegetation or crops at their peak growth stage as being 0.6 to 0.9 on the NDVI scale. Therefore, **I would suggest a threshold value of 0.6** to be input. However, this value can be adjusted according to the specific situation, which is why I designed it to be input by the user and not hard-coded into the tool. Use this link to read more about this threshold value: https://www.usgs.gov/special-topics/remote-sensing-phenology/science/ndvi-foundation-remote-sensing-phenology

The final input is the path on your computer where you would like to save the PNG images of the two NDVI rasters and the two reclassified rasters. 

# Output 

As stated above, this tool will output four PNG files: two NDVI rasters and two reclassified rasters. The naming conventions for these files is as follows: ndvi1.tif.png for the first set of input bands, ndvi2.tif.png for the second set of input bands, and reclass1.tif.png and reclass2.tif.png, corresponding to the first and second sets of input bands. The .tif part of the name is not intended to be there, but removing it broke the code, so unfortunately each of the files has .tif in the name even though they are .png files. 

The tool will also output 5 lines of text with information about the amount of healthy vegetation:

Total area above threshold for NDVI1: [#] square units

Total area above threshold for NDVI2: [#] square units

Percent healthy vegetation for NDVI1: [#] percent

Percent healthy vegetation for NDVI2: [#] percent

The difference in the amount of healthy vegetation is [#] percent

# Using the tool

To use the tool, you’ll need to import the following modules:

import arcpy

import os

import matplotlib.pyplot as plt

import numpy as np

arcpy.CheckOutExtension('spatial')

You will also need to import the module that holds the tool:

import sys

sys.path.append(r'C:\path\to\folder\containing\tool')

import veg_tool

Then, you will need to set each of the 7 variables:

workspace = r'C:\path\to\workspace'

red_band1 = r'C:\path\to\red_band1'

nir_band1 = r'C:\path\to\nir_band1'

red_band2 = r'C:\path\to\red_band2'

nir_band2 = r'C:\path\to\nir_band2'

threshold = 0.6 (or whatever value you decide)

output_location = r'C:\path\to\output_location'

Finally, call the function:

veg_tool.veg_analysis(workspace, red_band1, nir_band1, red_band2, nir_band2, threshold, output_location)
