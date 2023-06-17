from wow import wow
import numpy as np
import os
from glob import glob

data_path=input("Enter the path of the folder containing the data: ")+"/"
save_path=input("Enter the path to save the WOW data: ")+"/"

directory=save_path+"Data_WOW"+"/"

if not os.path.exists(directory):
    os.makedirs(directory)

files=sorted(glob(data_path+"*.npy"))
j=0

for file in files:
    df=np.load(file,allow_pickle='TRUE').item()
    data=df['data']
    header=df['hdr']
    df_wow={'data':wow(data),'hdr':header}
    np.save(directory+f"{j:04d}",df_wow)
    j+=1