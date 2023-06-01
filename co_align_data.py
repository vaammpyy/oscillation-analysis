import os
from sunpy.map import Map
from sunkit_image import coalignment
#from sunpy.images import coalignment

folder_in=input("Enter input folder path: ")

file_out=folder_in+"/"+"co-aligned"
folder_in=folder_in+"/"+"*.fits"

if not os.path.exists(file_out):
    os.makedirs(file_out)

mapseq=Map(folder_in,sequence=True)
coaligned_mapseq=coalignment.mapsequence_coalign_by_match_template(mapseq)

coaligned_mapseq.save(file_out+"/"+"{index:03d}.fits")
