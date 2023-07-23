# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:41:08 2023

@author: user
"""

import gdspy
import numpy as np
import uuid


ld_NWG = {"layer": 174, "datatype": 0}
ld_Silox = {"layer": 9, "datatype": 0}
ld_taperMark = {"layer": 118, "datatype": 120}
ld_GC = {"layer": 118, "datatype": 121}
ld_SUS = {"layer": 195, "datatype": 0}
ld_VG1 = {"layer": 192, "datatype": 0}
ld_TNR = {"layer": 26, "datatype": 0}
ld_VIA1 = {"layer": 17, "datatype": 0}
ld_VIA2 = {"layer": 27, "datatype": 0}
ld_METAL2 = {"layer": 18, "datatype": 0}
ld_METAL3 = {"layer": 28, "datatype": 0}
ld_ABLB = {"layer": 118, "datatype": 53}

ld_dataExtend = {"layer": 118, "datatype": 134}

lib = gdspy.GdsLibrary()

top_cell =lib.new_cell('TOP')

def sbendPath(wgsbend,L=100,H=50,info = ld_NWG):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        y = H/2 * (1- np.cos(t*np.pi))
        x =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt = H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend   
 

def sbendPathM(wgsbend,L=100,H=50,info = ld_NWG):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        y = H/2 * (np.cos(t*np.pi))
        x =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt =  -H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend    
    



def a2r(ang):  # angle to radian
    return np.pi/180*ang


def MMI2X1 (B_length = 100 , Brad_length = 20 , Brad = 0.3 , MMI_length = 15 , MMI_width = 5 , diss_edge = 0.5 
         ,A_length = 100 , S_length = 100 , S_height = 150 , Width_WG = 1 , x = 0 , y = 0 , ld_NWG = ld_NWG , Place = 0):
    
    Center = (MMI_width - 2*diss_edge - 2*(Width_WG + Brad) + Brad )/2
    diff_in_WG = Center * 2 + Width_WG
    
    if(Place == 0): 
      yT = y + diff_in_WG 
      yB = y
      
    if(Place == 1):
      yT = y
      yB = y - diff_in_WG
      
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = (x,yT))
    #path2.segment(length = B_length , direction ="+x" , **ld_NWG)
    path2.segment(length = Brad_length , direction ="+x" , final_width = Width_WG + Brad , **ld_NWG)
    
    
    path3 = gdspy.Path( width = Width_WG + Brad ,initial_point = (x ,yB))
    #path3.segment(length = B_length , direction ="+x" , **ld_NWG)
    path3.segment(length = Brad_length , direction ="+x" , final_width = Width_WG + Brad , **ld_NWG)
    
    
    rect = gdspy.Rectangle((path3.x , Center + Width_WG/2 - MMI_width/2 ),(path2.x + MMI_length , Center + Width_WG/2 + MMI_width/2 ), **ld_NWG)
    top_cell.add(rect)
    
    path1 = gdspy.Path( width = Width_WG + Brad ,initial_point = (path2.x + MMI_length,Center + Width_WG/2))
    path1.segment(length = Brad_length , direction ="+x" , final_width = Width_WG , **ld_NWG)
    #path1.segment(length = A_length , direction ="+x" , **ld_NWG)
    
    
    
    
    
    
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    
    return([path2.x , path2.y , path3.x , path3.y])






MMI2X1()

lib.write_gds('MMI2X1.gds')