import matplotlib.pyplot as plt
import matplotlib
import glob
import sunpy.visualization.colormaps as cm
import numpy as np
import os
import configparser as cfg

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

# cfg_file=input("Enter the path of config file: ")
# cfg_file=folder_in+"/info/units.cfg"
# config=cfg.ConfigParser()
# config.read(cfg_file)

# left_arcsec=eval(input("Enter the left coordinate in arcsec: "))
# bottom_arcsec=eval(input("Enter the bottom coordinate in arcsec: "))

os.system("mkdir {}/img".format(folder_in))
vid_name=folder_in+"/"+vid_name
img_save=folder_in+"/"+"img/"
folder_in=folder_in+"/"+"*.npy"


pth_first_file=sorted(glob.glob(folder_in))[0]

# #data1=fits.open(pth_first_file)
# # df1=np.load(pth_first_file,allow_pickle='TRUE').item()
# # data1=df1['data']
# # header1=df1['hdr']
# # n=0

# maxi=abs(0.8*header1['DATAMAX'])**gam
# mini=abs(header1['DATAMIN'])**gam

# left=eval(config['ARC-SECOND']['left'])
# right=eval(config['ARC-SECOND']['right'])
# top=eval(config['ARC-SECOND']['top'])
# bottom=eval(config['ARC-SECOND']['bottom'])

def bytescale(image):
    image=image-mini
    image=image/(maxi-mini)
    image=image*255
    image=np.rint(image)
    return(image)

def fits_to_img(path_load):
    df=np.load(path_load,allow_pickle='TRUE').item()
    dat=df['data']
    frame=df['frame']
    # header=df['hdr']
    # gamma_transformed_data=dat**gam
    # dat=bytescale(gamma_transformed_data)

    plt.figure()
    plt.title(frame)
    # plt.xlabel("Solar-X [arcsec]")
    # plt.ylabel("Solar-Y [arcsec]")
    # plt.imshow(dat,origin='lower',extent=[left,right,bottom,top],cmap=cmap)
    plt.imshow(dat,origin='lower',cmap=cmap)
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
