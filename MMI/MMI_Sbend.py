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

chip_length = 5000 #microns
Chip_Height = 5000 #microns
Spacing_length_at_start = 200
Spacing_Height_at_start = 200
Taper_length = 200
Taper_Width = 0.15
SUS_spacing=0
SUS_width=70
VG_spacing=-4.5
VG_width=78
chip_X0, chip_Y0= -chip_length/2,-Chip_Height/2

my_length = chip_length - Spacing_length_at_start - Taper_length
my_height = Chip_Height - Spacing_Height_at_start

Width_WG = 1
gap = np.array([0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6])

Spacing_Ring_Waveguide = 20
height_in_S = 10
Rad = np.array([50,100])
Spacing_between_Straight = 30

ringHeaterWidth=3
ringHeaterSpacing=3

## Vias size
via1Size=0.26
via1Spacing=0.26
via2Size=0.5
via2Spacing=0.5
# Metal
metal1Width=10
metalLineWidth=10
padSize=100
padSpacing=150
MetalLineOffset=40








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




def MMI1X2 (B_length = 100 , Brad_length = 20 , Brad = 0.3 , MMI_length = 15 , MMI_width = 5 , diss_edge = 0.5 
         ,A_length = 100 , S_length = 100 , S_height = 150 , Width_WG = Width_WG , x = 0 , y = 0):
    
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+x" , **ld_NWG)
    path1.segment(length = Brad_length , direction ="+x" , final_width = Width_WG + Brad , **ld_NWG)
    
    rect = gdspy.Rectangle((path1.x , path1.y - MMI_width/2),(path1.x + MMI_length , path1.y + MMI_width/2) , **ld_NWG)
    top_cell.add(rect)
    
    x = path1.x
    yT = y + MMI_width/2 - diss_edge - (Width_WG + Brad)/2
    yB = y - MMI_width/2 + diss_edge + (Width_WG + Brad)/2
    
    
    print(path1.x)
    path2 = gdspy.Path( width = Width_WG + Brad ,initial_point = (path1.x + MMI_length ,yT))
    path2.segment(length = Brad_length , direction ="+x" , final_width = Width_WG , **ld_NWG)
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_height , info = ld_NWG)
    path2.segment(length = A_length , direction ="+x" , **ld_NWG)
    
    print(x)
    path3 = gdspy.Path( width = Width_WG + Brad ,initial_point = (x + MMI_length ,yB))
    path3.segment(length = Brad_length , direction ="+x" , final_width = Width_WG , **ld_NWG)
    path3.y = path3.y - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_NWG)
    path3.segment(length = A_length , direction ="+x" , **ld_NWG)
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    
    return([path2.x , path2.y , path3.x , path3.y])
    
# first
[x1 , y1 , x0 , y0] = MMI1X2()

#seond Top
[x11 , y11 , x10 ,y10 ] = MMI1X2 ( x = x1 , y = y1 , S_height = 80 )

#second Bottom
[x01 , y01 , x00 ,y00 ] = MMI1X2 ( x = x0 , y = y0 , S_height = 80 )


#third highest
[x111 , y111 , x110 ,y110 ] = MMI1X2 ( x = x11 , y = y11 , S_height = 60 )

#third Mid Top
[x101 , y101 , x100 ,y100 ] = MMI1X2 ( x = x10 , y = y10 , S_height = 60 )

#third Mid Bottom
[x011 , y011 , x010 ,y010 ] = MMI1X2 ( x = x01 , y = y01 , S_height = 60 )

#third Lowest
[x001 , y001 , x000 ,y000 ] = MMI1X2 ( x = x00 , y = y00 , S_height = 60 )

lib.write_gds('MMI_sbend.gds')






