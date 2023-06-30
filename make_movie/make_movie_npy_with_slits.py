#npy to video with slits

import matplotlib.pyplot as plt
import matplotlib
import glob
import sunpy.visualization.colormaps as cm
import numpy as np
import os
import pandas as pd
import configparser as cfg

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
global path_save
global img_save
global n
global cmap
global data_slits
global scale

cmap= matplotlib.colormaps['sdoaia171']

folder_in=input("Enter folder containing data: ")
vid_name=input("Enter video name: ")
dpi=300
gam=eval(input("Enter gamma value: "))
path_save=input("Enter path to save video: ")
slit_location_file=input("Enter the path of file slit_location_pixel.csv: ")

cfg_file=folder_in+"/info/units.cfg"
config=cfg.ConfigParser()
config.read(cfg_file)

os.system("mkdir {}/img".format(folder_in))
vid_name=folder_in+"/"+vid_name
img_save=folder_in+"/"+"img/"
folder_in=folder_in+"/"+"*.npy"


pth_first_file=sorted(glob.glob(folder_in))[0]

#data1=fits.open(pth_first_file)
df1=np.load(pth_first_file,allow_pickle='TRUE').item()
data1=df1['data']
header1=df1['hdr']
n=0

maxi=abs(0.8*header1['DATAMAX'])**gam
mini=abs(header1['DATAMIN'])**gam

scale=eval(config['PHYSICAL UNITS']['scale'])*10**(-3)
left=0
right=np.shape(data1)[0]*scale
top=np.shape(data1)[1]*scale
bottom=0


df=pd.read_csv(slit_location_file,sep=',',header=0,names=["slit name","xi","yi","xf","yf","width"])
data_slits=df.to_numpy()

def bytescale(image):
    image=image-mini
    image=image/(maxi-mini)
    image=image*255
    image=np.rint(image)
    return(image)

def fits_to_img(path_load):
    df=np.load(path_load,allow_pickle='TRUE').item()
    dat=df['data']
    header=df['hdr']
    gamma_transformed_data=dat**gam
    dat=bytescale(gamma_transformed_data)

    plt.figure()
    plt.title(str(header['DATE_D$OBS'][0])[1::]+ " Frame {}".format(j))
    plt.xlabel("Distance [Mm]")
    plt.ylabel("Distance [Mm]")
    for i in range(np.shape(data_slits)[0]):
        plt.plot([data_slits[i,1]*scale,data_slits[i,3]*scale],[data_slits[i,2]*scale,data_slits[i,4]*scale],label=data_slits[i,0],c='cyan',linewidth=0.8)
        plt.text((data_slits[i,1]-43)*scale,(data_slits[i,2]+5)*scale,data_slits[i,0],c='magenta',fontsize=8)
    plt.imshow(dat,origin='lower',extent=[left,right,bottom,top],cmap=cmap)
    plt.savefig(img_save+"{:03d}".format(j)+".png",dpi=dpi)
    plt.close()

j=0

for path_load in sorted(glob.glob(folder_in)):
    j+=1
    print("{}/{}".format(j,len(glob.glob(folder_in))))
    fits_to_img(path_load)

cmd='ffmpeg -framerate 60 -start_number 0 -i {}%3d.png -vcodec mpeg4 -vb 20M '.format(img_save)+'{}.mp4'.format(vid_name)
os.system(cmd)
os.system("rm -r {}".format(img_save))