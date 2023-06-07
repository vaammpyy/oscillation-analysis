import pandas as pd
import matplotlib
import sunpy.visualization.colormaps as cm
import matplotlib.pyplot as plt
import glob
import numpy as np

cmap=matplotlib.colormaps['sdoaia171']

path_to_slits=input("Enter the path of folder containitng Slits: ")+"/"

slits=sorted(glob.glob(path_to_slits+"S*"))
scale=0.135
cadence=3

xt_map_name=input("Enter the name scheme of <xt-map-name.csv>: ")
gam=eval(input("Enter the value of gamma: "))

for slit in slits:
    xt_map=pd.read_csv(slit+"/"+xt_map_name)
    xt_map_data=xt_map.to_numpy().T
    slit_info=pd.read_csv(slit+"/"+"info.csv",sep=',',header=0,names=["slit name","xi","yi","xf","yf","width","folder"])
    slit_info_data=slit_info.to_numpy()
    fig=plt.figure(figsize=(15,6))
    left=0
    bottom=0
    right=np.shape(xt_map_data)[1]*cadence
    top=np.shape(xt_map_data)[0]*scale
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.imshow(xt_map_data**gam,origin='lower',extent=[left,right,bottom,top],cmap=cmap,aspect='auto')
    plt.xlabel("Time [s]",fontsize=22)
    plt.ylabel("Distance [Mm]",fontsize=22)
    plt.title(f"{slit_info_data[0,0]}",fontsize=20)
    plt.tight_layout()
    plt.savefig(slit+"/"+f"{xt_map_name[0:-4]}.png",dpi=100)

