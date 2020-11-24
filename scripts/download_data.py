import sys
sys.path.append("../Modules/")  # add Module to the path env variable, so we can import WaPOR from there.
import WaPOR
import os
import shapefile

from useful_functions import get_subdirs

def download_data():
    cubes_list = ['L1_PCP_D', 'L1_AETI_D', 'L1_NPP_D']  # Precipitation, Actual evapotranspiration, Net primary production
    regions_path = '../regions/'

    stdate = '2010-01-01'
    endate = '2020-10-31'

    for region, region_path in get_subdirs(regions_path):
        if region != 'somalia2':
            continue
        print('Starting with region ', region)
        shapefile_path = region_path+'/shapefile/'+region+'.shp'
        if not os.path.isfile(shapefile_path):
            print('ERROR: no shape file for region ', region)
            continue
        print('Reading shapefile ', shapefile_path)
        shape = shapefile.Reader(shapefile_path)
        xmin, ymin, xmax, ymax = shape.bbox   # read shapefile extent
        download_dir = region_path+'/cubes'

        for cube in cubes_list:
            download_var = "WaPOR." + cube.split('_')[1] + "_dekadal('" + download_dir + "', Startdate=stdate, Enddate=endate, " \
                            "latlim=[ymin-0.05, ymax+0.05], lonlim =[xmin-0.05, xmax+0.05]," \
                            "level=int(cube[1]), version = 2, Waitbar = 1)"

            print(download_var)
            eval(download_var)

download_data()