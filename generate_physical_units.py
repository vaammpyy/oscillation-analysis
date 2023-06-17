import configparser as cfg
import numpy as np

def arcsec_to_radians(theta):
    radians= 4.848*10**(-6)*theta
    return(radians)

data_file=input("Enter the path of the data file: ")
cadence=input("Enter the cadence value: ")
save_path=input("Enter the path to save the config file: ")

read_file=np.load(data_file,allow_pickle='TRUE').item()
data=read_file['data']
header=read_file['hdr']

n1=header['NAXIS2'][0]
n2=header['NAXIS2'][0]
cdelt1=header['CDELT1'][0]
cdelt2=header['CDELT2'][0]
crpix1=header['CRPIX1'][0]
crpix2=header['CRPIX2'][0]
crval1=header['CRVAL1'][0]
crval2=header['CRVAL2'][0]

left=crval1-cdelt1*crpix1
right=crval1+cdelt1*(n1-crpix1)

bottom=crval2-cdelt2*crpix2
top=crval2+cdelt2*(n2-crpix2)

distance=header['DSUN_OBS'][0]
radians=arcsec_to_radians(cdelt1)
scale=distance*radians*10**(-3)

config=cfg.ConfigParser()

config['PHYSICAL UNITS']={'scale':scale,
                          'cadence':cadence}

config['ARC-SECOND']={
    'left':left,
    'right':right,
    'bottom':bottom,
    'top':top
}

with open(save_path+"/units.cfg",'w') as configfile:
    config.write(configfile)