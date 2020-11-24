import sys
sys.path.append("../Modules/")  # add Module to the path env variable, so we can import GIS_functions from there.
import os
from GIS_functions import GIS_function as gis
import numpy as np
from useful_functions import get_subdirs
from useful_functions import get_subfiles


def calculate_waterproductivity():
    AOT = 0.8  # above ground over total biomass production ratio (this is  for sugarcane)
    FC = 1.6   # Light use efficiency correction factor
    MC = 0.7   # moisture content, dry matter over freshbiomass

    region_path = '../regions/'
    for region, region_path in get_subdirs(region_path):
        # if region != 'somalia2':
        #     continue
        # calculate biomass
        npp_folder = region_path + '/cubes/L1_NPP_D'
        output_folder_biomass = npp_folder.replace('NPP', 'biomass')

        # if the folder does not exit, make one
        if not os.path.exists(output_folder_biomass):
            os.makedirs(output_folder_biomass)

        for tif_file, tif_file_path in get_subfiles(npp_folder, '.tif'):
            # collecting Geoinfo such as projection, the x and y axis
            driver, NDV, xsize, ysize, GeoT, Projection = gis.GetGeoInfo(tif_file_path)

            npp_array = gis.OpenAsArray(tif_file_path, nan_values=True)
            biomass_array = (AOT * FC * (npp_array * 22.222 / (1 - MC)))/1000  # /1000 to covert from kg to ton [kg/ha]

            # save into output folder
            biomass_file= tif_file.replace('NPP', 'biomass')
            biomass_file_path = os.path.join(output_folder_biomass, biomass_file)
            gis.CreateGeoTiff(biomass_file_path, biomass_array, driver, NDV, xsize, ysize, GeoT, Projection)

        # Calculate Water Productivity
        biomass_path = region_path + '/cubes/L1_biomass_D'
        aeti_path = region_path + '/cubes/L1_AETI_D'
        wp_path = region_path + '/cubes/L1_WP_D'
        # if the folder does not exit, make one
        if not os.path.exists(wp_path):
            os.makedirs(wp_path)

        biomass_list = []
        aeti_list = []

        for _, tif_file_path in get_subfiles(biomass_path):
            biomass_list.append(tif_file_path)

        for _, tif_file_path in get_subfiles(aeti_path):
            aeti_list.append(tif_file_path)

        biomass_list.sort()
        aeti_list.sort()
        print(biomass_list)
        print(aeti_list)
        for biomass_tif, aeti_tif in zip(biomass_list, aeti_list):
            AETI_array = gis.OpenAsArray(aeti_tif, nan_values=True)
            AETI_array[AETI_array == 0] = np.nan
            biomass_array = gis.OpenAsArray(biomass_tif, nan_values=True)
            # save into output folder
            WP_array = biomass_array / AETI_array * 100  # [kg/m3]
            wp_file_path = biomass_tif.replace('biomass', 'WP')
            # collecting Geoinfo such as projection, the x and y axis
            driver, NDV, xsize, ysize, GeoT, Projection = gis.GetGeoInfo(biomass_tif)
            gis.CreateGeoTiff(wp_file_path, WP_array, driver, NDV, xsize, ysize, GeoT, Projection)

calculate_waterproductivity()