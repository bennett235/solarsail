# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:23:10 2023

@author: benne
"""
import numpy as np
import matplotlib.pyplot as plt

def num_iter(mass,area,total_days):
    """
    assuming sun luminosity of 3.83E26 W/m^2
    
    no closed form solution of ode y"-k/y^2=0, so solve numerically with one day
    as the iteration step
    
    pressure= L/(4 pi r^2)
    force = 2*P*A/c
    
    """
    l=3.83e26
    k=l*area/(2*np.pi*3e8*mass)
    rad=[1]
    vel=[0]
    days=list(range(int(total_days+1)))
    r_au=1
    v=0
    for d in range(int(total_days)):
        
        r_m=r_au*1.496e11
        a=k/r_m**2
        v+=a*24*3600
        deltar_m=v*24*3600
        r_m+=deltar_m
        r_au=r_m/1.496e11
        rad.append(r_au)
        vel.append(v)
             
    return days,vel,rad

def closedform(mass,area,total_days):
    l=3.83e26
    k=l*area/(2*np.pi*3e8*mass)
    days=[range(int(total_days))]
    
    
if __name__=="__main__":
    mass=2
    area=32
    total_days=30
    iterout=num_iter(mass,area,total_days)
    plt.plot(iterout[0],iterout[1])
    plt.show()
    
    