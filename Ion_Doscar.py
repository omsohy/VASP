#In directory, you should have Subdirectory 3_dos which has DOSCAR and POSCAR
#This code will make each ions' DOS in 'figures' directory

from ast import Is
from pickle import TRUE
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

#data from 3_dos
os.chdir('3_dos/')

#import data from POSCAR
old_name1 = "POSCAR"
new_name1 = "POSCAR.txt"

old_name2 = "DOSCAR"
new_name2 = "DOSCAR.txt"

try:
    os.rename(old_name1,new_name1)
    os.rename(old_name2,new_name2)
except:
    pass

poscar='POSCAR.txt'
doscar='DOSCAR.txt'

NEDOS=2000

#order of ions and number of ions

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

#import Fermi_Energy
fp = open(doscar)
for i, line in enumerate(fp):
    if i == 5:
        A=line
    
    elif i == 7:
        check_ispin=line
    
    elif i == (NEDOS+6+1):
        #checking if doscar include f_orbital or not
        check_f=line
        break

fp.close()
A=A.split()
Fermi_E=float(A[3])


#check spin
check_ispin=check_ispin.split()
if len(check_ispin)==5:
    ISPIN2 = True
else:
    ISPIN2 = False


check_f=check_f.split()
if ISPIN2==True:
    if len(check_f)==33:
        check_F = True
    else:
        check_F = False
else:
    if len(check_f)==17:
        check_F = True
    else:
        check_F = False

if ISPIN2 == True:
    E_tot,Dos_tot_up,Dos_tot_down,Cum_tot_up,Cum_tot_down = np.loadtxt(doscar,skiprows=6,unpack=True,max_rows=2000)
else:
    E_tot,Dos_tot,Cum_tot = np.loadtxt(doscar,skiprows=6,unpack=True,max_rows=NEDOS)
#check if f orbitals are calculated and make list for PDOS

NEDOS=int(NEDOS)
skip=0
PDOS=[]
s_orbital=[]
p_orbital=[]
d_orbital=[]
f_orbital=[]

if ISPIN2==True:
    for ii in range(sum(number)):
        E,s1u,s1d,p1u,p1d,p2u,p2d,p3u,p3d,d1u,d1d,d2u,d2d,d3u,d3d,d4u,d4d,d5u,d5d,f1u,f1d,f2u,f2d,f3u,f3d,f4u,f4d,f5u,f5d,f6u,f6d,f7u,f7d = np.loadtxt(doscar,skiprows=6+NEDOS+1+(NEDOS+1)*skip,unpack=True,max_rows=NEDOS)
        S=s1u+s1d
        P=p1u+p1d+p2u+p2d+p3u+p3d
        D=d1u+d1d+d2u+d2d+d3u+d3d+d4u+d4d+d5u+d5d
        F=f1u+f1d+f2u+f2d+f3u+f3d+f4u+f4d+f5u+f5d+f6u+f6d+f7u+f7d
        X=s1u+s1d+p1u+p1d+p2u+p2d+p3u+p3d+d1u+d1d+d2u+d2d+d3u+d3d+d4u+d4d+d5u+d5d+f1u+f1d+f2u+f2d+f3u+f3d+f4u+f4d+f5u+f5d+f6u+f6d+f7u+f7d
        
        s_orbital.append(S)
        p_orbital.append(P)
        d_orbital.append(D)
        f_orbital.append(F)
        PDOS.append(X)
        skip+=1
else:     
    if check_F==True:
        for ii in range(sum(number)):
            E,s1,p1,p2,p3,d1,d2,d3,d4,d5,f1,f2,f3,f4,f5,f6,f7 = np.loadtxt(doscar,skiprows=6+NEDOS+1+(NEDOS+1)*skip,unpack=True,max_rows=NEDOS)

            S=s1
            P=p1+p2+p3
            D=d1+d2+d3+d4+d5
            F=f1+f2+f3+f4+f5+f6+f7
            X=s1+p1+p2+p3+d1+d2+d3+d4+d5+f1+f2+f3+f4+f5+f6+f7
 
            s_orbital.append(S)
            p_orbital.append(P)
            d_orbital.append(D)
            f_orbital.append(F)
            PDOS.append(X)

            skip+=1
    elif check_F == False:
        for ii in range(sum(number)):
            E,s1,p1,p2,p3,d1,d2,d3,d4,d5 = np.loadtxt(doscar,skiprows=6+NEDOS+1+(NEDOS+1)*skip,unpack=True,max_rows=NEDOS)

            S=s1
            P=p1+p2+p3
            D=d1+d2+d3+d4+d5
            X=s1+p1+p2+p3+d1+d2+d3+d4+d5

            s_orbital.append(S)
            p_orbital.append(P)
            d_orbital.append(D)
            PDOS.append(X)

            skip+=1

#list
list_number=[0]+number
list_number=np.array(list_number)
list_number=np.cumsum(list_number)

#txt  원상복구
old_name1 = "POSCAR.txt"
new_name1 = "POSCAR"

old_name2 = "DOSCAR.txt"
new_name2 = "DOSCAR"

os.rename(old_name1,new_name1)
os.rename(old_name2,new_name2)


os.chdir('../')
os.mkdir("Ions'_Doscar")
os.chdir("Ions'_Doscar")
for ii in (ion):
    os.mkdir(ii)

b=0
for ii in range(len(list_number)-2):
    a=1
    for jj in range(list_number[ii],list_number[ii+1]):
        plt.plot(E-Fermi_E,s_orbital[jj],label='s')
        plt.plot(E-Fermi_E,p_orbital[jj],label='p')
        plt.plot(E-Fermi_E,d_orbital[jj],label='d')
        plt.plot(E-Fermi_E,f_orbital[jj],label='f')
        plt.xlim((-5,5))
        plt.ylim((0,1))
        plt.legend()
        plt.axvline(color='k',linestyle='--')
        plt.savefig(ion[b]+str(a)+'.png')
        shutil.move(ion[b]+str(a)+'.png',ion[b])
        plt.close()
        a += 1
    b += 1
