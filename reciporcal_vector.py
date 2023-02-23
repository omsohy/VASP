import numpy as np
import os

old_name1="POSCAR"
new_name2="POSCAR.txt"

try:
    os.rename(old_name1,new_name2)
except:
    pass

#get lattice vector from POSCAR
poscar="POSCAR.txt"
fp=open(poscar)
vectors=[]
for ii,line in enumerate(fp):
    if ii==2 or ii==3 or ii==4 : 
        vector=line.split()
        vector=np.array([float(x) for x in vector])
        vectors.append(vector)    
    elif ii==5:
        break

#Get reciprocal lattice vector
reciprocal=[]
for ii in range(3):
    b=2*np.pi*(np.cross(vectors[(ii+1)%3],vectors[(ii+2)%3]))/(np.dot(vectors[ii],np.cross(vectors[(ii+1)%3],vectors[(ii+2)%3])))
    print(ii)
    reciprocal.append(b)
b1=reciprocal[0]
b2=reciprocal[1]
b3=reciprocal[2]
print(b1)
mag_b1=np.linalg.norm(b1)
print(mag_b1)
print(2*np.pi/vectors[0])