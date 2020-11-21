import os                             # a module for interacting with the operating system
import glob                           # used to retrieve files/pathnames matching a specified pattern
import matplotlib.pyplot as plt       # is a plotting library used for 2D graphics in python
import numpy as np                    # stands for 'Numerical Python, is a python library used for scientific computing with arrays
from osgeo import ogr, gdal
import subprocess

import os
os.chdir(os.path.join(os.path.split(os.getcwd())[0], "Modules"))
import WaPOR                                # API to interact with WaPOR portal
WaPOR.API.version = 2

# os.chdir(os.path.join(os.path.split(os.getcwd())[0], "Modules"))
from GIS_functions import GIS_function as gis

# ######################## RESAMPLE PRECIPITATION ####################################
# Import the input data
dir_proj = os.path.split(os.getcwd())[0]
dir_data = "Data"

source_file = os.path.join(dir_proj, dir_data, "WAPOR.v2_mm-dekad-1_L2_AETI_D", "L2_AETI_1701.tif")  # Read gdal info of template raster file
target_folder = os.path.join(dir_proj, dir_data, "WAPOR.v2_mm-dekad-1_L1_PCP_D")  # data to be resampled
target_fhs = glob.glob(target_folder + '/*.tif')


# The size and shape of the raster files
template = gis.OpenAsArray(source_file, nan_values=True)
original = gis.OpenAsArray(target_fhs[0], nan_values=True)

print('The size & shape of the template raster      =', template.size,  '&', template.shape)
print('The size & shape of the data to be resampled =', original.size,  '&', original.shape)

# Make or connect with the directory the output folder
dir_proj = os.path.split(os.getcwd())[0]
dir_data = "Data"

output_folder = os.path.join(dir_proj, dir_data, "1_L1_PCP_D_resampled")

#  Make one if the folder does not exit
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
print(output_folder)

# Resample raster data
Resample = gis.MatchProjResNDV(source_file, target_fhs, output_folder, resample='near', dtype='float32')

# The size and shape of the resampled raster files
Resampled = os.path.join(dir_proj, dir_data,   "1_L1_PCP_D_resampled", "L1_PCP_1701.tif")
resampled = gis.OpenAsArray(Resampled, nan_values=True)
print('The size & shape of the resampled data =', resampled.size,  '&', resampled.shape)




