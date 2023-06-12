
# SLITS ARE NOT APPLIED PERPENDICULAR TO THE LOOP TRACK IS DIVIDED INTO SMALL SECTIONS AND SLIT IS APPLIED PERPENDICULAR TO THAT.
import numpy as np
import matplotlib.pyplot as plt
import sunpy.visualization.colormaps as cm
import matplotlib
import pandas as pd
import os

global loop_name
# global scale
# global cadence
# scale=135
# cadence=3

# def sinusoid(t,Am,P,phi,k,Ao):
#     return(Am*np.sin(2*np.pi*t/P+phi)+k*t+Ao)

# def loop_pos():
#     if df_slit_info['xi'][0]>df_slit_info['xf'][0]:
#         y=sinusoid(frame, Am, P, phi, k, Ao)-df_loop_info['x'][0]
#     else:
#         y=sinusoid(frame, Am, P, phi, k, Ao)+df_loop_info['x'][0]
#     return(y)
# def calc_points(x,y,distance):
#     x_points=[]
#     y_points=[]
#     for i in range(len(x)):

def slit_pos(x,y,length,w):
    slit_name=[]
    x1=[]
    x2=[]
    y1=[]
    y2=[]
    width=[]
    length=length/2
    for i in range(1,len(x)):
        slope=(y[i]-y[i-1])/(x[i]-x[i-1])
        slope=-1/slope
        theta=np.arctan(slope)
        x1_slit_pos=(x[i]+x[i-1])/2-length*np.cos(theta)
        y1_slit_pos=(y[i]+y[i-1])/2-length*np.sin(theta)
        x2_slit_pos=(x[i]+x[i-1])/2+length*np.cos(theta)
        y2_slit_pos=(y[i]+y[i-1])/2+length*np.sin(theta)
        slit_name.append(f"{loop_name}_S{i}")
        x1.append(round(x1_slit_pos))
        x2.append(round(x2_slit_pos))
        y1.append(round(y1_slit_pos))
        y2.append(round(y2_slit_pos))
        width.append(w)
    dictionary={"slit name":slit_name,"xi":x1,"yi":y1,"xf":x2,"yf":y2,"width":width}
    return(dictionary)

cmap= matplotlib.colormaps['sdoaia171']

#data_path="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/solo_L2_EUI-HRIEUV174-IMAGE_2022-03-17T03:18:00_2022-03-17T04:02:00/R3/Data/0000.npy"
data_path=input("Enter path of the data file: ")
path_to_save=input("Enter path to save the slit locations and track coordinates: ")+"/"
loop_name=input("Enter the loop name <single-Slit-name_Loop-name>: ")
# ref_loop=input("Enter the path of the loop to track: ")

# df_loop_info=pd.read_csv(ref_loop+"box_location.csv",sep=',',header=0,names=["x","y"])

# start_frame=df_loop_info["y"][0]
# stop_frame=df_loop_info["y"][1]

# frame=0

# df_oscillation_param=pd.read_csv(ref_loop+"oscillation_parameter.csv",sep=",",header=0,names=["Amplitude [km]","Period [s]","Drift Velocity [km/s]","Phase","Off-set","Chi-squared [pixel]"])
# Am=df_oscillation_param["Amplitude [km]"][0]/scale
# P=df_oscillation_param["Period [s]"][0]/cadence
# k=df_oscillation_param["Drift Velocity [km/s]"][0]/scale*cadence
# phi=df_oscillation_param["Phase"][0]
# Ao=df_oscillation_param["Off-set"][0]/scale

directory=path_to_save+loop_name+"/"

if not os.path.exists(directory):
    os.makedirs(directory)

df=np.load(data_path,allow_pickle='TRUE').item()
data=df['data']
header=df['hdr']

gam=0.25

plt.imshow(data**gam,origin='lower',cmap=cmap)
a=plt.ginput(-1)
x=[x for x,y in a]
y=[y for x,y in a]
plt.plot(x,y,'r')
plt.show()

n=int(input("Enter number of slits: "))
length=int(input("Enter the length of each slit: "))
width=int(input("Enter width of each slit: "))
distance=int(len(x)/n)

x_points=x[0::distance]
y_points=y[0::distance]
dictionary=slit_pos(x_points,y_points,length,width)
fig=plt.figure()
plt.imshow(data**gam,origin='lower',cmap=cmap)
for i in range(len(dictionary["xi"])):
    plt.plot([dictionary["xi"][i],dictionary["xf"][i]],[dictionary["yi"][i],dictionary["yf"][i]],color='cyan')
plt.plot(x,y,'r')
plt.xlabel("Pixel")
plt.ylabel("Pixel")
plt.show()
track_dict={"x":x,"y":y}
df_slits=pd.DataFrame(dictionary)
df_slits.to_csv(directory+"slits_location_pixel.csv",index=False)
df_track=pd.DataFrame(track_dict)
df_track.to_csv(directory+"track_coordinates.csv",index=False)
fig.savefig(directory+"loop_track_and_slit.png",dpi=300)