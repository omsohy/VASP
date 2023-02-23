import numpy as np
import matplotlib.pyplot as plt
import os

old_name1 = "POSCAR"
new_name1 = "POSCAR.txt"


try:
    os.rename(old_name1,new_name1)
except:
    pass

poscar='POSCAR.txt'

fp = open(poscar)
for i, line in enumerate(fp):
    if i == 5:
        ion=line
    elif i == 6:
        number=line
    elif i > 6:
        break
ion=ion.split()
number=number.split()
number = [int (i) for i in number]
fp.close()

list_number=[0]+number
list_number=np.array(list_number)
list_number=np.cumsum(list_number)

x,y,z = np.loadtxt(poscar,skiprows=8,unpack=True,max_rows=list_number[-1],dtype='float')
coordinate=np.stack((x,y,z),axis=-1)

for aa in range(1,len(list_number)):
    first, last = list_number[aa-1],list_number[aa]
    for jj in range(first,last):
        for kk in range(jj+1,last):
            if coordinate[jj][2] > coordinate[kk][2]:
                a=coordinate[jj].copy()
                b=coordinate[kk].copy()
                coordinate[jj]=b
                coordinate[kk]=a
            else:
                pass

np.savetxt('coordinate.txt',coordinate,delimiter='   ',fmt='%f')

old_name1 = "POSCAR.txt"
new_name1 = "POSCAR"


try:
    os.rename(old_name1,new_name1)
except:
    pass