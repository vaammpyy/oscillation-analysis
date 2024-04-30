# plotting the fitted oscillation with proper axis and start time mentioned

import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import matplotlib
import sunpy.visualization.colormaps as cm
from datetime import datetime, timedelta

d = '2022-03-17 03:18:00'
dt = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')

scale=105
cadence=3
cmap=matplotlib.colormaps['sdoaia171']

def sinusoid(t,Am,P,phi,k,Ao):
    return(Am*np.sin(2*np.pi*t/P+phi)+k*t+Ao)

directory=input("Enter the path of containing the slits: ")+"/"
slit_code=input("Enter slit code: ")
slits=glob.glob(directory+f"{slit_code}*")
i=0
for slit in slits:
    loops=glob.glob(slit+"/"+"L*")
    for loop in loops:
        df_loop_center=pd.read_csv(loop+"/"+"loop_center.csv",sep=',',header=0,names=["Frame","Peak center","Peak error"])
        df_oscillation_parameter=pd.read_csv(loop+"/"+"oscillation_parameter.csv",sep=',',header=0,names=["Amplitude [km]","Amplitude error [km]","Period [s]","Period error [s]","Drift Velocity [km/s]","Drift Velocity error [km/s]","Phase","Phase error","Off-set","Off-set error","Chi-squared [pixel]"])
        df_xt_map=pd.read_csv(loop+"/"+"xt_map.csv",header=None)
        df_box_loc=pd.read_csv(loop+"/"+"box_location.csv",sep=',',header=0,names=["x","y"])
        xt_map=df_xt_map.to_numpy()
        Am=df_oscillation_parameter["Amplitude [km]"][0]
        P=df_oscillation_parameter["Period [s]"][0]
        k=df_oscillation_parameter["Drift Velocity [km/s]"][0]
        phi=df_oscillation_parameter["Phase"][0]
        Ao=df_oscillation_parameter["Off-set"][0]
        loop_x=df_loop_center["Frame"]*cadence
        loop_y=df_loop_center["Peak center"]*scale*0.001
        loop_y_err=df_loop_center["Peak error"]*scale*0.001
        x=np.linspace(0,(np.shape(xt_map)[1]-1)*cadence,1000)
        start_time=dt+timedelta(seconds=int(df_box_loc['y'][0]*cadence))
        fig=plt.figure(figsize=(15,6))
        plt.imshow(xt_map,origin='lower',cmap=cmap,aspect='auto',extent=[0,cadence*np.shape(xt_map)[1],0,0.001*scale*np.shape(xt_map)[0]])
        plt.errorbar(loop_x,loop_y,yerr=loop_y_err,markerfacecolor='cyan',mec='black',ecolor='red',ms=5,fmt='mo',zorder=1)
        plt.xlabel(f"Time [s]\nStart time {start_time}",fontsize=14)
        plt.ylabel("Distance [Mm]",fontsize=14)
        plt.title("Amplitude= %.0f km, Period= %.0f s"%(abs(Am),abs(P)),fontsize=16)
        plt.plot(x,sinusoid(x,Am,P,phi,k,Ao)*0.001,color='blue',linewidth=1,zorder=2)
        plt.ylim(bottom=0,top=0.001*scale*np.shape(xt_map)[0])
        fig.savefig(loop+"/"+"fit_oscillation.png",dpi=300)
        plt.close()
        # plt.show()


