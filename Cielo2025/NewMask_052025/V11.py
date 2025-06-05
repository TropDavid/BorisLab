# -*- coding: utf-8 -*-
"""
Created on Tue May 27 16:23:54 2025

@author: user
"""

"CIELO_2025"

import gdspy
import numpy as np
import uuid

ld_NWG = {"layer": 32, "datatype": 0}
ld_LN = {"layer": 32, "datatype": 0}
ld_Silox = {"layer": 9, "datatype": 0}
ld_METAL2 = {"layer": 18, "datatype": 0}
ld_Metal = {"layer": 29, "datatype": 0}
ld_SU8 = {"layer": 50, "datatype": 0}
ld_METAL2 = {"layer": 29, "datatype": 0}
ld_NWG = {"layer": 32, "datatype": 0}
ld_Silox = {"layer": 50, "datatype": 0}

lib = gdspy.GdsLibrary()

top_cell =lib.new_cell('TOP')

Width_WG = 5
diss_bet_El = 17
diss_to_metal = (diss_bet_El - Width_WG)/2


length_WG = 20010
Metal_width = 15
Metal_length = 19000
holes_width = 280
holes_height = 1300
diss_holes_wg = 51

pads_w=280
pads_l=1300


gap = 700

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


def Tri(x = 0,y = 0):
    
    tri_width = 75
    tri_height = 160
    tri_diss_from_wg = 50
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)

    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)


def Arrow(cell,x=0,y=0):
    arrow_diss_down = 100
    arrow_mid_height = 355
    arrow_diss_sides = 100
    arrow_top_height = 150
    diss_arrow_from_wg = 200
    
    #create the arrow sign
    points = [( x - diss_arrow_from_wg , y + 500 ),(x - diss_arrow_from_wg - arrow_diss_down , y + 500)
              ,(x - diss_arrow_from_wg - arrow_diss_down , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg - arrow_diss_down - arrow_diss_sides , y + 500 + arrow_mid_height)
              ,( x - diss_arrow_from_wg - arrow_diss_down/2 , y + 500 + arrow_mid_height + arrow_top_height)
              ,(x - diss_arrow_from_wg + arrow_diss_sides , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg , y + 500 + arrow_mid_height)]
    arrow = gdspy.Polygon(points,**ld_LN)
    arrowM = gdspy.Polygon(points,**ld_Metal)
    cell.add(arrow)
    cell.add(arrowM)
    
def PadLeft(cell,x,y):
    rec = gdspy.Rectangle((x - diss_holes_wg - Width_WG/2 - diss_to_metal , y + 1000 - holes_height /2)
                          ,(x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    # rec = gdspy.Rectangle((x - diss_holes_wg - Width_WG/2 - diss_to_metal + 15 , y + 1000 - holes_height /2 - 15)
    #                       ,(x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal  - 15, y + 1000 + holes_height /2 + 15 ), **ld_Metal)
    # rect = rec.fillet(50)
    cell.add(rect)

def PadRight(cell,x,y):
    rec = gdspy.Rectangle((x + Width_WG/2 + diss_to_metal + diss_holes_wg ,y - 1000 - holes_height /2 +15)
                          ,(x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , y - 1000 + holes_height /2 - 15), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    # rec = gdspy.Rectangle((x + Width_WG/2 + diss_to_metal + diss_holes_wg - 15 , y - 1000 - holes_height /2)
    #                       ,(x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width + 15 , y - 1000 + holes_height /2), **ld_Metal)
    # rect = rec.fillet(50)
    cell.add(rect)


def Straigh (Width_WG = Width_WG,x = 0,y = 0,length_WG = length_WG , diss_to_metal = diss_to_metal,
             holes_width = 280, holes_height = 1300,diss_holes_wg = 100 , El_length = Metal_length
             ):

    Tri(x,y)
    # Tri(x,y + length_WG - 1000)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = length_WG , direction ="+y" , **ld_NWG)
    
    Tri(path1.x,path1.y - 1500)
    
    mid = gdspy.offset(path1 , diss_to_metal , join_first = True ,**ld_Silox)
    rect = gdspy.Rectangle((x - Metal_width , y + 500), (x + Metal_width , y + 500 + El_length), **ld_METAL2)
    stam = gdspy.boolean(rect,mid,"not",**ld_METAL2)
    
    
    PadLeft(top_cell,path1.x, path1.y/2)
    rec = gdspy.Rectangle((path1.x - Width_WG/2 - diss_to_metal , path1.y/2  + 1000 - holes_height/2 - 15)
                          , (path1.x - Width_WG/2 - diss_to_metal  - diss_holes_wg - holes_width , path1.y/2 + 1000 + holes_height/2 + 15)
                          ,**ld_Metal)
    top_cell.add(rec)


    PadRight(top_cell,path1.x, path1.y/2 + 3000)
    rec = gdspy.Rectangle((path1.x + Width_WG/2 + diss_to_metal , path1.y/2 +3000 - 1000 - holes_height/2)
                          , (path1.x + Width_WG/2 + diss_to_metal  + diss_holes_wg + holes_width , path1.y/2 + 3000 - 1000 + holes_height/2 )
                          ,**ld_Metal)
    top_cell.add(rec)
    
    top_cell.add(path1)
    top_cell.add(stam)


def Y_splitter (cell,B_length = 100 , Brad_length = 600 , Brad = 6 , A_length = 20010 - 700 - 4500  , S_length = 4500 , S_height = 210 
                 , S_heigth_top = 190 , Width_WG = Width_WG , x = 0 , y = 0 , Metal_width = Metal_width , diss_to_metal = diss_to_metal , El_length = 14410):
    
    # path4 = gdspy.Path(width = Width_WG ,initial_point = (x +  gap,y))
    # path4.segment(B_length + Brad_length + S_length + A_length + 501 + 173  ,"+y" ,**ld_LN )
    #Tri(x +gap,y)
    
    Tri(x,y)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    y_o = y
    
    x = path1.x
    y = path1.y
    
    # creating the half circle in the Branch of Y-splitter
    rect = gdspy.Rectangle((x + Brad/2 + Width_WG/2, y), (x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
    # adding Arrow
    Arrow(top_cell,x,y)
    
    #creating the right arm with the openings to the contacts
    path2 = gdspy.Path(width = Width_WG ,initial_point = (path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath(wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    
    #pad in the middle for joint Ground
    PadLeft(top_cell,path2.x,path2.y)
    
    x2 = path2.x
    y2 = path2.y
    
    path2.segment(length = A_length , direction ="+y" , **ld_LN)
    
    #creating the connection to the right pad
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + 15 , path2.y - 1500 - holes_height/2)
                          , (path2.x + Width_WG/2 + diss_to_metal + 15 + diss_holes_wg + holes_width , path2.y - 1500 + holes_height/2 )
                          ,**ld_Metal)
    cell.add(rec)
    
    #pad to the right of the right arm
    PadRight(top_cell, x = path2.x, y = path2.y - 500)
    
    
    #creating the left arm
    path3 = gdspy.Path(width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
   
    x3 = path3.x
    path3.segment(length = A_length , direction ="+y" , **ld_LN)
    
    #creating the middle line to connect both ground
    rec = gdspy.Rectangle((x2 - Width_WG/2 - diss_to_metal - 15 , y2 + 1000 - holes_height/2 - 50) 
                          ,(x3 + Width_WG/2 + diss_to_metal + 15 , y2 + 1000 + holes_height/2 + 50)
                          , **ld_Metal)
    cell.add(rec)
    
    
    #creating the contact
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y_o + length_WG - El_length - 500), (x + 600 , y_o + length_WG - 500), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    mid = gdspy.offset([path3,path2] , diss_to_metal + Metal_width  , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y_o + length_WG - El_length - 500), (x + 600 , y_o + length_WG - 500), **ld_Metal)
    stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
    
    # place = stam.get_bounding_box()
    # rightX = place[1,0]
    # rightY = place[1,1]
    # #leftX = place[0,0]
    
   
    
    # path7=gdspy.Path(Metal_width ,(rightX - Metal_width/2 - (S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 , rightY + 100))
    # path7.segment((S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 - 100  ,"+x",**ld_Metal)
    # path7.turn(100,a2r(-90),**ld_Metal)
   
    
    # path8=gdspy.Path(Metal_width ,(rightX - Metal_width/2 - (S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 , rightY + 100))
    # path8.segment((S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 - 100  ,"+x",**ld_Metal)
    # path8.turn(100,a2r(-90),**ld_Metal)
    # path8.mirror((-10 , rightY)
    #              ,((-10, rightY - 20)))
    
    
    
   
    # sign at the top
    Tri(path3.x,path3.y - 1500)
    
    Tri(path2.x,path2.y - 1500)
    
    #Tri(path4.x,path4.y-1000)

    # cell.add([path1,path2,path3,path4,path7,path8,stam])
    cell.add([path1,path2,path3,stam])
  
    return([path2.x , path2.y , path3.x , path3.y])

def MZ (cell,B_length = 100 , Brad_length = 400 , Brad = 6 , A_length = 10005 - 5002.5  , S_length = 4502.5 , S_height = 210 
                 , S_heigth_top = 190 , Width_WG = Width_WG , x = 0 , y = 0 , Metal_width = Metal_width , diss_to_metal = diss_to_metal , El_length = 5000):
    # path4 = gdspy.Path(width = Width_WG ,initial_point = (x +  gap,y))
    # path4.segment(B_length + Brad_length + S_length + A_length + 501 + 173  ,"+y" ,**ld_LN )
    #Tri(x +gap,y)
    
    Tri(x,y)
    Tri(x,y+length_WG - 1500)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    y_o = y
    x = path1.x
    y = path1.y
    
    # creating the half circle in the Branch of Y-splitter
    rect = gdspy.Rectangle((x + Brad/2 + Width_WG/2, y), (x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
    # adding Arrow
    Arrow(top_cell,x,y)
    
    #creating the right arm with the openings to the contacts
    path2 = gdspy.Path(width = Width_WG ,initial_point = (path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath(wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    path2.segment(length = A_length , direction ="+y" , **ld_LN)
    

    #creating the left arm
    path3 = gdspy.Path(width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
   
    x3 = path3.x
    path3.segment(length = A_length , direction ="+y" , **ld_LN)
    
    
    cell.add([path1,path2,path3,stam])
    
    #making turn Y splitter to complete the MZ
    path1m = gdspy.copy(path1).mirror(p1 = (path2.x,path2.y),p2 = (path3.x ,path2.y))
    path2m = gdspy.copy(path2).mirror(p1 = (path2.x - 5,path2.y),p2 = (path2.x+5 ,path2.y))
    path3m = gdspy.copy(path3).mirror(p1 = (path3.x - 5,path3.y),p2 = (path3.x + 5 ,path3.y))
    stam1 = gdspy.copy(stam).mirror(p1 = (path2.x,path2.y),p2 = (path3.x ,path2.y))
    
    
    
    #creating the contact
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    mid2 = gdspy.offset([path3m,path2m] , diss_to_metal  , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y_o + B_length+Brad_length+S_length), (x + 600 , y_o + B_length+Brad_length+S_length + El_length*2), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    stam = gdspy.boolean(stam,mid2,"not",**ld_Metal)
    
    
    mid = gdspy.offset([path3,path2] , diss_to_metal + Metal_width  , join_first = True ,**ld_SU8)
    mid2 = gdspy.offset([path3m,path2m] , diss_to_metal + Metal_width  , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y_o + B_length+Brad_length+S_length), (x + 600 , y_o + B_length+Brad_length+S_length + El_length*2), **ld_Metal)
    stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
    stam2 = gdspy.boolean(stam2,mid2,"not",**ld_Metal)
    
    stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
    
    
    
    # To add Pads in the design
    
    
    
    # cell.add(path1)
    cell.add([path1m,path2m,path3m,stam,stam1])
    
    
    
Straigh()
Y_splitter(top_cell,x = 3000)
MZ(top_cell,x = 10000,y=0)

lib.write_gds('V1.gds')


