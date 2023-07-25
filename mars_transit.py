# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:49:16 2023

@author: benne
"""
import numpy as np
import matplotlib.pyplot as plt
"""
compute acceleration and velocity of body transiting from earth to mars,
propelled by a solar sail

solar luminosity: 3.83E26 W
distance traveled: 1 to 1.524 au

"""

def force(a_msq,d_au):
    """
    calculate force on solar sail as a function of distance from sun and sail
    area
    """
    d_meters=1.496e11*d_au
    #luminosity of sun [W]:
    lum=3.83e26
    
    #speed of light [m/s]
    c=3e8
    
    #radiation pressure
    p=lum/(4*np.pi*d_meters**2)
    
    #radiation force
    f=2*p*a_msq/c
    
    return f

def plot_acc(mass,area):
    """
    plot instantaneous acceleration vs. distance from sun
    """
    d_vals=np.linspace(1,1.6)
    a=[force(area,d)/mass for d in d_vals]
    
    plt.plot(d_vals,a,label="acceleration")
    plt.axvline(1,label="Earth",ls=":",color="black")
    plt.annotate("Earth",xy=(1,.0001),xytext=(1.05,.00008),
                 arrowprops={"width":2,"headwidth":6,'headlength':6})
    
    plt.axvline(1.524,label="Mars",ls=":",color="black")
    plt.annotate("Mars",xy=(1.524,.0001),xytext=(1.3,.00012),
                 arrowprops={"width":2,"headwidth":6,'headlength':6})
    plt.xlim(.9,1.6)
    plt.title("Instantaneous Acceleration")
    plt.xlabel("Distance from Sun [AU]")
    plt.ylabel("Acceleration [m/s$^2$]")
    
    plt.annotate(f"sail area= {area} m$^2$\n mass= {mass} kg",xy=(.5,.85),
                 xycoords="axes fraction")
    plt.savefig("accinst.png")
    plt.show()
    
def plot_vel(mass,area):
    const=3.83E26*area/(2*np.pi*3E8*area)
    
    plt.show()
    
      
if __name__=="__main__":
    plot_acc(2,32)
    
    print(plot_vel(2,32))
    