import numpy as np
import pandas as pd
from astropy.io import fits

df=pd.read_csv(input("Enter path of slits_location_megameter.csv: "),sep=',',header=0,names=["x","y"])
data=df.to_numpy()
slit_name_r1=["S1","S2","S4","S5","S6","S7","S8"]
slit_name_r2=["S3","S9","S10","S11","S12","S13"]
path_to_save=input("Enter path to save the slits_location_pixel.csv: ")+"/"

scale=135

def megameter_to_pixel(x_data,y_data):
    x=int(x_data/scale)
    y=int(y_data/scale)
    return(x,y)

slit_name=[]
slit_xi=[]
slit_yi=[]
slit_xf=[]
slit_yf=[]
width=[]
t=0

for i in range(0,np.shape(data)[0],2):
    xi, yi=megameter_to_pixel(data[i,0],data[i,1])
    xf, yf=megameter_to_pixel(data[i+1,0],data[i+1,1])
    slit_name.append(slit_name_r2[t])
    slit_xi.append(xi)
    slit_yi.append(yi)
    slit_xf.append(xf)
    slit_yf.append(yf)
    width.append(5)
    t+=1

df1=pd.DataFrame({"slit name":slit_name,"xi":slit_xi,"yi":slit_yi,"xf":slit_xf,"yf":slit_yf,"width":width})
df1.to_csv(path_to_save+"slits_location_pixel.csv",index=False)