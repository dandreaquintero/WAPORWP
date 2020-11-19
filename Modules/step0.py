import os                     # module for interacting with the operating system
import shapefile              # module foe reading shapefile
import matplotlib.pyplot as plt # module for plotting
#os.chdir(os.path.join(os.path.split(os.getcwd())[0], "Modules"))  # change working directory to 'Modules' folder
print(os.getcwd())
import WaPOR                  # Import local module in 'Modules' folder

print('FINISH IMPORTING WaPOR')


# ####### Read geographical extent of the study area (Study area: Kenya) ################
roi_shapefile=r"../Data/1Boundary/Shapefile/kenya.shp" #path to the shapefile of study area
shape=shapefile.Reader(roi_shapefile) #read shapefile
xmin,ymin,xmax,ymax=shape.bbox #read shapefile extent
print('Extent of study area: lonlim = [{0},{2}], latlim = [{1},{3}]'.format(xmin,ymin,xmax,ymax))


########## plot to check shapefile ################
# plt.figure()
# sf=shape
# for shape in sf.shapeRecords(): #loop over all features in shapefile
#     for i in range(len(shape.shape.parts)): #loop over all points in feature
#         i_start = shape.shape.parts[i]
#         if i==len(shape.shape.parts)-1:
#             i_end = len(shape.shape.points)
#         else:
#             i_end = shape.shape.parts[i+1]
#         x = [i[0] for i in shape.shape.points[i_start:i_end]]
#         y = [i[1] for i in shape.shape.points[i_start:i_end]]
#         plt.plot(x,y)
# plt.show()

############# Bulk-download WaPOR data for the study area extent ############
output_dir=r'../Data' # folder to save data

# PRECIPITATION (Dekadal)
WaPOR.PCP_dekadal(output_dir, Startdate='2018-01-01', Enddate='2018-12-31',
         latlim=[ymin-0.05, ymax+0.05], lonlim=[xmin-0.05, xmax+0.05],level=1,
         version = 2, Waitbar = 1)

# NDVI (Dekadal)
