# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:01:47 2023

@author: benne
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def earth_position(day):
    #polar equation r in AU, theta in degrees
    #approximating orbit as circular
    r=1
    rate=2*np.pi/365.25
    theta=rate*day
    return theta

def mars_position(day,theta0):
    #approximating Mars orbit as circular with a radius of 1.524 AU
    r=1.524
    rate=2*np.pi/686.98
    theta=theta0+rate*day
    return theta

def craft_position(total_days,mass,area):
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
    r_au=1
    theta=[0]
    v=0
    for d in range(int(total_days)):
        #theta unchanged from earth angular velocity
        theta.append(d*2*np.pi/365.25)
        #instantaneous acceleration
        r_m=r_au*1.496e11
        a=k/r_m**2
        v+=a*24*3600
        deltar_m=v*24*3600
        r_m+=deltar_m
        r_au=r_m/1.496e11
        rad.append(r_au)
             
    return theta,rad

def solve_conds(mass,area):
    def opt_r(x,mass,area):
        
        _,rad=craft_position(int(x),mass,area)
        return (rad[-1]-1.524)**2
    
    solvetime=minimize(opt_r,x0=100,args=(mass,area),method="Nelder-Mead")
    time_to_orbit=solvetime["x"][0]
    deltatheta=earth_position(time_to_orbit)-mars_position(time_to_orbit,0)
    return time_to_orbit,deltatheta    
  
def make_plot(mass,area):
    total_days,mars_theta0=solve_conds(mass,area)
    days=np.linspace(0,total_days)
    earth_theta=[earth_position(d) for d in days]
    earth_r=[1]*len(days)
    mars_theta=[mars_position(d,mars_theta0) for d in days]
    mars_r=[1.524]*len(days)
    
    craft_theta,craft_r=craft_position(total_days,mass,area)
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(earth_theta, earth_r,label="earth")
    ax.plot(mars_theta,mars_r,label="mars")
    ax.scatter([0,earth_theta[-1]],[1,1],marker="o",edgecolor="blue",
               color="green",s=60)
    ax.scatter([mars_theta0,mars_theta[-1]],[1.524,1.524],marker="o",edgecolor="red",
               color="red",s=40)
    ax.scatter(0,0,marker="o",s=100,color="yellow",label="sun")
    ax.plot(craft_theta,craft_r,ls=":",color="black",label="spacecraft")
    ax.legend()
    ax.set_title("Positions")
    ax.grid(False)
    ax.set_yticklabels([])
    ax.annotate("start",xy=(0,.5))
    ax.annotate(f"{total_days} days",xy=(earth_theta[-1],earth_r[-1]-.2))
    plt.savefig("orbitplot.png")
    plt.show()
    print(f"For a mass of {mass} kg and a sail area of {area} m^2")
    print(f"Transit time= {total_days:.2f} days\nMars orbit offset= {mars_theta0:.2f} radians" )
    
    
if __name__=="__main__":
    mass=20
    area=2000
    
    make_plot(mass,area)
    
    
    