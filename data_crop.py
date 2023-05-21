import numpy as np
import pandas as pd
from astropy.io import fits
import glob
import matplotlib
import matplotlib.pyplot as plt
import sunpy.visualization.colormaps as cm
import os

def crop(data,xi,yi,xf,yf):
    return(data[xi:xf,yi:yf])

df=pd.read_csv(input("Enter the path of region_coords_pixel.csv: "),sep=',',header=0,names=["region name","xi","yi","xf","yf"])
region_info=df.to_numpy()
path_to_data=input("Enter the path of the data file: ")
#path_to_save=input("Enter the path to save the cropped region fits file: ")+"/"
files=sorted(glob.glob(path_to_data+"/*.fits"))

cmap=matplotlib.colormaps['sdoaia171']

for i in range(np.shape(region_info)[0]):
    region_name=region_info[i,0]
    xi=region_info[i,1]
    yi=region_info[i,2]
    xf=region_info[i,3]
    yf=region_info[i,4]
    directory=path_to_data+"/"+region_name+"/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for j in range(len(files)):
        data_file=fits.open(files[j])
        data=data_file[0].data
        header=data_file[0].header
        crop_data=crop(data,xi,yi,xf,yf)
        fits.writeto(directory+f"{j}.fits",crop_data,header)

        # plt.imshow(crop_data**0.35,origin='lower',cmap=cmap)
        # # plt.plot([xi,xf],[yi,yf])
        # plt.show()


