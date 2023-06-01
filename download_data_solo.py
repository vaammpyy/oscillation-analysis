from importlib.resources import path
import sunpy_soar
from sunpy.net import Fido
from sunpy.net.attrs import Instrument, Level, Time
from sunpy_soar.attrs import Identifier
import os

inst=input("Instrument name: ")
t_1=input("Start Time: ")
t_2=input("End Time: ")
lvl=input("Data Level: ")
iden=input("Data Identifier: ")
pth=input("Path to save: ")

folder_name=pth+"/"+"solo"+"_"+lvl+"_"+iden+"_"+t_1+"_"+t_2+"/"

os.system("mkdir {}".format(folder_name))

instrument = Instrument(inst)
time = Time(t_1,t_2)
level = Level(lvl)
identifier = Identifier(iden)

result = Fido.search(instrument, time, level, identifier)

files = Fido.fetch(result,path=folder_name)
