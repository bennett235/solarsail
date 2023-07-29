# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:47:21 2023

@author: benne
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize

def sail_attitude(theta):
    """
    sail angle to the sun as a function of position in orbit   
    
    assume sun at pi radians
    
    assume sail is normal to sun from 225 to 45 degrees
    
    assume force of 1 when sail is normal, 0 otherwise

    """
    if theta>=np.pi/4 and theta<=5*(np.pi/4):
        return 0
    
    else:
        return 1
    
def sailforce(area):
    """
    calculate force on solar sail as a function of distance from sun and sail
    area (m^2)
    
    assume distance from sun = 1AU
    """
    eff=.5
   
    d_au=1
    d_meters=1.496e11*d_au
    #luminosity of sun [W]:
    lum=3.83e26
    
    #speed of light [m/s]
    c=3e8
    
    #radiation pressure
    p=lum/(4*np.pi*d_meters**2)
    
    #radiation force
    f=2*p*area/c
    
    return f*eff
    
def iterate_orbit(area=32,m=5):
    #mass of earth, kg
    M=5.97219e24
    #gravitational constant
    G=6.67430E-11
    #earth radius in km
    r_earth=6378
    #initial orbital altitude in km
    a0=720
    #initial orbital radius in m
    R0=(r_earth+a0)*1000
    #compute initial orbital velocity
    v0=(G*M/R0)**.5
    
    #mass of satellite kg

    position=pd.DataFrame(columns=["theta","r","velocity_t","velocity_r"])
    velocity_t=v0
    velocity_r=0
    radius=R0
    for i,theta in enumerate(np.linspace(0,2*np.pi,360)):
        position.loc[i,"theta"]=theta
        position.loc[i,"r"]=radius
        position.loc[i,"velocity_t"]=velocity_t
        position.loc[i,"velocity_r"]=velocity_r
        alt=radius-(r_earth*1000)
        rho_air=6e-10*np.exp((r_earth-R0/1000)/88.667)
        
        timestep=2*np.pi*radius/360/velocity_t
       
             
        f_drag=-.5*rho_air*2.2*velocity_t**2
        f_gravity=-G*m*M/(radius**2)
        f_centrifugal=m*(velocity_t**2)/radius
        
        f_sail=sailforce(area)*sail_attitude(theta)
        f_sail_t=-f_sail*np.sin(theta)
        f_sail_r=f_sail*np.cos(theta)
        
        netforce_r=f_gravity+f_centrifugal+f_sail_r
        netforce_t=f_drag+f_sail_t
        
        r_a=netforce_r/m
        t_a=netforce_t/m
        
        #new velocities with drag
        velocity_t+=t_a*timestep
        velocity_r+=r_a*timestep
        
        #new orbital radius
        
        radius+=velocity_r*timestep
       
    return position

def solve_area(m=5):
    
    def ss(a):
        orbit=iterate_orbit(area=a,m=m)
        return 1e6*(orbit["velocity_t"][0]-orbit["velocity_t"][359])**2
    
    #optarea=minimize(ss,32,method="Nelder-Mead")
    optarea=minimize(ss,32)
    print(optarea)
    return optarea["x"][0]
   
def plot_radius(df):
    plt.plot(df["theta"]/np.pi,df["r"]/1000)
    plt.xlabel("Orbit Angle [pi*radians]")
    plt.ylabel("Orbit Radius [km]")
    plt.title("Orbital Radius")
    plt.show()


if __name__=="__main__":
    position=iterate_orbit(32)
    plot_radius(position)
    
    optimal_area=solve_area()
    position_opt=iterate_orbit(optimal_area)
    plot_radius(position_opt)
    