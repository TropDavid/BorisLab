# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:13:57 2023

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

gap = 700





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
diss_holes_wg = 100




x = 0
y = 0

points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
tri = gdspy.Polygon(points , **ld_METAL2)
top_cell.add(tri)

points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
tri = gdspy.Polygon(points , **ld_METAL2)
top_cell.add(tri)

points = [(x- tri_diss_from_wg , y + 19000),(x  - tri_diss_from_wg , y + 19000 + tri_height),(x  - tri_diss_from_wg - tri_width , y + 19000 + tri_height)]
tri = gdspy.Polygon(points , **ld_METAL2)
top_cell.add(tri)

points = [(x - tri_diss_from_wg , y + 19000 +  tri_height),(x  - tri_diss_from_wg , y + 19000 + tri_height*2),(x  - tri_diss_from_wg - tri_width , y + 19000 + tri_height*2)]
tri = gdspy.Polygon(points , **ld_METAL2)
top_cell.add(tri)

#the start of the WG
path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
path1.segment(length = 20010 , direction ="+y" , **ld_NWG)

mid = gdspy.offset(path1 , diss_to_metal , join_first = True ,**ld_Silox)
rect = gdspy.Rectangle((x - 600 , y + 5000), (x + 600 , y + 15000), **ld_METAL2)
stam = gdspy.boolean(rect,mid,"not",**ld_METAL2)

rec = gdspy.Rectangle((path1.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path1.y/2 + 1000 - holes_height /2)
                      ,(path1.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path1.y/2 + 1000 + holes_height /2), **ld_Silox)
rect = rec.fillet(50)
top_cell.add(rect)

rec = gdspy.Rectangle((path1.x + Width_WG/2 + diss_to_metal + diss_holes_wg , path1.y/2 + 3000 - holes_height /2)
                      ,(path1.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , path1.y/2 + 3000 + holes_height /2), **ld_Silox)
rect = rec.fillet(50)
top_cell.add(rect)


top_cell.add(path1)
top_cell.add(stam)
lib.write_gds('cielo straight.gds')
























