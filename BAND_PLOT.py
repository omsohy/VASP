# Put this code in the directory containing A and B and running it.

import numpy as np
import matplotlib.pyplot as plt
import os

#POSCAR and EIGENVAL files are needed in same directory
Fermi_E=float(input('Input Fermi Energy of your structure : '))
old_name = "EIGENVAL"
new_name = "EIGENVAL.txt"

old_name1="POSCAR"
new_name2="POSCAR.txt"


try:
    os.rename(old_name,new_name)
except:
    pass

try:
    os.rename(old_name1,new_name2)
except:
    pass

eigenval='EIGENVAL.txt'
poscar="POSCAR.txt"

#get lattice vector from POSCAR
fp=open(poscar)
vectors=[]
for ii,line in enumerate(fp):
    if ii==2 or ii==3 or ii==4 : 
        vector=line.split()
        vector=np.array([float(x) for x in vector])
        vectors.append(vector)    
    elif ii==5:
        break

#calculate reciprocal lattice vector
reciprocal=[]
for ii in range(3):
    b=2*np.pi*(np.cross(vectors[(ii+1)%3],vectors[(ii+2)%3]))/(np.dot(vectors[ii],np.cross(vectors[(ii+1)%3],vectors[(ii+2)%3])))
    reciprocal.append(b)
b1=reciprocal[0]
b2=reciprocal[1]
b3=reciprocal[2]

#read basic information from EIGENVAL
fp = open(eigenval)
for ii, line in enumerate(fp):
    if ii == 5:
        line6 = line
        num_electrons,num_kpoint,num_band = line6.split()
    elif ii == 8:
        line8 = line
        line8 = line8.split()
        if len(line8)==5:
            ISPIN2 = True
        else:
            ISPIN2 = False
        
        break
        
num_kpoint=int(num_kpoint)
num_band=int(num_band)

#get relative coordinate from EIGENVAL
head=7
band=[]
Kpoints=[]
skip=0
for ii in range(num_kpoint):
    x, y, z ,Q = np.loadtxt(eigenval,skiprows=head+(num_band+2)*skip,unpack=True,max_rows=1)
    
    Kpoints.append([x,y,z])
    skip+=1


#get Band's value from EIGANVAL
skip=0
if ISPIN2 == False:
    for ii in range(num_kpoint):
        band_index,E,R = np.loadtxt(eigenval,skiprows=(head+1)+(num_band+2)*skip,unpack=True,max_rows=num_band)
        band.append(E)
        skip+=1
elif ISPIN2 == True:
    for ii in range(num_kpoint):
        band_index,E_up,E_down,R_up,R_down = np.loadtxt(eigenval,skiprows=(head+1)+(num_band+2)*skip,unpack=True,max_rows=num_band)
        band.append(E_up)
        skip+=1

#Transpose Band's value to plot
np.array(band)
band=np.transpose(band)

Kpoints=np.array(Kpoints)
x_axis = np.arange(len(Kpoints))

#Make x_axis by multiply relative coordinates, reciprocal vectors

xticks=[0]
ds=[]

#magnitude of reciprocal vectors..
mag_b1=np.linalg.norm(b1)
mag_b2=np.linalg.norm(b2)
mag_b3=np.linalg.norm(b3)
for ii in range(1,len(Kpoints)):
    s=((mag_b1*Kpoints[ii][0]-mag_b1*Kpoints[ii-1][0])**2+(mag_b2*Kpoints[ii][1]-mag_b2*Kpoints[ii-1][1])**2+(mag_b3*Kpoints[ii][2]-mag_b3*Kpoints[ii-1][2])**2)**0.5
    ds.append(s)
x_axis=np.concatenate([np.zeros(1),np.cumsum(ds)])

#get high symmetry points from EIGENVAL
for ii in range(1,len(x_axis)):
    if x_axis[ii] == x_axis[ii-1]:
        xticks.append(x_axis[ii])
xticks.append(x_axis[-1])

fig=plt.figure()
ax=plt.subplot()


#plot
for i in range(num_band):
    ax.plot(x_axis,band[i]-Fermi_E ,'-',color='b',lw=1)

#상황에 맞게 ylim 설정
plt.ylim((-3,3))
plt.ylabel('E-$E_f$(eV)')
plt.yticks(fontsize=13)
plt.axhline(color='k',ls='--')
for ii in xticks:
    plt.axvline(ii,color='k',ls='-')
#KPOINTS file에서 만든 KPOINTS point들을 표기해줘야함...
plt.xticks(xticks,labels=[r'$\Gamma$','X','M',r'$\Gamma$'])
plt.savefig('BAND.png')


old_name = "EIGENVAL.txt"
new_name = "EIGENVAL"

try:
    os.rename(old_name,new_name)
except:
    pass

