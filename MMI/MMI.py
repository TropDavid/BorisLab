# -*- coding: utf-8 -*-
"""
Created on Mon May 29 15:42:46 2023

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

Width_WG = np.array([1,0.7])
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


def a2r(ang):  # angle to radian
    return np.pi/180*ang





lib = gdspy.GdsLibrary()

top_cell =lib.new_cell('TOP')



def MMI (B_length = 100 , A_length = 100 , Body_length = 15 , Body_width = 5 , Extant = 0.3 , Extant_length = 20 
         , Width_WG = 1 , x = 0 , y = 0 , diss_from_Edge = 0.5 , Rad = 100 ):
    
    path1 = gdspy.Path(Width_WG , (x,y))
    path1.segment(length = B_length ,direction = "+x" ,**ld_NWG)
    path1.segment(length = Extant_length , direction = "+x" ,final_width = Width_WG + Extant , **ld_NWG)

    
    
    rect = gdspy.Rectangle((path1.x,path1.y - Body_width/2), (path1.x + Body_length , path1.y + Body_width/2 ),**ld_NWG)
    top_cell.add(rect) 
    
    x = path1.x + Body_length
    yT = path1.y + Body_width/2 - diss_from_Edge - (Width_WG + Extant)/2
    yB = -yT
    
    path2 = gdspy.Path(width = Width_WG + Extant ,initial_point = (x,yT))
    path2.segment(length = A_length , direction= "+x" , final_width = Width_WG , **ld_NWG)
    path2.arc(radius = Rad ,initial_angle = a2r(270) , final_angle = a2r(360),**ld_NWG)
    path2.arc(radius = Rad ,initial_angle = a2r(180) , final_angle = a2r(90),**ld_NWG)
    
    
    path3 = gdspy.Path(width = Width_WG + Extant ,initial_point = (x,yB))
    path3.segment(length = A_length , direction= "+x" , final_width = Width_WG , **ld_NWG)
    path3.arc(radius = Rad ,initial_angle = a2r(90) , final_angle = a2r(0),**ld_NWG)
    path3.arc(radius = Rad ,initial_angle = a2r(180) , final_angle = a2r(270),**ld_NWG)
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    
    return([path2.x,path2.y,path3.x,path3.y])
    
    
    
# to understan Who is What in The figure
# first
[x1 , y1 , x0 , y0] = MMI(Rad = 170)

#seond Top
[x11 , y11 , x10 ,y10 ] = MMI ( x = x1 , y = y1 , Rad = 100 )

#second Bottom
[x01 , y01 , x00 ,y00 ] = MMI ( x = x0 , y = y0 , Rad = 100 )


#third highest
[x111 , y111 , x110 ,y110 ] = MMI ( x = x11 , y = y11 , Rad = 50 )

#third Mid Top
[x101 , y101 , x100 ,y100 ] = MMI ( x = x10 , y = y10 , Rad = 50 )

#third Mid Bottom
[x011 , y011 , x010 ,y010 ] = MMI ( x = x01 , y = y01 , Rad = 50 )

#third Lowest
[x001 , y001 , x000 ,y000 ] = MMI ( x = x00 , y = y00 , Rad = 50 )




    
lib.write_gds('MMI.gds')         









