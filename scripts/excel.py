import pandas as pd
import matplotlib.pyplot as plt
from useful_functions import get_subdirs
from useful_functions import get_subfiles

def plot_excel():
    regions_path = '../regions/'
    for region, region_path in get_subdirs(regions_path):
        if region != 'somalia2':
            continue

        excel_file = region_path + '/excel_data/somalia2.csv'
        df = pd.read_csv(excel_file, sep=';', header=0, thousands='.', decimal=',')

        df.rename(columns={'basein_somalia Rainfall': 'rainfall_bacino', 'basin_somalia S10 TOC NDVI':'ndvi_bacino', 'Somalia2 RAINFALL': 'rainfall_region', 'Somalia2 S10 TOC NDVI': 'ndvi_region'}, inplace=True)
        #df.drop(['B', 'C'], axis=1)
        df.drop(df.index[0:37], inplace=True)
        #df.drop(df.index[83], inplace=True)
        print(df.head(10))

        # df['ndvi_region'] = df['ndvi_region'].astype(float)
        # print(df.head(5))
        # x = df.DateTime
        # y = df.ndvi_region
        # plt.plot(x, y)
        # plt.show()

plot_excel()