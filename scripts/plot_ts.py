import sys
sys.path.append("../Modules/")  # add Module to the path env variable, so we can import GIS_functions from there.
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from GIS_functions import GIS_function as gis

from useful_functions import get_subdirs
from useful_functions import get_subfiles

def plot_timeseries():
    regions_path = '../regions/'

    for region, region_path in get_subdirs(regions_path):
        # if region != 'somalia2':
        #     continue
        for cube, cube_path in get_subdirs(region_path+'/cubes/'):
           # if 'WP' in cube:
           #     continue
            spatial_avg = []
            time = []
            for tif_file, tif_file_path in get_subfiles(cube_path):
                if tif_file[-4:] == '.tif':   # string ends with .tif
                    raster_enddate = tif_file.split('.')[0].split('*')[1].split(',')[1]
                    time.append(raster_enddate)

                    tif_as_array = gis.OpenAsArray(tif_file_path, nan_values=True)
                    spatial_avg.append(np.nanmean(tif_as_array))  # media in flat array
            print(spatial_avg)
            print(time)

            spatial_avg_sort = [x for _, x in sorted(zip(time, spatial_avg))]
            time_sort = sorted(time)

            #fig = plt.figure(figsize=(8, 8))

            tick_spacing = 12

            fig, ax = plt.subplots(1, 1)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
            # plt.style.use('dark_background')
            plt.xticks(rotation=45)
            ax.plot(time_sort, spatial_avg_sort)
            label_y = cube

            plt.ylabel(label_y)
            plt.tight_layout(pad=4)
            plt.title(cube + ' in ' + region, fontweight="bold")
            plt.grid(linestyle='--')
            # plt.show()

            time_series_path = os.path.join(region_path, 'time_series')
            if not os.path.isdir(time_series_path):
                os.mkdir(time_series_path)

            fig.savefig(os.path.join(time_series_path, cube+'.png'))
plot_timeseries()

