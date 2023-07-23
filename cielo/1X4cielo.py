# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:59:13 2023

@author: LUM
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



Width_WG = 5
diss_to_metal = 6
Metal_width = 1000

gap = 700





lib = gdspy.GdsLibrary()

top_cell =lib.new_cell('TOP')







def sbendPath(wgsbend,L=100,H=50,info = ld_NWG):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        x = H/2 * (1- np.cos(t*np.pi))
        y =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dx_dt = H/2*np.pi*np.sin(t*np.pi)
        dy_dt = L

        return (dx_dt,dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend   
 

def sbendPathM(wgsbend,L=100,H=50,info = ld_NWG):

    def sbend(t):
        x = H/2 * (np.cos(t*np.pi))
        y = L*t
        
        return (x,y)
    
    def dtsbend(t):
        dx_dt =  -H/2*np.pi*np.sin(t*np.pi)
        dy_dt = L

        return (dx_dt,dy_dt )

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend    
    



def a2r(ang):  # angle to radian
    return np.pi/180*ang




def cielo (B_length = 1750 , Brad_length = 426 , Brad = 6 , A_length = 12220 , S_length = 6833 , S_height = 210 , S_heigth_top = 190 
           , Width_WG = Width_WG ,M_width = Metal_width  , x = 0 , y = 0):
    """
    path4 = gdspy.Path(width = Width_WG ,initial_point = (x + S_height + gap,y))
    path4.segment(B_length + Brad_length + S_length + A_length + 1  ,"+y" ,**ld_NWG )
    """
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_NWG)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_NWG)
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_NWG)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_NWG ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_NWG)
    top_cell.add(stam)
    
    
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_NWG)
    path2.segment(length = A_length , direction ="+y" , **ld_NWG)
    
    
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_NWG)
    path3.segment(length = A_length , direction ="+y" , **ld_NWG)
    
    
    
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_Silox)
    rect = gdspy.Rectangle((x - M_width/2 , y + S_length/5), (x + M_width/2 , y + S_length + A_length), **ld_METAL2)
    stam = gdspy.boolean(rect,mid,"not",**ld_METAL2)
    
    
    
    
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    #top_cell.add(path4)
    top_cell.add(stam)

    
    return([path2.x , path2.y , path3.x , path3.y])

   
# first
[x1 , y1 , x0 , y0] = cielo()

#seond Top
[x11 , y11 , x10 ,y10 ] = cielo ( x = x1 , y = y1 , S_height = 60 , S_heigth_top = 50 , M_width = 300)

#second Bottom
[x01 , y01 , x00 ,y00 ] = cielo ( x = x0 , y = y0, S_height = 60 , S_heigth_top = 50 , M_width = 300)

"""
#third highest
[x111 , y111 , x110 ,y110 ] = MMI1X2 ( x = x11 , y = y11 , S_height = 60 )

#third Mid Top
[x101 , y101 , x100 ,y100 ] = MMI1X2 ( x = x10 , y = y10 , S_height = 60 )

#third Mid Bottom
[x011 , y011 , x010 ,y010 ] = MMI1X2 ( x = x01 , y = y01 , S_height = 60 )

#third Lowest
[x001 , y001 , x000 ,y000 ] = MMI1X2 ( x = x00 , y = y00 , S_height = 60 )
"""



lib.write_gds('cielo spliter1X4.gds')




