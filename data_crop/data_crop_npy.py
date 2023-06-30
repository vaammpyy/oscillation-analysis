import numpy as np
import pandas as pd
import glob
import os
import configparser as cfg

global left
global right
global bottom
global top
global dx 
global dy 
global n

n=2048

def crop(data,xi,yi,xf,yf):
    return(data[xi:xf,yi:yf])

def arcsec_extent(xi,xf,yf,yi):
    xi=left+dx*xi
    xf=left+dx*xf
    yi=bottom+dy*yi
    yf=bottom+dy*yf
    return(xi,xf,yi,yf)


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
    info_dir=directory+"info/"
    if not os.path.exists(info_dir):
        os.makedirs(info_dir)
    for j in range(len(files)):
        read_file=np.load(files[j],allow_pickle='TRUE').item()
        data=read_file['data']
        header=read_file['hdr']
        crop_data=crop(data,xi,yi,xf,yf)
        var_save={'data':crop_data,'hdr':header}
        np.save(directory+f"{j:04d}",var_save)

    cfg_file=cfg.ConfigParser()
    cfg_file.read(path_to_data+"/info/units.cfg")

    left=eval(cfg_file['ARC-SECOND']['left'])
    right=eval(cfg_file['ARC-SECOND']['right'])
    top=eval(cfg_file['ARC-SECOND']['top'])
    bottom=eval(cfg_file['ARC-SECOND']['bottom'])

    dx=(right-left)/n
    dy=(top-bottom)/n

    x_left, x_right, y_bottom, y_top=arcsec_extent(left,right,top,bottom)

    config=cfg.ConfigParser()
    config['PHYSICAL UNITS']={
        'scale':cfg_file['PHYSICAL UNITS']['scale'],
        'cadence':cfg_file['PHYSICAL UNITS']['cadence']
    }
    config['ARC-SECOND']={
        'left':x_left,
        'right':x_right,
        'bottom':y_bottom,
        'top':y_top
    }

    config['PIXEL LOCATION']={
        'left':xi,
        'right':xf,
        'bottom':yi,
        'top':yf
    }
    with open(info_dir+"/units.cfg",'w') as configfile:
        config.write(configfile)