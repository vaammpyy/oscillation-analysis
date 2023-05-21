"""
NAME: make_slit

PURPOSE: Calculates the pixel locations for slits of varying width between start [xi,yi] and stop [xf,yf] pixels.

INPUT: 
[1] Path to a csv file with slit_name,xi,yi,xf,yf,width.
[2] Path to save the slit arrays.

OUTPUT: 
[1] Stores the slit array in a path_to_save/slit_name/slit.npy file.
[2] Stores the slit info in path_to_save/slit_name/info.csv file.

HISTORY: 

[1] Created by Rohan Kumar (IISER Kolkata) on 20-05-2023.
"""


import numpy as np
import pandas as pd
import os

def make_slit(xi,yi,xf,yf,width):
    slit_pix=[]
    length=int(((xi-xf)**2+(yi-yf)**2)**0.5)
    if width!=1:
        slope_slit=(yf-yi)/(xf-xi)
        slope_slit_perp=-1/slope_slit
        theta=np.arctan(slope_slit_perp)
        xi_neg=xi-width/2*np.cos(theta)
        xi_pos=xi+width/2*np.cos(theta)
        yi_neg=yi-width/2*np.sin(theta)
        yi_pos=yi+width/2*np.sin(theta)
        xi=xi_neg+(xi_pos-xi_neg)/(width-1)*np.arange(0,width,1,dtype=int)
        yi=yi_neg+(yi_pos-yi_neg)/(width-1)*np.arange(0,width,1,dtype=int)
        xi=np.asarray(xi,dtype=int)
        yi=np.asarray(yi,dtype=int)
        start_cords=np.column_stack((xi,yi))

        xf_neg=xf-width/2*np.cos(theta)
        xf_pos=xf+width/2*np.cos(theta)
        yf_neg=yf-width/2*np.sin(theta)
        yf_pos=yf+width/2*np.sin(theta)
        xf=xf_neg+(xf_pos-xf_neg)/(width-1)*np.arange(0,width,1,dtype=int)
        yf=yf_neg+(yf_pos-yf_neg)/(width-1)*np.arange(0,width,1,dtype=int)
        xf=np.asarray(xf,dtype=int)
        yf=np.asarray(yf,dtype=int)
        end_cords=np.column_stack((xf,yf))
        for i in range(len(start_cords)):
            slit_coords_x=start_cords[i,0]+(end_cords[i,0]-start_cords[i,0])/(length-1)*np.arange(0,length,1,dtype=int)
            slit_coords_y=start_cords[i,1]+(end_cords[i,1]-start_cords[i,1])/(length-1)*np.arange(0,length,1,dtype=int)
            slit_coords_x=np.asarray(slit_coords_x,dtype=int)
            slit_coords_y=np.asarray(slit_coords_y,dtype=int)
            slit_coords=np.column_stack((slit_coords_x,slit_coords_y))
            slit_pix.append(slit_coords)
    else:
        slit_coords_x=xi+(xf-xi)/(length-1)*np.arange(0,length,1,dtype=int)
        slit_coords_y=yi+(yf-yi)/(length-1)*np.arange(0,length,1,dtype=int)
        slit_coords_x=np.asarray(slit_coords_x,dtype=int)
        slit_coords_y=np.asarray(slit_coords_y,dtype=int)
        slit_coords=np.column_stack((slit_coords_x,slit_coords_y))
        slit_pix.append(slit_coords)
    return(slit_pix)

df=pd.read_csv(input("Enter path of csv file with slit coordinates and names: "),sep=',',header=0,names=["slit name","xi","yi","xf","yf","width"])
path_to_save=input("Enter path to save the slits: ")+"/"

data=df.to_numpy()

for i in range(np.shape(data)[0]):
    slits=make_slit(data[i,1],data[i,2],data[i,3],data[i,4],data[i,5])
    directory=path_to_save+f"{data[i,0]}"+"/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.save(directory+"slits.npy",slits)
    df1=pd.DataFrame({"slit name":[data[i,0]],"xi":[data[i,1]],"yi":[data[i,2]],"xf":[data[i,3]],"yf":[data[i,4]],"width":[data[i,5]],"folder":[directory]})
    df1.to_csv(directory+"info.csv",index=False)