from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib
import glob
import sunpy.visualization.colormaps as cm
import numpy as np
import os

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

folder_in=input("Enter folder containing data: ")
vid_name=input("Enter video name: ")
dpi=300
gam=eval(input("Enter gamma value: "))
path_save=input("Enter path to save video: ")

os.system("mkdir {}/img".format(folder_in))
vid_name=folder_in+"/"+vid_name
img_save=folder_in+"/"+"img/"
folder_in=folder_in+"/"+"*.fits"

n=0

# pth_first_file=sorted(glob.glob(folder_in))[0]

# data1=fits.open(pth_first_file)
# n=len(data1)-1
# n1=data1[n].header['NAXIS1']
# n2=data1[n].header['NAXIS2']
# cdelt1=data1[n].header['CDELT1']
# cdelt2=data1[n].header['CDELT2']
# crpix1=data1[n].header['CRPIX1']
# crpix2=data1[n].header['CRPIX2']
# crval1=data1[n].header['CRVAL1']
# crval2=data1[n].header['CRVAL2']
# ax1_unit=data1[n].header['CUNIT1']
# ax2_unit=data1[n].header['CUNIT2']
# maxi=abs(0.8*data1[n].header['DATAMAX'])**gam
# mini=abs(data1[n].header['DATAMIN'])**gam

# # maxi=abs(1.1*data1[n].header['DATAMAX'])**gam
# # mini=abs(0.9*data1[n].header['DATAMIN'])**gam

# left=crval1-cdelt1*crpix1
# right=crval1+cdelt1*(n1-crpix1)

# bottom=crval2-cdelt2*crpix2
# top=crval2+cdelt2*(n2-crpix2)

# file=fits.open(pth_first_file)
#dat=file[n].data

# def bytescale(image):
#     image=image-mini
#     image=image/(maxi-mini)
#     image=image*255
#     image=np.rint(image)
#     return(image)

def fits_to_img(path_load):
    file=fits.open(path_load)
    dat=file[n].data**gam
    # gamma_transformed_data=dat**gam
    # dat=bytescale(gamma_transformed_data)

    plt.figure()
    plt.title(file[n].header['DATE-OBS']+ " Frame {}".format(i))
    # plt.xlabel(ax1_unit)
    # plt.ylabel(ax2_unit)
    #plt.imshow(dat,origin='lower',extent=[left,right,bottom,top],cmap=cmap)
    plt.imshow(dat,origin='lower',cmap='gray')
    plt.savefig(img_save+"{:03d}".format(i)+".png",dpi=dpi)
    plt.close()

i=0

for path_load in sorted(glob.glob(folder_in)):
    i+=1
    print("{}/{}".format(i,len(glob.glob(folder_in))))
    fits_to_img(path_load)

cmd='ffmpeg -framerate 2 -start_number 0 -i {}%3d.png -vcodec mpeg4 -vb 20M '.format(img_save)+'{}.mp4'.format(vid_name)
os.system(cmd)
os.system("rm -r {}".format(img_save))
