import numpy as np
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

x,y,z= np.loadtxt(poscar,skiprows=9,unpack=True,max_rows=list_number[-1],dtype='float')
z_min=min(z)
#shift=z_min-10
shift=float(input("input shifiting parameters : "))
coordinate=np.stack((x,y,z),axis=-1)

for ii in range (len(coordinate)):
    coordinate[ii][2] -= shift

np.savetxt('coordinate.txt',coordinate,delimiter='   ',fmt='%f')

old_name1 = "POSCAR.txt"
new_name1 = "POSCAR"


try:
    os.rename(old_name1,new_name1)
except:
    pass