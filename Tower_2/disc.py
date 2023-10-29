"""
Created on Tue May 23 11:58:05 2023

@author: user
"""
import gdspy
import numpy as np



def a2r(ang):  # angle to radian
    return np.pi/180*ang







lib = gdspy.GdsLibrary()
cell = lib.new_cell('TOP')

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



def Via (x_i = 0,y_i = 0,info_l = ld_VIA1 , info_M = ld_METAL2, l_via = 0.26 , dis_from_edge = 0.15,Col = 40,Row = 20,MN = 2):
    pad_shift=100    
    dis_bet_via = l_via
    F_length =  dis_from_edge*2 + l_via*Col + dis_bet_via*(Col -1)
    F_height = dis_from_edge*2 + l_via*Row + dis_bet_via*(Row - 1)
    
    if (MN == 2):
        rectM = gdspy.Rectangle((x_i - F_length/2, y_i), (x_i + F_length/2, y_i + F_height) , **info_M)
        cell.add(rectM)
        
    else:
        rectM = gdspy.Rectangle((x_i - F_length/2, y_i), (x_i + F_length/2, y_i + F_height) , **info_M)
        cell.add(rectM)
        rectO = gdspy.Rectangle((x_i - F_length/2, y_i + F_height), (x_i + F_length/2, y_i + F_height + pad_shift),**info_M)
        cell.add(rectO)
        y = y_i + F_height + pad_shift
        rectP = gdspy.Rectangle((x_i - 110/2, y), (x_i + 110/2, y + 110),**info_M)
        cell.add(rectP)
        # ABLB layer on pads

        rectP = gdspy.Rectangle((x_i - 110/2, y), (x_i + 110/2, y + 110),**ld_ABLB)
        cell.add(rectP)

        rectH = gdspy.Rectangle((x_i - 100/2, y+5), (x_i + 100/2, y + 105),**ld_Silox)
        cell.add(rectH)
        
        
    
    x = x_i - F_length/2 + dis_from_edge
    y = y_i + F_height - dis_from_edge
    
    step = l_via + dis_bet_via
    
    def via (x = 0,y = 0, l = 0.26,info = ld_VIA1):
        rect = gdspy.Rectangle((x,y),(x+l,y-l),**info)
        cell.add(rect)
        
    
    for i in range(0,Row):
        for j in range(0,Col):
            via(x = x + step*j , y = y - step*i, l = l_via , info = info_l)        



chip_length = 4800 #microns
Chip_Height = 4800 #microns
Spacing_length_at_start = 0
Spacing_Height_at_start = 0
Taper_length = 100
Taper_Width = 0.15

my_length = chip_length - Spacing_length_at_start
my_height = Chip_Height - Spacing_Height_at_start

gap = np.array([0.2
                ,0.25,0.3])

Spacing_Ring_Waveguide = 20
Rad = np.array([100])
Spacing_between_Straight = 30

Width_Waveguide = 1



for j in range(0,len(Rad)):
    Radius = Rad[j]
    Basic_Straight_step = 5*Radius + Spacing_Ring_Waveguide*3
    diss_in_bunches  = 100 + 2*Radius + 8*Spacing_between_Straight 
     
    for i in range(0,len(gap)):
        height_in_S = Radius *2
        
        path1 = gdspy.Path(Taper_Width , (-my_length/2 , my_height/2 - Spacing_between_Straight*(i)*2 - diss_in_bunches*j ))
        pathT = gdspy.Path(3 , (-my_length/2 , my_height/2 - Spacing_between_Straight*(i)*2 - diss_in_bunches*j))
            
            
    
        path1.segment(length=Taper_length,direction= "+x",final_width= Width_Waveguide ,**ld_NWG)
        pathT.segment(length=Taper_length,direction= "+x",**ld_taperMark)
        path1.segment(Basic_Straight_step*(i+1),"+x",**ld_NWG)
        x = path1.x
        y = path1.y
        path1.segment(Radius,"+x",**ld_NWG)
        path1.segment(Spacing_Ring_Waveguide,"+x",**ld_NWG)
        path1.turn(Radius,"l",**ld_NWG)
        path1.segment(height_in_S,"+y",**ld_NWG)
        path1.turn(Radius,"r",**ld_NWG)
        path1.segment(my_length - Basic_Straight_step*(i+1) - 3*Radius - Spacing_Ring_Waveguide,"+x",**ld_NWG)
        xT = path1.x
        yT = path1.y
        path1.segment(length=Taper_length,direction= "+x",final_width= Taper_Width,**ld_NWG)
    
        
        Disk =  gdspy.Round((x,y+gap[i]+Width_Waveguide+Radius), radius = Radius , **ld_NWG)
        cell.add(Disk)
        
        Disk =  gdspy.Round((x,y+gap[i]+Width_Waveguide+Radius), radius = Radius , **ld_TNR)
        cell.add(Disk)
        
        path2 = gdspy.Path(1 ,(x,y+gap[i]+Width_Waveguide+Radius))
        path2.segment(Radius + 20 , "+y" , 8 , **ld_TNR)
        stam = gdspy.Rectangle((path2.x  - 15 , path2.y - 5), (path2.x + 15 , path2.y + 15) , **ld_TNR)
        cell.add(stam)
        Via(x_i = path2.x   , y_i = path2.y  , info_l = ld_Contact , info_M = ld_METAL1 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
        Via(x_i = path2.x , y_i = path2.y  , info_l = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
        
              
        path3 = gdspy.Path(Width_Waveguide , (x + Radius , y + gap[i]*2 + Width_Waveguide*2  +2*Radius ))
        path3.segment(2*Radius , "-x" , **ld_NWG)
        path3.turn(Radius , "r" , **ld_NWG)
        path3.segment(8.5 , "+y" , **ld_NWG )
        path3.turn(Radius , "r" , **ld_NWG)
        path3.segment(my_length - Basic_Straight_step*(i+1) - Radius - Spacing_Ring_Waveguide + 220,"+x",**ld_NWG)
        x_s = path3.x
        y_s = path3.y
        path3.segment(length=Taper_length,direction= "+x",final_width= Taper_Width,**ld_NWG)
        path5 = gdspy.Path(3,(x_s,y_s))
        path5.segment(length=Taper_length,direction= "+x" ,**ld_taperMark)

        path4 = gdspy.Path(3,(xT,yT))
        path4.segment(length=Taper_length,direction= "+x" ,**ld_taperMark)
    
    
        cell.add(path1)
        cell.add(path2)
        cell.add(pathT)
        cell.add(path3)
        cell.add(path4)
        cell.add(path5)



lib.write_gds('Disc_To_Tower.gds')