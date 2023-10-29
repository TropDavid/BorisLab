# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:19:13 2023

@author: user
"""

import gdspy
import numpy as np
import uuid

ld_NWG          = {"layer": 174,    "datatype": 0}
ld_Silox        = {"layer": 9,      "datatype": 0}
ld_taperMark    = {"layer": 118,    "datatype": 120}
ld_GC           = {"layer": 118,    "datatype": 121}
ld_SUS          = {"layer": 195,    "datatype": 0}
ld_VG1          = {"layer": 192,    "datatype": 0}
ld_TNR          = {"layer": 26,     "datatype": 0}
ld_Contact      = {"layer": 7,      "datatype": 0}
ld_VIA1         = {"layer": 17,     "datatype": 0}
ld_METAL1       = {"layer": 8,      "datatype": 0}
ld_METAL2       = {"layer": 18,     "datatype": 0}
ld_dataExtend   = {"layer": 118,    "datatype": 134}
ld_holes        = {"layer": 18,     "datatype":20}

ld_ABLB = {"layer": 118, "datatype": 53}

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

'''
def Via1 (x_i = 0,y_i = 0,info = ld_VIA1 ,info_M2 = ld_METAL2, l_via1 = 0.26,dis_from_edge = 0.15,Col = 40,Row = 20):
    dis_bet_via1 = l_via1

    F_length =  dis_from_edge*2 + l_via1*40 + dis_bet_via1*39
    F_height = dis_from_edge*2 + l_via1*20 + dis_bet_via1*19
    
    M2_l = dis_from_edge*2 + l_via1*40 + dis_bet_via1*39
    M2_h = dis_from_edge*2 + l_via1*20 + dis_bet_via1*19
    
    rectM2 = gdspy.Rectangle((x_i - M2_l/2, y_i), (x_i + M2_l/2, y_i + M2_h) , **info_M2)
    top_cell.add(rectM2)
    
    x = x_i - F_length/2 + dis_from_edge
    #y = y_i + F_height + dis_from_edge
    y = y_i + dis_from_edge
    
    step = l_via1 + dis_bet_via1
    
    def Via1_1 (x = 0,y = 0, l = 0.26,info = ld_VIA1):
        rect = gdspy.Rectangle((x,y),(x+l,y+l),**ld_VIA1)
        top_cell.add(rect)
        
    
    for i in range(0,Row):
        for j in range(0,Col):
            Via1_1(x = x + step*j,y = y + step*i,l = l_via1,info = info)
'''
            
def Via (x_i = 0,y_i = 0,info_l = ld_VIA1 , info_M = ld_METAL2, l_via = 0.26 , dis_from_edge = 0.15,Col = 40,Row = 20,MN = 2):
    pad_shift=100    
    dis_bet_via = l_via
    F_length =  dis_from_edge*2 + l_via*Col + dis_bet_via*(Col -1)
    F_height = dis_from_edge*2 + l_via*Row + dis_bet_via*(Row - 1)
    
    if (MN == 2):
        rectM = gdspy.Rectangle((x_i - F_length/2, y_i), (x_i + F_length/2, y_i + F_height) , **info_M)
        top_cell.add(rectM)
        
    else:
        rectM = gdspy.Rectangle((x_i - F_length/2, y_i), (x_i + F_length/2, y_i + F_height) , **info_M)
        top_cell.add(rectM)
        rectO = gdspy.Rectangle((x_i - F_length/2, y_i + F_height), (x_i + F_length/2, y_i + F_height + pad_shift),**info_M)
        top_cell.add(rectO)
        y = y_i + F_height + pad_shift
        rectP = gdspy.Rectangle((x_i - 110/2, y), (x_i + 110/2, y + 110),**info_M)
        top_cell.add(rectP)
        
        
        # ABLB layer on pads
        rectP = gdspy.Rectangle((x_i - 110/2, y), (x_i + 110/2, y + 110),**ld_ABLB)
        top_cell.add(rectP)

        rectH = gdspy.Rectangle((x_i - 100/2, y+5), (x_i + 100/2, y + 105),**ld_Silox)
        top_cell.add(rectH)
        
        
    
    x = x_i - F_length/2 + dis_from_edge
    y = y_i + F_height - dis_from_edge
    
    step = l_via + dis_bet_via
    
    def via (x = 0,y = 0, l = 0.26,info = ld_VIA1):
        rect = gdspy.Rectangle((x,y),(x+l,y-l),**info)
        top_cell.add(rect)
        
    
    for i in range(0,Row):
        for j in range(0,Col):
            via(x = x + step*j , y = y - step*i, l = l_via , info = info_l)        







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



def MMI (B_length = 100 , Brad_length = 200 , Brad = 0.3 , MMI_length = 15 , MMI_width = 5 , diss_edge = 0.5 
         ,A_length = 430 , S_length = 1000 , S_height = 150 , Width_WG = Width_WG , x = 0 , y = 0 , Metal = 0 , start = 0 , final = 0):
    
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    if ( start == 1):
        path1 = gdspy.Path( width = 0.15 ,initial_point = (x,y))
        pathT = gdspy.Path( width = 3 ,initial_point = (x,y))
        pathT.segment(length = 150 , direction ="+x" , **ld_taperMark)
        top_cell.add(pathT)
        
    path1.segment(length = 100 , direction ="+x" , final_width = Width_WG, **ld_NWG)
    path1.segment(length = B_length , direction ="+x" , **ld_NWG)
    path1.segment(length = Brad_length , direction ="+x" , final_width = Width_WG + Brad , **ld_NWG)
    
    rect = gdspy.Rectangle((path1.x , path1.y - MMI_width/2),(path1.x + MMI_length , path1.y + MMI_width/2) , **ld_NWG)
    top_cell.add(rect)
    rect = gdspy.Rectangle((path1.x - 5, path1.y - MMI_width/2 -5 ),(path1.x + MMI_length + 5 , path1.y + MMI_width/2 + 5) , **ld_taperMark)
    top_cell.add(rect)
    
    x_1 = path1.x
    yT = y + MMI_width/2 - diss_edge - (Width_WG + Brad)/2
    yB = y - MMI_width/2 + diss_edge + (Width_WG + Brad)/2
    
    
    path2 = gdspy.Path( width = Width_WG + Brad ,initial_point = (path1.x + MMI_length ,yT))
    path2.segment(length = Brad_length , direction ="+x" , final_width = Width_WG , **ld_NWG)
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_height , info = ld_NWG)
    if Metal == 1:
        x = path2.x
        y = path2.y
        path4 = gdspy.Path(width = Width_WG ,initial_point = (x , y))
        path4.arc(radius = 10, initial_angle = a2r(270),final_angle = a2r(180),final_width = 8,**ld_TNR)
        rect = gdspy.Rectangle((path4.x - 12,path4.y), (path4.x + 12 , path4.y + 12) , **ld_TNR)
        top_cell.add(rect)
        Via(x_i = path4.x  , y_i = path4.y + 1 , info_l = ld_Contact , info_M = ld_METAL1 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
        Via(x_i = path4.x  , y_i = path4.y + 1 , info_l = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
        path5 = gdspy.Path(width = Width_WG ,initial_point = (x , y))
        path5.segment(length = A_length , direction = "+x" , **ld_TNR)
        path5.arc(radius = 10, initial_angle = a2r(270),final_angle = a2r(360),final_width = 8,**ld_TNR)
        rect = gdspy.Rectangle((path5.x - 12,path5.y), (path5.x + 12 , path5.y + 12) , **ld_TNR)
        top_cell.add(rect)
        Via(x_i = path5.x  , y_i = path5.y + 1 , info_l = ld_Contact , info_M = ld_METAL1 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
        Via(x_i = path5.x  , y_i = path5.y + 1 , info_l = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
        
        top_cell.add(path4)
        top_cell.add(path5) 
    path2.segment(length = A_length -200 , direction ="+x" , **ld_NWG)
    if( final == 1):
       path2.segment(length = 500 , direction ="+x" , **ld_NWG)
       pathT = gdspy.Path( width = 3 ,initial_point = (path2.x ,path2.y))
       path2.segment(length = 165 , direction ="+x" , final_width = 0.15 , **ld_NWG) 
       pathT.segment(length = 165 , direction ="+x" , **ld_taperMark)
       top_cell.add(pathT)
    
    
    path3 = gdspy.Path( width = Width_WG + Brad ,initial_point = (x_1 + MMI_length ,yB))
    path3.segment(length = Brad_length , direction ="+x" , final_width = Width_WG , **ld_NWG)
    path3.y = path3.y - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_NWG)
    if Metal == 1:
        x = path3.x
        y = path3.y
        path4 = gdspy.Path(width = Width_WG ,initial_point = (x , y))
        path4.arc(radius = 10, initial_angle = a2r(270),final_angle = a2r(180),final_width = 8,**ld_TNR)
        rect = gdspy.Rectangle((path4.x - 12,path4.y), (path4.x + 12 , path4.y + 12) , **ld_TNR)
        top_cell.add(rect)
        Via(x_i = path4.x  , y_i = path4.y + 1 , info_l = ld_Contact , info_M = ld_METAL1 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
        Via(x_i = path4.x  , y_i = path4.y + 1 , info_l = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
        path5 = gdspy.Path(width = Width_WG ,initial_point = (x , y))
        path5.segment(length = A_length , direction = "+x" , **ld_TNR)
        path5.arc(radius = 10, initial_angle = a2r(270),final_angle = a2r(360),final_width = 8,**ld_TNR)
        rect = gdspy.Rectangle((path5.x - 12,path5.y), (path5.x + 12 , path5.y + 12) , **ld_TNR)
        top_cell.add(rect)
        Via(x_i = path5.x  , y_i = path5.y + 1 , info_l = ld_Contact , info_M = ld_METAL1 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
        Via(x_i = path5.x  , y_i = path5.y + 1 , info_l = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
        
        top_cell.add(path4)
        top_cell.add(path5)
    
    path3.segment(length = A_length - 200 , direction ="+x" , **ld_NWG)
    if( final == 1):
       path3.segment(length = 500 , direction ="+x" , **ld_NWG) 
       pathT = gdspy.Path( width = 3 ,initial_point = (path3.x ,path3.y))
       path3.segment(length = 165 , direction ="+x" , final_width = 0.15 , **ld_NWG) 
       pathT.segment(length = 165 , direction ="+x" , **ld_taperMark)
       top_cell.add(pathT)
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    
    
    return([path2.x , path2.y , path3.x , path3.y])
    
# first
[x1 , y1 , x0 , y0] = MMI( S_length = 1000 , S_height = 700 , Metal = 1 , start = 1 )

#seond Top
[x11 , y11 , x10 ,y10 ] = MMI (x = x1 , y = y1 ,B_length = 0 ,S_length = 700 , S_height = 350 , Metal = 1)

#second Bottom
[x01 , y01 , x00 ,y00 ] = MMI (x = x0 , y = y0 ,B_length = 0 ,S_length = 700 , S_height = 350 , Metal = 1)


#third highest
[x111 , y111 , x110 ,y110 ] = MMI ( x = x11 , y = y11 , S_height = 200 ,S_length = 300,B_length = 0, Metal = 1, final = 1)

#third Mid Top
[x101 , y101 , x100 ,y100 ] = MMI ( x = x10 , y = y10 , S_height = 200 ,S_length = 300,B_length = 0, Metal = 1, final = 1)

#third Mid Bottom
[x011 , y011 , x010 ,y010 ] = MMI ( x = x01 , y = y01 , S_height = 200 ,S_length = 300,B_length = 0 , Metal = 1, final = 1)

#third Lowest
[x001 , y001 , x000 ,y000 ] = MMI ( x = x00 , y = y00 , S_height = 200 ,S_length = 300,B_length = 0 , Metal = 1, final = 1)




lib.write_gds('MMI_1X8.gds')















