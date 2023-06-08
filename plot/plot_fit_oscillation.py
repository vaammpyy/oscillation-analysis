# plotting the fitted oscillation with proper axis and start time mentioned

import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import matplotlib
import sunpy.visualization.colormaps as cm

scale=135
cadence=3
cmap=matplotlib.colormaps['sdoaia171']

def sinusoid(t,Am,P,phi,k,Ao):
    return(Am*np.sin(2*np.pi*t/P+phi)+k*t+Ao)

directory=input("Enter the path of containing the slits: ")+"/"
slits=glob.glob(directory+"S*")
i=0
for slit in slits:
    loops=glob.glob(slit+"/"+"L*")
    for loop in loops:
        df_loop_center=pd.read_csv(loop+"/"+"loop_center.csv",sep=',',header=0,names=["Frame","Peak center"])
        df_oscillation_parameter=pd.read_csv(loop+"/"+"oscillation_parameter.csv",sep=',',header=0,names=["Amplitude [km]","Period [s]","Drift Velocity [km/s]","Phase","Off-set","Chi-squared [pixel]"])
        df_xt_map=pd.read_csv(loop+"/"+"xt_map.csv",header=None)
        xt_map=df_xt_map.to_numpy()
        # Am=df_oscillation_parameter["Amplitude [km]"][0]/scale
        # P=df_oscillation_parameter["Period [s]"][0]/cadence
        # k=df_oscillation_parameter["Drift Velocity [km/s]"][0]/scale*cadence
        # phi=df_oscillation_parameter["Phase"][0]
        # Ao=df_oscillation_parameter["Off-set"][0]/scale
        # loop_x=df_loop_center["Frame"]
        # loop_y=df_loop_center["Peak center"]
        # x=np.linspace(0,np.shape(xt_map)[1]-1,1000)
        Am=df_oscillation_parameter["Amplitude [km]"][0]
        P=df_oscillation_parameter["Period [s]"][0]
        k=df_oscillation_parameter["Drift Velocity [km/s]"][0]
        phi=df_oscillation_parameter["Phase"][0]
        Ao=df_oscillation_parameter["Off-set"][0]
        loop_x=df_loop_center["Frame"]*cadence
        loop_y=df_loop_center["Peak center"]*scale*0.001
        x=np.linspace(0,(np.shape(xt_map)[1]-1)*cadence,1000)
        fig=plt.figure(figsize=(15,6))
        plt.imshow(xt_map,origin='lower',cmap=cmap,aspect='auto',extent=[0,cadence*np.shape(xt_map)[1],0,0.001*scale*np.shape(xt_map)[0]])
        plt.scatter(loop_x,loop_y,color='cyan',s=5)
        plt.xlabel("Time [s]")
        plt.ylabel("Distance [Mm]")
        plt.title(slit.split("/")[-1]+"/"+loop.split("/")[-1])
        plt.plot(x,sinusoid(x,Am,P,phi,k,Ao)*0.001,color='magenta',linewidth=1)
        plt.ylim(bottom=0)
        plt.show()
        i+=1

print(i)

