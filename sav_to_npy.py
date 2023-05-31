
import numpy as np
from scipy.io.idl import readsav
from types import SimpleNamespace
import glob
import os

def crop(data,xi,yi,xf,yf):
    return(data[xi:xf,yi:yf])

path_to_data=input("Enter the path of the data file: ")
files=sorted(glob.glob(path_to_data+"/*.sav"))

directory=path_to_data+"/"+"Data_npy"+"/"
if not os.path.exists(directory):
    os.makedirs(directory)
for j in range(len(files)):
    df=readsav(files[j], python_dict=True, verbose=True)
    var =  SimpleNamespace(**df)
    data=var.data
    header=var.hdr
    var_save={'data':data,'hdr':header}
    np.save(directory+f"{j:04d}",var_save)