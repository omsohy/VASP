import numpy as np
import matplotlib.pyplot as plt
import os

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

NEDOS=int(input("input NEDOS of your structure : "))
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
  


#total Energy 
if ISPIN2 == True:
    E_tot,Dos_tot_up,Dos_tot_down,Cum_tot_up,Cum_tot_down = np.loadtxt(doscar,skiprows=6,unpack=True,max_rows=2000)
    plt.plot(E_tot-Fermi_E,Dos_tot_up+Dos_tot_down)
    plt.xlabel('E-$E_f$(eV)')
    plt.ylabel('Density of states')
    plt.ylim((0,20))
    plt.xlim((-10,10))
    plt.axvline(x=0, color='k', linestyle='--')
  
    
else:
    E_tot,Dos_tot,Cum_tot = np.loadtxt(doscar,skiprows=6,unpack=True,max_rows=NEDOS)
    plt.plot(E_tot-Fermi_E,Dos_tot)
    plt.xlabel('E-$E_f$(eV)')
    plt.ylabel('Density of states')
    plt.ylim((0,20))
    plt.xlim((-10,10))
    plt.axvline(x=0, color='k', linestyle='--')
    plt.savefig('DOS.png')

    

#check if f orbitals are calculated

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


#total DOS
Total_dos=[]
for ii in range(1,len(list_number)):
    Total_dos.append(np.sum(PDOS[list_number[ii-1]:list_number[ii]],axis=0))
    

fig,ax=plt.subplots(len(ion)+1,1,sharex=True,figsize=(6,(len(ion)+1)*3))
for ii in range(len(ion)):
    ax[ii].plot(E-Fermi_E,Total_dos[ii],label=ion[ii])
    ax[ii].legend(prop={'size':20},loc=2)
    ax[ii].set_xlim((-10,10))
    ax[ii].set_ylim((0,3))
    ax[ii].axvline(color='k',linestyle='--')

if ISPIN2==True:
    ax[len(ion)].plot(E-Fermi_E,Dos_tot_up+Dos_tot_down,label='total' )
    ax[len(ion)].legend(prop={'size':20},loc=2)
    ax[len(ion)].set_xlim((-10,10))
    ax[len(ion)].axvline(color='k',linestyle='--')
    ax[len(ion)].set_ylim((0,25))
    ax[len(ion)].set_xlabel('E-$E_f$(eV)',fontsize=20)
    fig.tight_layout()
    plt.savefig('DOS.png')
    
else:
    ax[len(ion)].plot(E-Fermi_E,Dos_tot,label='total' )
    ax[len(ion)].legend(prop={'size':20},loc=2)
    ax[len(ion)].set_xlim((-10,10))
    ax[len(ion)].axvline(color='k',linestyle='--')
    ax[len(ion)].set_ylim((0,25))
    ax[len(ion)].set_xlabel('E-$E_f$(eV)',fontsize=20)
    fig.tight_layout()
    plt.savefig('DOS.png')


#PDOS
S_orbital=[]
P_orbital=[]
D_orbital=[]
F_orbital=[]
for ii in range(1,len(list_number)):
    S_orbital.append(np.sum(s_orbital[list_number[ii-1]:list_number[ii]],axis=0))
    P_orbital.append(np.sum(p_orbital[list_number[ii-1]:list_number[ii]],axis=0))
    D_orbital.append(np.sum(d_orbital[list_number[ii-1]:list_number[ii]],axis=0))
    if check_F==True:
        F_orbital.append(np.sum(f_orbital[list_number[ii-1]:list_number[ii]],axis=0))
    elif check_F==False:
        pass


fig,ax=plt.subplots(len(ion)+1,1,sharex=True,figsize=(6,(len(ion)+1)*3))

if check_F==True:
    for ii in range(len(ion)):
        ax[ii].plot(E-Fermi_E,S_orbital[ii],label='s')
        ax[ii].plot(E-Fermi_E,P_orbital[ii],label='p')
        ax[ii].plot(E-Fermi_E,D_orbital[ii],label='d')
        ax[ii].plot(E-Fermi_E,F_orbital[ii],label='f')
        ax[ii].legend(prop={'size':10},loc=1)
        ax[ii].set_xlim((-10,10))
        ax[ii].set_ylim((0,3))
        ax[ii].axvline(color='k',linestyle='--')
else:
        for ii in range(len(ion)):
            ax[ii].plot(E-Fermi_E,S_orbital[ii],label='s')
            ax[ii].plot(E-Fermi_E,P_orbital[ii],label='p')
            ax[ii].plot(E-Fermi_E,D_orbital[ii],label='d')
            ax[ii].legend(prop={'size':10},loc=1)
            ax[ii].set_xlim((-10,10))
            ax[ii].set_ylim((0,3))
            ax[ii].axvline(color='k',linestyle='--')


if ISPIN2==True:
    ax[len(ion)].plot(E-Fermi_E,Dos_tot_up+Dos_tot_down,label='total' )
    ax[len(ion)].legend(prop={'size':20},loc=2)
    ax[len(ion)].set_xlim((-10,10))
    ax[len(ion)].axvline(color='k',linestyle='--')
    ax[len(ion)].set_ylim((0,20))
    ax[len(ion)].set_xlabel('E-$E_f$(eV)',fontsize=20)
    fig.tight_layout()
    plt.savefig('PDOS.png')
    
else:
    ax[len(ion)].plot(E-Fermi_E,Dos_tot,label='total' )
    ax[len(ion)].legend(prop={'size':20},loc=2)
    ax[len(ion)].set_xlim((-10,10))
    ax[len(ion)].axvline(color='k',linestyle='--')
    ax[len(ion)].set_ylim((0,10))
    ax[len(ion)].set_xlabel('E-$E_f$(eV)',fontsize=20)
    fig.tight_layout()
    plt.savefig('PDOS.png')
