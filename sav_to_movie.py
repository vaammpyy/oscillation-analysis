#SAV to video

import matplotlib.pyplot as plt
import matplotlib
import glob
import sunpy.visualization.colormaps as cm
import numpy as np
import os
from scipy.io.idl import readsav
from types import SimpleNamespace

global folder_out
global i
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

cmap= matplotlib.colormaps['sdoaia171']

folder_in="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/solo_L2_EUI-HRIEUV174-IMAGE_2022-03-17T03:18:00_2022-03-17T04:02:00/Data_full/Data"
vid_name="full"
dpi=300
gam=0.35
path_save="img"

os.system("mkdir {}/img".format(folder_in))
vid_name=folder_in+"/"+vid_name
img_save=folder_in+"/"+"img/"
folder_in=folder_in+"/"+"*.sav"


pth_first_file=sorted(glob.glob(folder_in))[0]

#data1=fits.open(pth_first_file)
df1=readsav(pth_first_file, python_dict=True, verbose=True)
var =  SimpleNamespace(**df1)
data1=var.data
header1=var.hdr
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

left=crval1-cdelt1*crpix1
right=crval1+cdelt1*(n2-crpix1)

bottom=crval2-cdelt2*crpix2
top=crval2+cdelt2*(n2-crpix2)
#file=fits.open(pth_first_file)
# df1=readsav(, python_dict=True, verbose=True)
# var =  SimpleNamespace(**df1)
# data=var.data
# header=var.hdr
#dat=file[n].data

def bytescale(image):
    image=image-mini
    image=image/(maxi-mini)
    image=image*255
    image=np.rint(image)
    return(image)

def fits_to_img(path_load):
    df=readsav(path_load, python_dict=True, verbose=True)
    var =  SimpleNamespace(**df)
    dat=var.data
    header=var.hdr
    gamma_transformed_data=dat**gam
    dat=bytescale(gamma_transformed_data)

    plt.figure()
    plt.title(str(header['DATE_D$OBS'][0])[1::]+ " Frame {}".format(i))
    plt.xlabel("Solar-X [arcsec]")
    plt.ylabel("Solar-Y [arcsec]")
    plt.imshow(dat,origin='lower',extent=[left,right,bottom,top],cmap=cmap)
    plt.savefig(img_save+"{:03d}".format(i)+".png",dpi=dpi)
    plt.close()

i=0

for path_load in sorted(glob.glob(folder_in)):
    i+=1
    print("{}/{}".format(i,len(glob.glob(folder_in))))
    fits_to_img(path_load)

cmd='ffmpeg -framerate 60 -start_number 0 -i {}%3d.png -vcodec mpeg4 -vb 20M '.format(img_save)+'{}.mp4'.format(vid_name)
os.system(cmd)
os.system("rm -r {}".format(img_save))
