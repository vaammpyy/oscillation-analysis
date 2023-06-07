
# SLITS ARE NOT APPLIED PERPENDICULAR TO THE LOOP TRACK IS DIVIDED INTO SMALL SECTIONS AND SLIT IS APPLIED PERPENDICULAR TO THAT.
import numpy as np
import matplotlib.pyplot as plt
import sunpy.visualization.colormaps as cm
import matplotlib
import pandas as pd

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
        slit_name.append(f"S{i}")
        x1.append(int(x1_slit_pos))
        x2.append(int(x2_slit_pos))
        y1.append(int(y1_slit_pos))
        y2.append(int(y2_slit_pos))
        width.append(w)
    dictionary={"slit name":slit_name,"xi":x1,"yi":y1,"xf":x2,"yf":y2,"width":width}
    return(dictionary)

cmap= matplotlib.colormaps['sdoaia171']

data_path="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/solo_L2_EUI-HRIEUV174-IMAGE_2022-03-17T03:18:00_2022-03-17T04:02:00/R3/Data/0000.npy"
path_to_save=input("Enter path to save the slit locations and track coordinates: ")+"/"

df=np.load(data_path,allow_pickle='TRUE').item()
data=df['data']
header=df['hdr']

plt.imshow(data,origin='lower',cmap=cmap)
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
plt.imshow(data,origin='lower',cmap=cmap)
for i in range(len(dictionary["xi"])):
    plt.plot([dictionary["xi"][i],dictionary["xf"][i]],[dictionary["yi"][i],dictionary["yf"][i]],color='cyan')
plt.plot(x,y,'r')
plt.xlabel("Pixel")
plt.ylabel("Pixel")
plt.show()
track_dict={"x":x,"y":y}
df_slits=pd.DataFrame(dictionary)
df_slits.to_csv(path_to_save+"slits_location_pixel.csv",index=False)
df_track=pd.DataFrame(track_dict)
df_track.to_csv(path_to_save+"track_coordinates.csv",index=False)
fig.savefig(path_to_save+"loop_track_and_slit.png",dpi=300)