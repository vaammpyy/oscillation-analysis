"""
NAME: make_xtmap

PURPOSE: Makes interpolated xt-map of the data according to the provided slits. 

INPUT: 
[1] Path to the folder containing both Data and Slits folder. [A specific format is being followed]

OUTPUT: 
[1] Stores the generated xt_map.csv in the specific slit folder.
[2] Adds the location of the dataset in info.csv

IMPORTANT:
This program requires a very specific folder structure to run.
It takes in parent folder location and picks up data from parent_folder_location/Data/ and picks up slit information from parent_folder_location/Slits/.
It runs for all the slits in the Slits folder. Note that the slits are named S1,S2 and so on in Slits/.

HISTORY: 

[1] Created by Rohan Kumar (IISER Kolkata) on 20-05-2023.
"""


import numpy as np
import glob
import pandas as pd
from scipy.interpolate import interp1d
import os

def apply_slits(slit,data):
    y,x=np.split(slit,2,axis=1)
    x1=x+1
    y1=y+1
    x_1=x-1
    y_1=y-1
    # sl_1=np.column_stack((x1,y1))
    # sl_2=np.column_stack((x_1,y_1))
    # sl_3=np.column_stack((x_1,y1))
    # sl_4=np.column_stack((x1,y_1))
    # pix0=[]
    # pix1=[]
    # pix2=[]
    # pix3=[]
    # pix4=[]
    pix0=data[x,y].T[0]
    pix1=data[x1,y1].T[0]
    pix2=data[x_1,y_1].T[0]
    pix3=data[x_1,y1].T[0]
    pix4=data[x1,y_1].T[0]
    inter_slit_1=interp1d(pix_array,pix0,kind='cubic')
    inter_slit_2=interp1d(pix_array,pix1,kind='cubic')
    inter_slit_3=interp1d(pix_array,pix2,kind='cubic')
    inter_slit_4=interp1d(pix_array,pix3,kind='cubic')
    inter_slit_5=interp1d(pix_array,pix4,kind='cubic')
    return((inter_slit_1(pix_array)+inter_slit_2(pix_array)+inter_slit_3(pix_array)+inter_slit_4(pix_array)+inter_slit_5(pix_array))/5)
    # return((inter_slit_1(pix_array)))
    # return(pix0)

folder_uni=input("Enter path of the folder containing and slits: ")+"/"
slit_code=input("Enter slit code: ")
slit_folder_uni=folder_uni+"Slits"+"/"
for slit_folder in sorted(glob.glob(slit_folder_uni+f"{slit_code}*")):
    xt_map=[]
    k=0
    n=0
    slits=np.load(slit_folder+"/"+"slits.npy")
    df=pd.read_csv(slit_folder+"/"+"info.csv",sep=',',header=0,names=["slit name","xi","yi","xf","yf","width","folder"])
    info_data=df.to_numpy()
    length=int(((info_data[0,1]-info_data[0,3])**2+(info_data[0,2]-info_data[0,4])**2)**0.5)
    pix_array=np.arange(0,length)

    folder_in=folder_uni+"Data"+"/"
    files=sorted(glob.glob(folder_in+"/*.npy"))

    for file in files:
        arr=np.zeros((length,))
        k+=1
        read_file=np.load(file,allow_pickle='TRUE').item()
        data=read_file['data']
        for slit in slits:
            arr+=apply_slits(slit,data) 
        arr=arr/len(slits)
        xt_map.append(arr)

    xt_map=np.array(xt_map)
    np.savetxt(info_data[0,6]+"xt_map.csv",xt_map,delimiter=',')
    cfg_file=folder_in+"info/units.cfg"
    cfg_file_cp=info_data[0,6]+"units.cfg"
    cmd=f"cp {cfg_file} {cfg_file_cp}"
    os.system(cmd)