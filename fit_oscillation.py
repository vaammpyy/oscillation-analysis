"""
NAME: fit_oscillation

PURPOSE: Fits a sinusoidal curve on zoomed in XT-map to find out the oscillation parameters. This program can be run as many times as the user wants depending on the menu selection.

INPUT: 
[1] Path to the Slit folder which contains xt_map.csv.
[2] Asks user to select the region where the oscillation is prominent.
[3] For sinusoidal fit takes in the value of the range of guess periods.

OUTPUT: 
[1] Makes a folder for storing all information related to the selected region of the xt_map in slit_folder/loop_name/.
[2] Makes a file slit_folder/loop_name/xt_map.csv, for storing the zoomed in xt_map.
[3] Makes a file slit_folder/loop_name/loop_center.csv, for storing the fitted centers of the loops in the zoomed in xt_map.
[4] Makes a file slit_folder/loop_name/box_location.csv, for storing the location of the points in pixels for zooming in the xt_map.
[5] Makes a file slit_folder/loop_name/oscillation.png, for storing the plot of zoomed in xt_map with loop centers and sinusoidal fit.
[6] Makes a file slit_folder/loop_name/oscillation_parameter.csv, for storing the parameters of the sinusoidal fit.

IMPORTANT:
This program requires a very specific folder structure to run.
It takes in slit_folder location and picks up slit_folder/xt_map.csv, for fitting the oscillations present in this xt_map.

HISTORY: 

[1] Created by Rohan Kumar (IISER Kolkata) on 20-05-2023.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.ndimage import center_of_mass
from scipy.signal import lombscargle
import matplotlib.pyplot as plt
import matplotlib
import sunpy.visualization.colormaps as cm
import os
import pandas as pd


def gaussian(x,A,mu,sigma,const):
    return(A*np.exp(-(x-mu)**2/(2*sigma**2))+const)

def sinusoid(t,Am,P,phi,k,Ao):
    return(Am*np.sin(2*np.pi*t/P+phi)+k*t+Ao)

def find_peak(y):
    # making the slice of compatible dimension
    y=y[::,0]
    l=len(y)
    x=np.arange(0,l)
    com=center_of_mass(y)[0]
    avg=np.average(y)
    maxi=np.argmax(y)
    std=np.std(y)
    try:
        parameters = curve_fit(gaussian, x, y,p0=[com,maxi,std,avg])[0]
        fit_y=gaussian(x,parameters[0],parameters[1],parameters[2],parameters[3])
        index_max=np.argmax(fit_y)
        if abs(parameters[2])<10 and 0<parameters[1]<l:
            # return(index_max)
            return(parameters[1])
    except RuntimeError:
        pass

def chi_squared(expected,observed):
    chi=0
    for i in range(len(expected)):
        chi+=(expected[i]-observed[i*10])**2/expected[i]
    return(chi)
    
directory=input("Enter the path of the slit: ")+"/"

data = np.loadtxt(directory+"xt_map.csv",delimiter=",", dtype=float)

cadence=3
scale=135

cmap=matplotlib.colormaps['sdoaia171']

toggle=1

while toggle==1:
    fig=plt.figure()
    plt.imshow(data,origin='lower',cmap=cmap)
    a=np.array((plt.ginput(2)))
    a=np.asarray(a,dtype='int')
    x=[a[0,0],a[1,0],a[1,0],a[0,0],a[0,0]]
    y=[a[0,1],a[0,1],a[1,1],a[1,1],a[0,1]]
    left=min(a[0,1],a[1,1])
    right=max(a[0,1],a[1,1])
    top=max(a[0,0],a[1,0])
    bottom=min(a[0,0],a[1,0])
    mid_frame=int((right+left)/2)
    plt.plot(x,y,c='cyan')
    plt.show()
    plt.close()
    data_osci=data[left:right,bottom:top]
    plt.imshow(data_osci,origin='lower',cmap=cmap)
    plt.show()


    # breaking the xt-map in slices then fitting gaussian on each slice
    slices=np.hsplit(data_osci,len(data_osci[0]))
    peak=[]
    t=[]

    for i in range(len(slices)):
        peak_loc=find_peak(slices[i])
        if peak_loc!=None:
            t.append(i)
            peak.append(peak_loc)


    guess_amplitude=np.max(peak)-np.mean(peak)
    periods=np.linspace(eval(input("Enter period start: ")),eval(input("Enter period end: ")),1000)
    pgram=lombscargle(t,peak,periods)
    guess_period=periods[np.argmax(pgram)]
    guess_phase=0
    guess_offset=np.mean(peak)
    guess_drift=(peak[-1]-peak[0])/len(peak)
    guess=[guess_amplitude,guess_period,guess_phase,guess_drift,guess_offset]
    t_fit=np.linspace(t[0],t[-1],10*len(t))

    try:
        sine_param=curve_fit(sinusoid,t,peak,p0=guess)[0]
    except RuntimeError:
        print("Sinusoidal fit did not converge")

    fig=plt.figure(figsize=(8,8))
    plt.imshow(data_osci,origin='lower',cmap=cmap)
    plt.scatter(t,peak,color='cyan',s=0.5)
    try:
        sine=sinusoid(t_fit,sine_param[0],sine_param[1],sine_param[2],sine_param[3],sine_param[4])
        plt.plot(t_fit,sine,color='magenta',linewidth=0.6)
        chi_sq=chi_squared(peak,sine)
        plt.title(r"$A_m=$%.3f km, $P=$%.3f s, $\phi=$%.3f, $k=$%.3f km/s, $\chi^2$=%.3f"%(abs(sine_param[0]*scale),sine_param[1]*cadence,sine_param[2],sine_param[3]*scale/cadence,chi_sq))
    #    plt.savefig(directory+f"xt_map_fit.png",dpi=300)
    except NameError:
        print("Can't plot Sinusoidal parameters not found!")
    plt.show()

    toggle_1=int(input("Enter 1 to save oscillation, 0 to skip: "))
    if toggle_1==0:
        pass
    if toggle_1==1:
        loop_name=input("Enter loop name: ")
        save_path=directory+loop_name+"/"
        os.makedirs(save_path)
        np.savetxt(save_path+"xt_map.csv",data_osci,delimiter=',')
        df_loop_center=pd.DataFrame({"Frame":t,"Peak center":peak})
        df_loop_center.to_csv(save_path+"loop_center.csv",index=False)
        df_box_loc=pd.DataFrame({"x":[left,right],"y":[bottom,top]})
        df_box_loc.to_csv(save_path+"box_location.csv",index=False)
        fig.savefig(save_path+"oscillation.png",dpi=300)
        df_oscillation_parameter=pd.DataFrame({"Amplitude [km]":[abs(sine_param[0]*scale)],"Period [s]":[sine_param[1]*cadence],"Drift Velocity [km/s]":[sine_param[3]*scale/cadence],"Phase":[sine_param[2]],"Chi-squared [pixel]":[chi_sq]})
        df_oscillation_parameter.to_csv(save_path+"oscillation_parameter.csv",index=False)
    toggle=int(input("Enter 1 to re-run the code, 0 to end the code: "))

