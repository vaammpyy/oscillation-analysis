# generating synthetic oscillation
import numpy as np
import pandas as pd

def gaussian(x,sigma,mu,A):
    gauss=A*np.exp(-(x-mu)**2/sigma)
    return(gauss)

def sinusoid(x,A,P):
    sine=A*np.sin(2*np.pi/P*x)
    return(sine)

# frames=500
# P=300
# A_sine=0.2
# A_gauss=0.8
# sigma=60
# theta=np.pi/10

frames=int(input("Enter the number of frames: "))
P=int(input("Enter the oscillation period: "))
A_sine=eval(input("Enter the oscillation amplitude: "))
A_gauss=eval(input("Enter the brightness of the loop: "))
sigma=eval(input("Enter the width of the loop: "))/2
theta=np.pi/180*eval(input("Enter the tilt angle of the loop: "))
bkg=int(input("Enter 1 for random background 0 for constant 0 intensity background: "))

save_path=input("Enter the save path of the loops: ")+"/"

dictionary={"Amplitude":[A_sine], "Period":[P], "Brightness":[A_gauss], "Width":[sigma], "Tilt":[theta]}
df=pd.DataFrame(dictionary)
df.to_csv(save_path+"oscillation.csv",index=False)

for i in range(frames):
    column=np.arange(0,100)
    image=np.zeros((100,100))
    for j in range(100):
        x=sinusoid(i,A_sine,P)+(j-50)*np.tan(theta)+50
        gauss_col=gaussian(column,sigma,x,A_gauss)
        # #plt.scatter(column,gauss_col)
        image[::,j]=gauss_col+j
    
    if bkg==1:
        image=image+np.random.rand(100,100)
        # image=image+np.ones((100,100))*i
    else:
        image=image
    # image=image
    frame={'data':image,'frame':i}
    np.save(save_path+f"{i:04d}.npy",frame)