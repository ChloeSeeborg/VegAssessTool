import arcpy
import os
import matplotlib.pyplot as plt
import numpy as np
arcpy.CheckOutExtension('spatial')

def veg_analysis(workspace, red_band1, nir_band1, red_band2, nir_band2, threshold, output_location):
    import arcpy
    # set the workspace
    arcpy.env.workspace = workspace
    # create raster objects for each band
    red1 = arcpy.Raster(red_band1)
    nir1 = arcpy.Raster(nir_band1)
    red2 = arcpy.Raster(red_band2)
    nir2 = arcpy.Raster(nir_band2)
    # calculate ndvi for the first raster
    ndvi1 = (nir1 - red1) / (nir1 + red1)
    # calculaste ndvi for the second raster
    ndvi2 = (nir2 - red2) / (nir2 + red2)
    # save png of each ndvi raster
    ndvi1.save('ndvi1.tif')
    ndvi2.save('ndvi2.tif')
    raster_list = ['ndvi1.tif', 'ndvi2.tif']
    for raster in raster_list:
        raster_path = os.path.join(arcpy.env.workspace, raster)
        # Read the raster into a numpy array.
        array = arcpy.RasterToNumPyArray(raster_path)
        # create a new figure
        plt.figure()
        # plot raster
        plt.imshow(array, cmap='YlGn', vmin=-1, vmax=1)
        # Add a legend.
        plt.colorbar()
        # Save the figure to a png.
        plt.savefig(os.path.join(output_location, f'{raster}.png'))
    # reclassify each raster
    # [min_value, max_value, new_value]
    values = [[-1, threshold, 0],
              [threshold, 1, 1]]
    # Create a RemapRange using the data just created.
    remap = arcpy.sa.RemapRange(remapTable = values)
    ndvi1_reclass = arcpy.sa.Reclassify(in_raster = ndvi1, 
                        reclass_field = 'VALUE', 
                        remap = remap)
    ndvi2_reclass = arcpy.sa.Reclassify(in_raster = ndvi2, 
                        reclass_field = 'VALUE', 
                        remap = remap)
    # save a png of each reclassified raster
    ndvi1_reclass.save('reclass1.tif')
    ndvi2_reclass.save('reclass2.tif')
    reclass_list = ['reclass1.tif', 'reclass2.tif']
    for reclass in reclass_list:
        reclass_path = os.path.join(arcpy.env.workspace, reclass)
        # Read the raster into a numpy array.
        re_array = arcpy.RasterToNumPyArray(reclass_path)
        # create a new figure
        plt.figure()
        # plot raster
        plt.imshow(re_array, cmap='binary', vmin=0, vmax=1)
        # Add a legend.
        plt.colorbar()
        # Save the figure to a png.
        plt.savefig(os.path.join(output_location, f'{reclass}.png'))
    # calculate the area of healthy vegetation for each raster
    # Specify the value you're interested in
    target_value = 1
    # Convert raster to NumPy array
    raster_array1 = arcpy.RasterToNumPyArray(ndvi1_reclass)
    raster_array2 = arcpy.RasterToNumPyArray(ndvi2_reclass)
    # Identify cells with the target value
    target_cells1 = np.where(raster_array1 == target_value)
    target_cells2 = np.where(raster_array2 == target_value)
    # Count of cells with the target value
    cell_count1 = len(target_cells1[0])
    cell_count2 = len(target_cells2[0])
    # Cell size information
    cell_size_x1 = arcpy.GetRasterProperties_management(ndvi1_reclass, "CELLSIZEX")
    cell_size_y1 = arcpy.GetRasterProperties_management(ndvi1_reclass, "CELLSIZEY")
    cell_size_x2 = arcpy.GetRasterProperties_management(ndvi2_reclass, "CELLSIZEX")
    cell_size_y2 = arcpy.GetRasterProperties_management(ndvi2_reclass, "CELLSIZEY")
    # Calculate the area of each cell
    cell_area1 = float(cell_size_x1.getOutput(0)) * float(cell_size_y1.getOutput(0))
    cell_area2 = float(cell_size_x2.getOutput(0)) * float(cell_size_y2.getOutput(0))
    # Calculate the total area with the target value
    healthy_area1 = int(cell_count1 * cell_area1)
    healthy_area2 = int(cell_count2 * cell_area2)
    print(f"Total area above threshold for NDVI1: {healthy_area1} square units")
    print(f"Total area above threshold for NDVI2: {healthy_area2} square units")
    # calculate the percent area of healthy vegetation
    rest_value = 0
    rest_cells1 = np.where(raster_array1 == rest_value)
    rest_cells2 = np.where(raster_array2 == rest_value)
    count_rest1 = len(rest_cells1[0])
    count_rest2 = len(rest_cells2[0])
    total_cells1 = cell_count1 + count_rest1
    total_cells2 = cell_count2 + count_rest2
    total_area1 = cell_area1 * total_cells1
    total_area2 = cell_area2 * total_cells2
    percent_healthy1 = (healthy_area1 / total_area1) * 100
    percent_healthy2 = (healthy_area2 / total_area2) * 100
    print(f"Percent healthy vegetation for NDVI1: {percent_healthy1:.4f} percent")
    print(f"Percent healthy vegetation for NDVI2: {percent_healthy2:.4f} percent")
    # calculate the percent difference of healthy vegetation
    percent_diff = abs(percent_healthy1 - percent_healthy2)
    print(f"The difference in the amount of healthy vegetation is {percent_diff:.4f} percent")
