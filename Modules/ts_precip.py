import geopandas as gpd
import os
import rasterio
import scipy.sparse as sparse
import pandas as pd


# Read the points shapefile using GeoPandas
#file_kenya = gpd.read_file('/Users/danielaquintero/Documents/wapor/WAPORWP/Data/1Boundary/shapefile/kenya.shp')

matrix = pd.DataFrame()

input_path = '../Data/1_L1_PCP_D_resampled'

# Iterate through the rasters and save the data as individual arrays to matrix
for files in os.listdir(input_path):
    if files[-4: ] == '.tif':    # string ends with .tif
        dataset = rasterio.open(input_path + '/' + files)   # save the info from each .tif into the new variable dataset
        data_array = dataset.read(1)
        data_array_sparse = sparse.coo_matrix(data_array)
        data = files[:-4]
        matrix[data] = data_array_sparse.toarray().tolist()
        print('Processing is done for the raster: ' + files[:-4])
#print(len(data_array))

