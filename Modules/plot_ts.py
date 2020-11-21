import WaPOR
import gdal
import os
import shapefile
import matplotlib.pyplot as plt
import numpy as np
from GIS_functions import GIS_function as gis
import glob
import pandas as pd
import re

#dani: use relative paths
data_path = "../Data/"
maps_folder = "1Boundary/shapefile/"
out_folder = 'timeseries/'

maps_path = data_path+maps_folder
out_path = data_path+out_folder

# Decide the time range you want to evaluate #####
stdate = '2018-01-01'
endate = '2018-06-30'
timerange = stdate + "," + endate

# Decide the data you want to import, by adding or removing them from the list
evaluation_list = ["PCP", "NPP", "AETI"]  # PCP: dekadal precipitation data

# read the cube info (dataframe) from the catalogue
cube_codePCP = 'L1_PCP_D'
cube_codeAETI = 'L1_AETI_D'
cube_codeRET = 'L1_RET_D'
cube_codeNPP = 'L1_NPP_D'

if not os.path.isdir(out_path):
    os.mkdir(out_path)

# loop to create some folders
k = 0
output = []
mainfolder = []
for word in evaluation_list:
    mainfolder.append(out_path + "/output_" + word + "_" + timerange)
    if not os.path.isdir(mainfolder[k]):
        os.mkdir(mainfolder[k])
    direct = mainfolder[k] + "/output_cubes"
    output.append(direct)
    if not os.path.isdir(output[k]):
        os.mkdir(output[k])
    k +=1

k = 0
sourcefiles = glob.glob(maps_path + '*.shp')
print(sourcefiles)

for file in sourcefiles:
    shape = shapefile.Reader(file)
    xmin, ymin, xmax, ymax = shape.bbox
    for word in evaluation_list:
        output_string = ("output[%d]" % k)
        download_var = "WaPOR." + word + "_dekadal(" + output_string + ", Startdate=stdate, Enddate=endate, " \
                                                    "latlim=[ymin-0.05, ymax+0.05], lonlim =[xmin-0.05, xmax+0.05]," \
                                                    "level=1, version = 2, Waitbar = 1)"
        print(download_var)
        print(output[k])

        tif_folder = eval(download_var) # dani: fixed input_folder. you need to modify your PCP_dekadal.py to return Dir

        actual_cubecode = "cube_code" + word
        cube_code = eval(actual_cubecode)
        print(actual_cubecode, cube_code)
        time_range = timerange

        print(tif_folder)
        tif_list = glob.glob(tif_folder + '/*.tif')

        #  Import the dates corresponding to the raster layers of WaPOR (cube code)
        excel_folder = mainfolder[k] + "/Data_excel"
        if not os.path.isdir(excel_folder):
            os.mkdir(excel_folder)
        df_availT = WaPOR.API.getAvailData(cube_code, time_range)
        output_folder = excel_folder

        df_availT.to_excel(os.path.join(output_folder, 'df_avail_' + word + '.xlsx'))

        spatial_avg = []
        time = []
        for tif_file in tif_list:
            raster_id = os.path.split(tif_file)[-1].split('.')[0]  # dani: fixed raster id
            raster_info = df_availT.loc[df_availT['raster_id'] == raster_id]
            print(raster_id)
            print(raster_info)
            raster_startdate = raster_info['time_code'].iloc[0].split(',')[0]

            raster_startdate = re.sub(r"[[)]", "", raster_startdate)

            raster_enddate = raster_info['time_code'].iloc[0].split(',')[-1]
            raster_enddate = re.sub(r"[[)]", "", raster_enddate)
            time.append(raster_enddate)
            tif_as_array = gis.OpenAsArray(tif_file, nan_values=True)
            spatial_avg.append(np.nanmean(tif_as_array))  # media in flat array

        print(spatial_avg)
        print(time)
        # dani: fixed order of timestamps
        tutti_s = [x for _, x in sorted(zip(time, spatial_avg))]
        time_s = sorted(time)

        plt.figure(figsize=(8, 8))
        x = np.arange(len(tutti_s))
        plt.xticks(x, time_s[::1], rotation=45)
        # plt.locator_params(axis='x', nbins=len(x)/20)
        plt.plot(time_s, tutti_s)
        if word == "PCP":
            label_y = "Precipitation [mm]"
        elif word == "T":
            label_y = "Net Transpiration [mm]"
        plt.ylabel(label_y)
        plt.tight_layout(pad=4)
        plt.grid()
        plt.show()
        sf = shape
        k = k + 1

    # for shape in sf.shapeRecords():  # loop over all features in shapefile
    #     for i in range(len(shape.shape.parts)):  # loop over all points in feature
    #         i_start = shape.shape.parts[i]
    #         if i == len(shape.shape.parts) - 1:
    #             i_end = len(shape.shape.points)
    #         else:
    #             i_end = shape.shape.parts[i + 1]
    #         x = [i[0] for i in shape.shape.points[i_start:i_end]]
    #         y = [i[1] for i in shape.shape.points[i_start:i_end]]
    #         plt.plot(x, y)
    #         plt.title("Study Area. \n Lat from %1.5s to %1.5s, Long from %1.5s  to %1.5s" % (xmin, xmax, ymin, ymax))
    #
    #  plt.show()