import numpy as np
import pandas as pd
from astropy.io import fits

df=pd.read_csv(input("Enter path of slits_info_arcsec.csv: "),sep=',',header=0,names=["slit name","xi","yi","xf","yf","width"])
data=df.to_numpy()
path_to_save=input("Enter path to save the slits_info_pixel.csv: ")+"/"
path_to_data=input("Enter the path of the data file for reference pixel information: ")

data1=fits.open(path_to_data)
n=0

cdelt1=data1[n].header['CDELT1']
cdelt2=data1[n].header['CDELT2']
crpix1=data1[n].header['CRPIX1']
crpix2=data1[n].header['CRPIX2']
crval1=data1[n].header['CRVAL1']
crval2=data1[n].header['CRVAL2']

def arcsec_to_pixel(x_data,y_data):
    x=crpix1+(x_data-crval1)/cdelt1
    y=crpix2+(y_data-crval2)/cdelt2
    return(x,y)

slit_name=[]
slit_xi=[]
slit_yi=[]
slit_xf=[]
slit_yf=[]
width=[]

for i in range(np.shape(data)[0]):
    print(i)
    xi, yi=arcsec_to_pixel(data[i,1],data[i,2])
    xf, yf=arcsec_to_pixel(data[i,3],data[i,4])
    slit_name.append(data[i,0])
    slit_xi.append(xi)
    slit_yi.append(yi)
    slit_xf.append(xf)
    slit_yf.append(yf)
    width.append(data[i,5])

df1=pd.DataFrame({"slit name":slit_name,"xi":slit_xi,"yi":slit_yi,"xf":slit_xf,"yf":slit_yf,"width":width})
df1.to_csv(path_to_save+"slits_info_pixel.csv",index=False)