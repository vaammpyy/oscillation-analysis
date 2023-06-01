# code to plot slits with on the region in megameters
import matplotlib.pyplot as plt
import matplotlib
import glob
import sunpy.visualization.colormaps as cm
import numpy as np
import os
import pandas as pd

global folder_out
global j
global top
global bottom
global left
global right
global mini
global maxi
global dpi
global ax1_unit
global ax2_unit
global gam
global img_name
global n
global cmap
global data_slits
global scale

cmap= matplotlib.colormaps['sdoaia171']

folder_in=input("Enter folder containing data: ")
img_name=input("Enter image name: ")
dpi=300
gam=eval(input("Enter gamma value: "))
slit_location_file=input("Enter the path of file slit_location_pixel.csv: ")

img_name=folder_in+"/"+img_name
folder_in=folder_in+"/"+"*.npy"

pth_first_file=sorted(glob.glob(folder_in))[0]

df1=np.load(pth_first_file,allow_pickle='TRUE').item()
data1=df1['data']
header1=df1['hdr']
n=0

maxi=abs(0.8*header1['DATAMAX'])**gam
mini=abs(header1['DATAMIN'])**gam

n1=header1['NAXIS1'][0]
n2=header1['NAXIS2'][0]
cdelt1=header1['CDELT1'][0]
cdelt2=header1['CDELT2'][0]
crpix1=header1['CRPIX1'][0]
crpix2=header1['CRPIX2'][0]
crval1=header1['CRVAL1'][0]
crval2=header1['CRVAL2'][0]

scale=0.135
left=0
right=np.shape(data1)[0]*scale
top=np.shape(data1)[1]*scale
bottom=0

df=pd.read_csv(slit_location_file,sep=',',header=0,names=["slit name","xi","yi","xf","yf","width"])
data_slits=df.to_numpy()

def fits_to_img(path_load):
    df=np.load(path_load,allow_pickle='TRUE').item()
    dat=df['data']
    header=df['hdr']
    gamma_transformed_data=dat**gam
    dat=gamma_transformed_data
    plt.figure()
    plt.title(str(header['DATE_D$OBS'][0])[1::])
    plt.xlabel("Distance [Mm]")
    plt.ylabel("Distance [Mm]")
    for i in range(np.shape(data_slits)[0]):
        plt.plot([data_slits[i,1]*scale,data_slits[i,3]*scale],[data_slits[i,2]*scale,data_slits[i,4]*scale],label=data_slits[i,0],c='cyan',linewidth=0.8)
        plt.text((data_slits[i,1]-43)*scale,(data_slits[i,2]+5)*scale,data_slits[i,0],c='magenta',fontsize=8)
        #plt.text((data_slits[i,1]+3)*scale,(data_slits[i,2]+13)*scale,data_slits[i,0],c='magenta',fontsize=8)
    plt.imshow(dat,origin='lower',extent=[left,right,bottom,top],cmap=cmap)
    plt.savefig("{}.png".format(img_name),dpi=dpi)
    plt.close()

path_load=sorted(glob.glob(folder_in))[0]
fits_to_img(path_load)