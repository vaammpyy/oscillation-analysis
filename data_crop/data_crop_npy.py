import numpy as np
import pandas as pd
import glob
import os

def crop(data,xi,yi,xf,yf):
    return(data[xi:xf,yi:yf])

df=pd.read_csv(input("Enter the path of region_coords_pixel.csv: "),sep=',',header=0,names=["region name","xi","yi","xf","yf"])
region_info=df.to_numpy()
path_to_data=input("Enter the path of the data file: ")
#path_to_save=input("Enter the path to save the cropped region fits file: ")+"/"
files=sorted(glob.glob(path_to_data+"/*.npy"))

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
        read_file=np.load(files[j],allow_pickle='TRUE').item()
        data=read_file['data']
        header=read_file['hdr']
        crop_data=crop(data,xi,yi,xf,yf)
        var_save={'data':crop_data,'hdr':header}
        np.save(directory+f"{j:04d}",var_save)