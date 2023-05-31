from astropy.convolution import convolve, Box1DKernel
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt

def smoothing(slice,width):
    return(convolve(slice,Box1DKernel(width)))

slits_dir=input("Enter the path to directory containing slits: ")+"/"

width=67

for slit_folder in sorted(glob.glob(slits_dir+"S*")):
    smooth_map=[]
    path_xt_map=slit_folder+"/"+"xt_map.csv"
    xt_map_file=pd.read_csv(path_xt_map)
    xt_map=xt_map_file.to_numpy().T
    rows=np.array_split(xt_map,np.shape(xt_map)[0],axis=0)
    for j in range(np.shape(rows)[0]):
        smooth_map.append(smoothing(rows[j][0],width))
    smooth_map=np.array(smooth_map)
    np.savetxt(slit_folder+"/"+f"xt_map_smooth_{int(width*3)}.csv",(xt_map-smooth_map).T,delimiter=',')