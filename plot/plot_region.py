# code to plot the cropped region on the full image
import matplotlib
import sunpy.visualization.colormaps as cm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

cmap=matplotlib.colormaps['sdoaia171']

data_path=input("Enter the path of the data file: ")
region_info_path=input("Enter the path of the file regions_coords_pixel.csv: ")
path_save=input("Enter path to save the image: ")+"/"
image_name=input("Enter the name of the image: ")

df1=np.load(data_path,allow_pickle='TRUE').item()
data=df1['data']
header=df1['hdr']
df=pd.read_csv(region_info_path,sep=',',header=0,names=["region name","xi","yi","xf","yf"])
region_info=df.to_numpy()

n1=header['NAXIS1'][0]
n2=header['NAXIS2'][0]
cdelt1=header['CDELT1'][0]
cdelt2=header['CDELT2'][0]
crpix1=header['CRPIX1'][0]
crpix2=header['CRPIX2'][0]
crval1=header['CRVAL1'][0]
crval2=header['CRVAL2'][0]

left=crval1-cdelt1*crpix1
right=crval1+cdelt1*(n2-crpix1)

bottom=crval2-cdelt2*crpix2
top=crval2+cdelt2*(n2-crpix2)

def pixel_to_arcsec(x_data,y_data):
    x=crval1+(x_data-crpix1)*cdelt1
    y=crval2+(y_data-crpix2)*cdelt2
    return([x,y])

r1_y1, r1_x1, r1_y2, r1_x2=region_info[0,1],region_info[0,2],region_info[0,3],region_info[0,4]
r2_x1, r2_y1, r2_x2, r2_y2=region_info[1,1],region_info[1,2],region_info[1,3],region_info[1,4]

r1_x1, r1_y1=pixel_to_arcsec(r1_x1,r1_y1)
r1_x2, r1_y2=pixel_to_arcsec(r1_x2,r1_y2)
r2_x1, r2_y1=pixel_to_arcsec(r2_x1,r2_y1)
r2_x2, r2_y2=pixel_to_arcsec(r2_x2,r2_y2)

r1_x=[r1_x1,r1_x1,r1_x2,r1_x2,r1_x1]
r1_y=[r1_y1,r1_y2,r1_y2,r1_y1,r1_y1]
r2_x=[r2_x1,r2_x1,r2_x2,r2_x2,r2_x1]
r2_y=[r2_y1,r2_y2,r2_y2,r2_y1,r2_y1]

data=data**0.35

scale=135

plt.imshow(data,cmap=cmap,extent=[left,right,bottom,top],origin='lower')
plt.plot(r1_x,r1_y,c='lawngreen')
plt.plot(r2_x,r2_y,c='lawngreen')
plt.text(r1_x2-50,r1_y2+50,"R1",c='lawngreen')
plt.text(r2_x2-50,r2_y2+50,"R2",c='lawngreen')
plt.xlabel("Solar-X [arcsec]")
plt.ylabel("Solar-Y arcsec")
plt.grid(True,color='k',linestyle='--',linewidth=0.5)
plt.savefig(path_save+image_name+".png",dpi=300)