import sys
sys.path.append("../Modules/")  # add Module to the path env variable, so we can import GIS_functions from there.
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.stats
import pandas as pd
from GIS_functions import GIS_function as gis

from useful_functions import get_subdirs
from useful_functions import get_subfiles

def plot_timeseries():
    regions_path = '../regions/'

    for region, region_path in get_subdirs(regions_path):
        if region != 'somalia2':
            continue

        pcp_folder = region_path + '/cubes/L1_PCP_D'
        wp_folder = region_path + '/cubes/L1_WP_D'
        NDVI_folfer = regions_path + '/cubes/L1_NDVI_D'
        excel_file = region_path + '/cubes/L1_NDVI_D/Somalia2.csv'

        spatial_avg_pcp = []
        time_pcp = []
        spatial_avg_wp = []
        time_wp = []
        for tif_file, tif_file_path in get_subfiles(pcp_folder, '.tif'):
            raster_enddate = tif_file.split('.')[0].split('*')[1].split(',')[1]
            time_pcp.append(raster_enddate)

            tif_as_array_pcp = gis.OpenAsArray(tif_file_path, nan_values=True)
            spatial_avg_pcp.append(np.nanmean(tif_as_array_pcp))  # media in flat array

        for tif_file_wp, tif_file_path_wp in get_subfiles(wp_folder, '.tif'):
            raster_enddate_wp = tif_file_wp.split('.')[0].split('*')[1].split(',')[1]
            time_wp.append(raster_enddate_wp)

            tif_as_array_wp = gis.OpenAsArray(tif_file_path_wp, nan_values=True)
            spatial_avg_wp.append(np.nanmean(tif_as_array_wp))  # media in flat array
        # print(spatial_avg)
        # print(time)

        df = pd.read_csv(excel_file, sep=';', header=0, thousands='.', decimal=',')
        # print(df.dtypes)
        df.rename(columns={'basein_somalia Rainfall': 'rainfall_bacino', 'basin_somalia S10 TOC NDVI': 'ndvi_bacino',
                           'Somalia2 RAINFALL': 'rainfall_region', 'Somalia2 S10 TOC NDVI': 'ndvi_region'}, inplace=True)

        df['ndvi_region'] = df['ndvi_region'].astype(float)
        print(df.head(5))
        x = df.DateTime
        y = df.ndvi_region
        #plt.plot(x, y)


        spatial_avg_sort_pcp = [x for _, x in sorted(zip(time_pcp, spatial_avg_pcp))]
        time_sort_pcp = sorted(time_pcp)

        spatial_avg_sort_wp = [x for _, x in sorted(zip(time_wp, spatial_avg_wp))]
        time_sort_wp = sorted(time_wp)

        scipy.stats.pearsonr(spatial_avg_pcp, spatial_avg_sort_wp)
        print('Pearson correlation:', scipy.stats.pearsonr(spatial_avg_pcp, spatial_avg_sort_wp))

        scipy.stats.spearmanr(spatial_avg_pcp, spatial_avg_sort_wp)
        print('Spearman correlation:', scipy.stats.pearsonr(spatial_avg_pcp, spatial_avg_sort_wp))

        scipy.stats.kendalltau(spatial_avg_pcp, spatial_avg_sort_wp)
        print('Kendall correlation:', scipy.stats.pearsonr(spatial_avg_pcp, spatial_avg_sort_wp))

        tick_spacing = 12
        fig, ax1 = plt.subplots(1, 1)
        # plt.style.use('dark_background')

        plt.xticks(rotation=45, fontsize=6)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        ax1.plot(time_sort_pcp, spatial_avg_sort_pcp, color='royalblue', label='Precipitation')
        ax2.plot(time_sort_wp, spatial_avg_sort_wp, color='mediumseagreen', label='Water productivity')
        #ax3.plot(x, y, color='red', label='NDVI')

        ax1.tick_params(axis='y', labelcolor='royalblue', )
        ax2.tick_params(axis='y', labelcolor='mediumseagreen')

        ax1.set_ylabel('Precipitation [mm]', fontsize=8)
        ax2.set_ylabel('Water Productivity [kg/m3]', fontsize=8)

        ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        ax1.legend(loc=2)
        ax2.legend(loc=1)
        #label_y = cube
        #plt.ylabel(label_y)
        plt.tight_layout(pad=4)
        plt.title('Water Productivity and Precipitation in ' + region, fontweight="bold")
        plt.grid(linestyle='--')
        #plt.legend()
        plt.show()

        time_series_path = os.path.join(region_path, 'time_series')
        if not os.path.isdir(time_series_path):
            os.mkdir(time_series_path)

        fig.savefig(os.path.join(time_series_path, 'wp_pcp.png'), dpi=300)
        plt.close(fig)

        #fig, ax = plt.subplots(2, 1)

plot_timeseries()
