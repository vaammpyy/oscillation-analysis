# code to select slits and store it in a .csv file
import matplotlib
import sunpy.visualization.colormaps as cm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_path=input("Enter the path of the data file: ")
gam=eval(input("Enter the gamma value: "))
slit_info_path=input("Enter the path to save slits_location_pixel.csv: ")+"/"

df1=np.load(data_path,allow_pickle='TRUE').item()
data=df1['data']**gam
headr=df1['hdr']

cmap= matplotlib.colormaps['sdoaia171']

toggle=1
slit_info={"slit name":[],"xi":[],"yi":[],"xf":[],"yf":[],"width":[]}

while toggle==1:
    fig, ax=plt.subplots()
    if len(slit_info["slit name"])>0:
        for i in range(len(slit_info["slit name"])):
            print(i)
            x_slit=[slit_info["xi"][i],slit_info["xf"][i]]
            y_slit=[slit_info["yi"][i],slit_info["yf"][i]]
            ax.plot([slit_info["yi"][i],slit_info["yf"][i]],[slit_info["xi"][i],slit_info["xf"][i]],c="cyan")
            ax.text(y_slit[0]+5,x_slit[0]+5,slit_info["slit name"][i],c='magenta')
    ax.imshow(data,origin='lower',cmap=cmap)
    a=np.array((plt.ginput(2)))
    a=np.asarray(a,dtype='int')
    x=[a[0,0],a[1,0]]
    y=[a[0,1],a[1,1]]
    left=min(a[0,1],a[1,1])
    right=max(a[0,1],a[1,1])
    top=max(a[0,0],a[1,0])
    bottom=min(a[0,0],a[1,0])
    ax.plot(x,y,c='cyan')
    plt.show()
    toggle_1=int(input("Enter 1 to save slit, 0 to skip: "))
    if toggle_1==0:
        pass
    if toggle_1==1:
        slit_name=input("Enter slit name: ")
        slit_width=int(input("Enter slit width: "))
        slit_info["slit name"].append(slit_name)
        slit_info["xi"].append(left)
        slit_info["yi"].append(bottom)
        slit_info["xf"].append(right)
        slit_info["yf"].append(top)
        slit_info["width"].append(slit_width)
    toggle=int(input("Enter 1 to re-run the code, 0 to end the code: "))

if len(slit_info["slit name"])>0:
    df=pd.DataFrame(slit_info)
    df.to_csv(slit_info_path+"slits_location_pixel.csv",index=False)
else:
    print("Exiting program no slits have been saved.")