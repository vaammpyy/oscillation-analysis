# code to plot the cropped region on the full image
import matplotlib
import sunpy.visualization.colormaps as cm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import configparser as cfg

cmap=matplotlib.colormaps['sdoaia171']

data_path=input("Enter the path of the data folder: ")
region_info_path=input("Enter the path of the file regions_coords_pixel.csv: ")
path_save=input("Enter path to save the image: ")+"/"
image_name=input("Enter the name of the image: ")

df1=np.load(data_path+"/0000.npy",allow_pickle='TRUE').item()
data=df1['data']
header=df1['hdr']
df=pd.read_csv(region_info_path,sep=',',header=0,names=["region name","xi","yi","xf","yf"])
region_info=df.to_numpy()

config_file=data_path+"/info/units.cfg"

config=cfg.ConfigParser()
config.read(config_file)

scale=eval(config['PHYSICAL UNITS']['scale'])

n1=header['NAXIS1'][0]
n2=header['NAXIS2'][0]
cdelt1=header['CDELT1'][0]
cdelt2=header['CDELT2'][0]
crpix1=header['CRPIX1'][0]
crpix2=header['CRPIX2'][0]
crval1=header['CRVAL1'][0]
crval2=header['CRVAL2'][0]

left=crval1-cdelt1*crpix1
right=crval1+cdelt1*(n2-crpix1)

bottom=crval2-cdelt2*crpix2
top=crval2+cdelt2*(n2-crpix2)

def pixel_to_arcsec(x_data,y_data):
    x=crval1+(x_data-crpix1)*cdelt1
    y=crval2+(y_data-crpix2)*cdelt2
    return([x,y])

plt.imshow(data**0.35,cmap=cmap,origin='lower')

for i in range(np.shape(region_info)[0]):
    r1_y1, r1_x1, r1_y2, r1_x2=region_info[i,1],region_info[i,2],region_info[i,3],region_info[i,4]

    r1_x=[r1_x1,r1_x1,r1_x2,r1_x2,r1_x1]
    r1_y=[r1_y1,r1_y2,r1_y2,r1_y1,r1_y1]

    plt.plot(r1_x,r1_y,c='lawngreen')
    # plt.plot(r2_x,r2_y,c='lawngreen')
    plt.text(r1_x2-50,r1_y2+50,region_info[i,0],c='lawngreen')
    # plt.text(r2_x2-50,r2_y2+50,"R2",c='lawngreen')
    # plt.xlabel("Solar-X [arcsec]")
    # plt.ylabel("Solar-Y arcsec")
    plt.xlabel("Pixels")
    plt.ylabel("Pixels")
    plt.grid(True,color='k',linestyle='--',linewidth=0.5)
plt.savefig(path_save+image_name+".png",dpi=300)