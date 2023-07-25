# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 11:04:02 2023

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



Width_WG = 5
diss_to_metal = 6

gap = 500





lib = gdspy.GdsLibrary()

top_cell =lib.new_cell('TOP')

arrow_diss_down = 100
arrow_mid_height = 355
arrow_diss_sides = 100
arrow_top_height = 150
diss_arrow_from_wg = 200

tri_width = 75
tri_height = 160
tri_diss_from_wg = 50

sign_width = 20
sign_height = 130
sign_bottom = 130
sign_diss_from_wg = 720

holes_width = 280
holes_height = 1300
diss_holes_wg = 51










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




def cielo (B_length = 200 , Brad_length = 427 , Brad = 6 , A_length = 5089 , S_length = 6833 , S_height = 210 , S_height_top = 190 , Width_WG = Width_WG , x = 0 , y = 0):
    
    path4 = gdspy.Path(width = Width_WG ,initial_point = (x + S_height + gap,y))
    path4.segment(B_length*2 + Brad_length*2 + S_length*2 + A_length + 2 ,"+y" ,**ld_NWG )
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500),(x + gap - tri_diss_from_wg , y + 500 + tri_height),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500 +  tri_height),(x + gap - tri_diss_from_wg , y + 500 + tri_height*2),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)
    
    
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_NWG)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_NWG)
    
    
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_NWG)
    circle = gdspy.Round((x, y + 0.5 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_NWG ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_NWG)
    top_cell.add(stam)
    
    
    #create the arrow sign
    points = [( x - diss_arrow_from_wg , y + 1350 ),(x - diss_arrow_from_wg - arrow_diss_down , y + 1350)
              ,(x - diss_arrow_from_wg - arrow_diss_down , y + 1350 + arrow_mid_height)
              ,(x - diss_arrow_from_wg - arrow_diss_down - arrow_diss_sides , y + 1350 + arrow_mid_height)
              ,( x - diss_arrow_from_wg - arrow_diss_down/2 , y + 1350 + arrow_mid_height + arrow_top_height)
              ,(x - diss_arrow_from_wg + arrow_diss_sides , y + 1350 + arrow_mid_height)
              ,(x - diss_arrow_from_wg , y + 1350 + arrow_mid_height)]
    arrow = gdspy.Polygon(points,**ld_NWG)
    arrowM = gdspy.Polygon(points,**ld_METAL2)
    top_cell.add(arrow)
    top_cell.add(arrowM)
    
    
    
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_height_top , info = ld_NWG)
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_height_top , info = ld_NWG)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path2.y + 1000 - holes_height /2)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path2.y + 1000 + holes_height /2), **ld_Silox)
    rect = rec.fillet(50)
    top_cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg , path2.y + 3000 - holes_height /2)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , path2.y + 3000 + holes_height /2), **ld_Silox)
    rect = rec.fillet(50)
    top_cell.add(rect)
    
    path2.segment(length = A_length , direction ="+y" , **ld_NWG)
    path2.x = path2.x - S_height_top/2
    path2 = sbendPathM( wgsbend = path2 , L = S_length , H = S_height_top , info = ld_NWG)
    
    
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_NWG)
    path3.segment(length = A_length , direction ="+y" , **ld_NWG)
    path3 = sbendPath( wgsbend = path3 , L = S_length , H = S_height , info = ld_NWG)
    
    
    rect = gdspy.Rectangle(( path2.x + Width_WG/2 , path2.y ), ( path3.x - Width_WG /2 ,path3.y + 1  ),**ld_NWG)
    circle = gdspy.Round((0, path3.y), 0.5 ,initial_angle = 0 , final_angle = np.pi ,**ld_NWG ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_NWG)
    top_cell.add(stam)
    
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_Silox)
    rect = gdspy.Rectangle((x-600 , y + S_length/2), (x + 600 , y + S_length + A_length + S_length/2), **ld_METAL2)
    stam = gdspy.boolean(rect,mid,"not",**ld_METAL2)
    
    path6=gdspy.Path(50,(0,y+S_length/2-100))
    path6.segment(350,"+x",**ld_METAL2)
    path6.turn(100,a2r(90),final_width=100,**ld_METAL2)
    
    path7 = gdspy.Path(50,(0,y+S_length/2-100))
    path7.segment(350,"+x",**ld_METAL2)
    path7.turn(100,a2r(90),final_width=100,**ld_METAL2)
    path7.mirror((0,y+S_length/2+25),(0,y+S_length/2-25))
    
    
    path8=gdspy.Path(50,(0,path3.y- S_length/2 + 100))
    path8.segment(350,"+x",**ld_METAL2)
    path8.turn(100,a2r(-90),final_width=100,**ld_METAL2)
    
    path9 = gdspy.Path(50,(0,path3.y - S_length/2 + 100))
    path9.segment(350,"+x",**ld_METAL2)
    path9.turn(100,a2r(-90),final_width=100,**ld_METAL2)
    path9.mirror((0,path3.y-500+25),(0,path3.y-500-25))
    
    
    
    path5 = gdspy.Path(Width_WG + Brad ,(0,path3.y + 1))
    path5.segment(Brad_length , "+y" , final_width = Width_WG ,**ld_NWG)
    path5.segment(B_length , "+y" ,**ld_NWG)
    
    x = path5.x
    y = path5.y
    
    
    points = [(x - tri_diss_from_wg , y - 800),(x - tri_diss_from_wg , y - 800 + tri_height),(x - tri_diss_from_wg - tri_width , y - 800 + tri_height)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y - 800 +  tri_height),(x - tri_diss_from_wg , y - 800 + tri_height*2),(x - tri_diss_from_wg - tri_width , y - 800 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    top_cell.add(tri)
    
    
    
    
    
    
    
    
    
    
    
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    top_cell.add(path4)
    top_cell.add(stam)
    top_cell.add(path5)
    top_cell.add(path6)
    top_cell.add(path7)
    top_cell.add(path8)
    top_cell.add(path9)
    

    
    return([path2.x , path2.y , path3.x , path3.y])


[x1 , y1 , x0 , y0] = cielo()
lib.write_gds('cielo spliter_close.gds')