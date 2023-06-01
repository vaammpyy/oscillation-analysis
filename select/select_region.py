# code to select the region and store it in a .csv file.
import matplotlib
import sunpy.visualization.colormaps as cm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_path=input("Enter the path of the data file: ")
gam=eval(input("Enter the gamma value: "))
region_info_path=input("Enter the path to save regions_coords_pixel.csv: ")+"/"

df1=np.load(data_path,allow_pickle='TRUE').item()
data=df1['data']**gam
headr=df1['hdr']

cmap= matplotlib.colormaps['sdoaia171']

toggle=1
region_info={"region name":[],"xi":[],"yi":[],"xf":[],"yf":[]}

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
    plt.plot(x,y,c='lawngreen')
    plt.show()
    plt.close()
    data_region=data[left:right,bottom:top]
    plt.imshow(data_region,origin='lower',cmap=cmap)
    plt.show()
    toggle_1=int(input("Enter 1 to save region, 0 to skip: "))
    if toggle_1==0:
        pass
    if toggle_1==1:
        region_name=input("Enter region name: ")
        region_info["region name"].append(region_name)
        region_info["xi"].append(left)
        region_info["yi"].append(bottom)
        region_info["xf"].append(right)
        region_info["yf"].append(top)
    toggle=int(input("Enter 1 to re-run the code, 0 to end the code: "))

if len(region_info["region name"])>0:
    df=pd.DataFrame(region_info)
    df.to_csv(region_info_path+"regions_coords_pixel.csv",index=False)
else:
    print("Exiting program no region have been saved.")