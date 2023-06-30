import numpy as np
import matplotlib.pyplot as plt
import sunpy.visualization.colormaps as cm
import pandas as pd
import glob 
import matplotlib

global scale
global cadence
# global Am
# global phi
# global k
# global Ao
# global P
global frame
global loop_center

# def sinusoid(t,Am,P,phi,k,Ao):
#     return(Am*np.sin(2*np.pi*t/P+phi)+k*t+Ao)

def loop_pos():
    if df_slit_info['xi'][0]>df_slit_info['xf'][0]:
        # y=sinusoid(frame, Am, P, phi, k, Ao)-df_loop_info['x'][0]
        y=loop_center-df_loop_info['x'][0]
    else:
        # y=sinusoid(frame, Am, P, phi, k, Ao)+df_loop_info['x'][0]
        y=loop_center+df_loop_info['x'][0]
    return(y)

def loop_length(x1,y1,x2,y2):
    d=((x1-x2)**2+(y1-y2)**2)**0.5
    length=np.pi*d/2
    length_Mm=length*scale*0.001
    return(length_Mm)

scale=135
cadence=3
cmap=matplotlib.colormaps['sdoaia171']

#data_path=input("Enter the path of folder containing Data: ")+"/*.npy"
data_path="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/solo_L2_EUI-HRIEUV174-IMAGE_2022-03-17T03:18:00_2022-03-17T04:02:00/R1/Data"+"/*.npy"
# slit_info_path=input("Enter path of info.csv of the slit: ")
slit_info_path="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/solo_L2_EUI-HRIEUV174-IMAGE_2022-03-17T03:18:00_2022-03-17T04:02:00/R1/Slits/S1/info.csv"
print(f"DATA PATH: {data_path}")
print(f"SLIT PATH: {slit_info_path}")
loop_path=input("Enter the path of the loop folder: ")+"/"
#loop_path="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/solo_L2_EUI-HRIEUV174-IMAGE_2022-03-17T03:18:00_2022-03-17T04:02:00/oscillations/S1/L1"+"/"

data_files=sorted(glob.glob(data_path))

df_slit_info=pd.read_csv(slit_info_path,sep=',',header=0,names=["slit name","xi","yi","xf","yf","width","folder"])
slit_info=df_slit_info.to_numpy()

df_loop_info=pd.read_csv(loop_path+"box_location.csv",sep=',',header=0,names=["x","y"])

start_frame=df_loop_info["y"][0]
stop_frame=df_loop_info["y"][1]

# df_oscillation_param=pd.read_csv(loop_path+"oscillation_parameter.csv",sep=",",header=0,names=["Amplitude [km]","Period [s]","Drift Velocity [km/s]","Phase","Off-set","Chi-squared [pixel]"])

# Am=df_oscillation_param["Amplitude [km]"][0]/scale
# P=df_oscillation_param["Period [s]"][0]/cadence
# k=df_oscillation_param["Drift Velocity [km/s]"][0]/scale*cadence
# phi=df_oscillation_param["Phase"][0]
# Ao=df_oscillation_param["Off-set"][0]/scale

df_oscillation=pd.read_csv(loop_path+"loop_center.csv",sep=",",header=0,names=["Frame","Peak center","Peak error"])

frame=df_oscillation["Frame"][0]
loop_center=df_oscillation['Peak center'][0]

data_oscillation=data_files[start_frame:stop_frame]
df_data=np.load(data_oscillation[frame],allow_pickle='TRUE').item()
data=df_data['data']

xi_slit=df_slit_info['xi']
yi_slit=df_slit_info['yi']
xf_slit=df_slit_info['xf']
yf_slit=df_slit_info['yf']

loop_mean_pos=loop_pos()

slope=(yf_slit-yi_slit)/(xf_slit-xi_slit)
theta=np.arctan(slope)
x_loop=xi_slit+loop_mean_pos*np.cos(theta)
y_loop=yi_slit+loop_mean_pos*np.sin(theta)

toggle=0

while toggle==0:
    plt.imshow(data**0.04,origin='lower',cmap=cmap)
    plt.scatter([df_slit_info['xi']],[df_slit_info['yi']],c='red',marker='x',zorder=2)
    plt.scatter([x_loop],[y_loop],c='blue',marker='x',zorder=2)
    plt.plot([df_slit_info['xi'],df_slit_info['xf']],[df_slit_info['yi'],df_slit_info['yf']],c='cyan',zorder=1)
    plt.title(f"Frame:{frame+start_frame}")
    plt.show(block=False)
    loop_input=input("Enter the loop footpoint coordinates x1 y1 x2 y2: ")
    plt.close()
    loop_footpoints=list(map(float,loop_input.split(" ")))
    fig=plt.figure()
    plt.imshow(data**0.04,origin='lower',cmap=cmap)
    plt.scatter([df_slit_info['xi']],[df_slit_info['yi']],c='red',marker='x',zorder=2)
    plt.scatter([x_loop],[y_loop],c='blue',marker='x',zorder=2)
    plt.plot([df_slit_info['xi'],df_slit_info['xf']],[df_slit_info['yi'],df_slit_info['yf']],c='cyan',zorder=1)
    plt.scatter(loop_footpoints[0::2],loop_footpoints[1::2],c='blue',marker='x')
    plt.xlabel("pixel")
    plt.ylabel("pixel")
    plt.show()
    loop_length_Mm=loop_length(loop_footpoints[0], loop_footpoints[1],loop_footpoints[2], loop_footpoints[3])   
    dictonary={"x1":[loop_footpoints[0]],"y1":[loop_footpoints[1]],"x2":[loop_footpoints[2]],"y2":[loop_footpoints[3]],"Loop Length [Mm]":[loop_length_Mm]}
    df_loop_length=pd.DataFrame(dictonary)
    toggle=input("Enter 1 to save 0 to re-enter footpoints: ")

fig.savefig(loop_path+"loop_footpoints.png",dpi=300)
df_loop_length.to_csv(loop_path+"loop_length.csv",index=False)
