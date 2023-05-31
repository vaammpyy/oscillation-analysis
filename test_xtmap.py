import numpy as np
import glob
import pandas as pd
from scipy.io.idl import readsav
from types import SimpleNamespace
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def apply_slits(slit,data):
    x,y=np.split(slit,2,axis=1)
    x1=x+1
    y1=y+1
    x_1=x-1
    y_1=y-1
    sl_1=np.column_stack((x1,y1))
    sl_2=np.column_stack((x_1,y_1))
    sl_3=np.column_stack((x_1,y1))
    sl_4=np.column_stack((x1,y_1))
    pix0=[]
    pix1=[]
    pix2=[]
    pix3=[]
    pix4=[]
    for i in range(len(x)):
        pix0.append(data[slit[i][0],slit[i][1]])
        pix1.append(data[sl_1[i][0],sl_1[i][1]])
        pix2.append(data[sl_2[i][0],sl_2[i][1]])
        pix3.append(data[sl_3[i][0],sl_3[i][1]])
        pix4.append(data[sl_4[i][0],sl_4[i][1]])
    inter_slit_1=interp1d(pix_array,pix0,kind='cubic')
    inter_slit_2=interp1d(pix_array,pix1,kind='cubic')
    inter_slit_3=interp1d(pix_array,pix2,kind='cubic')
    inter_slit_4=interp1d(pix_array,pix3,kind='cubic')
    inter_slit_5=interp1d(pix_array,pix4,kind='cubic')
    return((inter_slit_1(pix_array)+inter_slit_2(pix_array)+inter_slit_3(pix_array)+inter_slit_4(pix_array)+inter_slit_5(pix_array))/5)

folder_uni="/home/vampy/acads/projects/Probing_high_freq_waves_in_corona/Data/Test Data"+"/"
slit_folder_uni=folder_uni+"Slits"+"/"
for slit_folder in sorted(glob.glob(slit_folder_uni+"S*")):
    xt_map=[]
    k=0
    n=0
    slits=np.load(slit_folder+"/"+"slits.npy")
    df=pd.read_csv(slit_folder+"/"+"info.csv",sep=',',header=0,names=["slit name","xi","yi","xf","yf","width","folder"])
    info_data=df.to_numpy()
    length=int(((info_data[0,1]-info_data[0,3])**2+(info_data[0,2]-info_data[0,4])**2)**0.5)
    pix_array=np.arange(0,length)

    folder_in=folder_uni+"Data"+"/"+"filter_cube_2796.sav"
    df=readsav(folder_in)
    var=SimpleNamespace(**df)
    print(np.shape(var.filter_cube))
    file=var.filter_cube
    #print(np.shape(var))

    for i in range(np.shape(file)[0]):
        plt.imshow(file[i],vmin=-5,vmax=5)
        plt.show()
        arr=np.zeros((length,))
        k+=1
        #file=fits.open(file)
        data=file[i]
        for slit in slits:
            arr+=apply_slits(slit,data) 
            arr=arr/len(slits)
        xt_map.append(arr)

    xt_map=np.array(xt_map)
    np.savetxt(folder_uni+"xt_map.csv",xt_map.T,delimiter=',')
    # df["dataset"]=folder_in
    # df.to_csv(slit_folder+"/"+"info.csv",index=False)
