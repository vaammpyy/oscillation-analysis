import os
from sunpy.map import Map
from sunkit_image import coalignment
import glob
#from sunpy.images import coalignment

folder_in=input("Enter input folder path: ")
n=int(input("Enter the number of files to co-align at once: "))

file_out=folder_in+"/"+"co-aligned"
folder_in=folder_in+"/"+"*.fits"

if not os.path.exists(file_out):
    os.makedirs(file_out)

files=sorted(glob.glob(folder_in))
first_file=files[0]

t=0
k=1

for i in range(1,len(files),n):
    name=[]
    name.append(first_file)
    if len(files)-i<=n:
        for j in range(0,len(files)-i):
            name.append(files[i+j])
    else:
        for j in range(0,n):
            name.append(files[i+j])
    mapseq=Map(name,sequence=True)
    coaligned_mapseq=coalignment.mapsequence_coalign_by_match_template(mapseq)
    if t==1:
        coaligned_mapseq=coaligned_mapseq[1::]
        coaligned_mapseq.save(file_out+"/"+"{:03d}".format(k)+"{index:03d}.fits")
        first_file=file_out+"/"+"{:03d}{:03d}.fits".format(k,n-1)
    else:
        coaligned_mapseq=coaligned_mapseq
        coaligned_mapseq.save(file_out+"/"+"{:03d}".format(k)+"{index:03d}.fits")
        first_file=file_out+"/"+"{:03d}{:03d}.fits".format(k,n)
    t=1
    print("Map set {}/{} coalignment completed".format(k,int(len(files)/n)+1))
    k+=1
