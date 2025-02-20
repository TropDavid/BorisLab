# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 12:52:15 2024

@author: user
"""
import gdspy
import numpy as np
import uuid


ld_X1 = {"layer": 2,    "datatype": 0} # 800 Nitride
ld_P1P = {"layer": 380 , "datatype":0} # Heater to X1 layer
ld_Via = {"layer": 382 , "datatype":0} # Via to Heater 
ld_P1R = {"layer": 381 , "datatype":0} # Metal layer to the X1 Heater
ld_P1Pad = {"layer": 383 , "datatype":0}
ld_X3 = {"layer":70 , "datatype":0} # 350 Nitride
ld_LNAP = {"layer": 301,    "datatype": 0} # LN Path
ld_LNAX = {"layer":302 , "datatype": 4} # LN Not 
ld_LNASIZE = {"layer": 303 , "datatype": 0} # mark of where LN is
ld_LNARFVIA = {"layer": 320 , "datatype": 0} # Conection between LN and Electrode
ld_LNARFP = {"layer": 330 , "datatype": 0} # Electrode layer
ld_LNARFPAD = {"layer": 331 , "datatype": 0} # Opening to the Electrode


lib = gdspy.GdsLibrary()
cell =lib.new_cell('Modulator_BIU')

lib.read_gds('cells.GDS')

# the notation is from left to right and the (0,0) is at the (left, middle) of the BB (So 5 overlap in required) , length of 400
Taper_end=lib.cells['ligentecInvertedTaper_w1.0BB'] 

# the notation is from left to right and the (0,0) is at the (left, middle) of the BB (So 5 overlap in required)
# width 30 , length 220 , the 1 is at center and the 2 are at +- 12.27
MMI_1X2=lib.cells['ligentecMMI1x2BB']


# the notation is from left to right and the (0,0) is at the (left, middle) of the BB (So 5 overlap in required)
# the Top and Bottom Metal are 50 width, and middle is 30 , the 2 WG are at +-19 , The Top start at 23 and the Bottom at -23
# the overall width of the BB is 156 and length is 10,752 
GSGM=lib.cells['ligentecLNA15ModulatorPushPullCbandLongBB'] 

# C_S = lib.cells['Stam']
# C_E = lib.cells['Stam-end']
padL=lib.cells['padL']
padR=lib.cells['padR']
############################################################################################################################################
#  50 micron from CHS layer if less then 100 from CSL and 10 if its more
#  X1 width 0.2 , dis 0.3
#  X3 width 0.2 , dis 0.3
#  LNAP width 2 , dis 5
#  LNAP must be enclosed by LNASIZE
#  LNARFP width 1.5, dis 3
#  LNARFP must be enclosed by LNA by 5 , lLNA = (LNASIZE NOT LNAX) OR LNAP
#  LNARFVIA width 3, dis 3
#  LNARFVIA  must be enclosed by LNARFP by 5
#  LNARFPAD width 10, dis 10
#  LNARFPAD  must be enclosed by LNARFP by 10
#  Dis between LNARFPAD and LNARFVIA is 10
############################################################################################################################################

Cell_Length = 15830
Cell_Width = 4850

WG_Width = 1
G_RF_Width = 50
S_RF_Width = 30
Taper_Length = 400
Overlap_Length = 5
MMI_Length = 220
radius_bend = 100



side = 4
dis = 4




def ViaAndPad(x = 0, y = 0,S = -1):
    k = S*(-1)
    x = x - k*(4 + 7*side +6*dis)/2
    cell.add(gdspy.Rectangle((x,y), (x +( 8 + 7*side +6*dis)*k , y + ( 8 + 7*side +6*dis)*k),**ld_P1P))
    cell.add(gdspy.Rectangle((x - 10*k,y - 2*k), (x + (8 + 7*side +6*dis + 10)*k , y + (20 + 7*side +6*dis + 70)*k ),**ld_P1R))
    cell.add(gdspy.Rectangle((x - 9*k + 3*k ,y  +( 7*side +6*dis + 15)*k + 3*k), (x - 3*k + (8 + 7*side +6*dis + 10)*k , y  +( 20 + 7*side +6*dis + 65)*k  - 3*k),**ld_P1Pad))
    
    for i in range(7):
        for j in range(7):
            cell.add(gdspy.Rectangle((x + (4 + (side+dis)*j)*k,y +( 4 + (side+dis)*i)*k), (x + (4 + (side+dis)*j + side)*k  , y + (4 + (side+dis)*i+ side)*k),**ld_Via))

def sbendPath(wgsbend,L=100,H=50,info = ld_X1):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        y = H/2 * (1- np.cos(t*np.pi))
        x =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt = H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt,dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend   
 

def sbendPathM(wgsbend,L=100,H=50,info = ld_X1):

    def sbend(t):
        y = H/2 * (np.cos(t*np.pi))
        x = L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt =  -H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt,dy_dt )

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend      


def sbendPathMBetter(wgsbend,L=100,H=50,info = ld_X1):

    def sbend(t):
        y = -(H/2 * (1- np.cos(t*np.pi)))
        x = L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt =  -H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt,dy_dt )

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend      

def a2r(ang):  # angle to radian
    return np.pi/180*ang


cell.add(gdspy.CellReference(Taper_end, (400,0) , rotation = 180))
path1 = gdspy.Path(width = WG_Width , initial_point = (Taper_Length - Overlap_Length ,0))
path1.segment(length = 1000 , direction = "+x" , **ld_X1)

cell.add(gdspy.CellReference(MMI_1X2, (path1.x,path1.y)))

pathTop = gdspy.Path(width = WG_Width , initial_point = (path1.x + MMI_Length - 10, 12.27))
pathBottom = gdspy.Path(width = WG_Width , initial_point = (path1.x + MMI_Length - 10, -12.27))

pathTop.segment(length = 100 , direction = "+x" , **ld_X1)
pathBottom.segment(length = 100 , direction = "+x" , **ld_X1)

pathTop = sbendPath(pathTop , L = 200 , H = 19 - 12.27)
pathBottom = sbendPathMBetter(pathBottom , L = 200 , H = 19 - 12.27)

pathTop.segment(length = 100 , direction = "+x" , **ld_X1)
pathBottom.segment(length = 100 , direction = "+x" , **ld_X1)

##############################################################################################################
Left_Electrode_x = pathTop.x 
Right_Electrode_x = pathTop.x + 10752 
G_Top_y = 23 + 25
G_Bottom_y = -23 - 25
S_y = 0
##############################################################################################################
#  electrodes 
# cell.add(gdspy.CellReference(C_S, (pathTop.x ,path1.y)))
cell.add(gdspy.CellReference(padL, (pathTop.x - 370,path1.y+120)))
cell.add(gdspy.CellReference(padR, (pathTop.x-2*Overlap_Length + 10752+50,path1.y+120)))


cell.add(gdspy.CellReference(GSGM, (pathTop.x ,path1.y)))
# cell.add(gdspy.CellReference(C_E, (pathTop.x-2*Overlap_Length + 10752 ,path1.y)))

pathTop.x = pathTop.x + 10752 - Overlap_Length *2
pathBottom.x = pathBottom.x + 10752 - Overlap_Length *2

pathTop.segment(length = 270 , direction = "+x" , **ld_X1)
pathBottom.segment(length = 270 , direction = "+x" , **ld_X1)

pathTop = sbendPathMBetter(pathTop , L = 200 , H = 19 - 12.27)
pathBottom = sbendPath(pathBottom , L = 200 , H = 19 - 12.27)

pathTop.segment(length = 100 , direction = "+x" , **ld_X1)
pathBottom.segment(length = 100 , direction = "+x" , **ld_X1)

########################################################################################Heaters#########################################################################
pathHTop = gdspy.Path(width = 5 , initial_point=(pathTop.x,pathTop.y))
pathHTop.turn(radius = radius_bend , angle = 'l' ,**ld_P1P)
pathHTop.turn(radius = radius_bend , angle = -np.pi , **ld_P1P)
pathHTop.turn(radius = radius_bend , angle = 'l' , **ld_P1P)

pathBackHTop = gdspy.Path(width = 5 , initial_point=(pathTop.x,pathTop.y))
pathBackHTop.segment(length = 40 , direction= "-x" , **ld_P1P)
pathBackHTop.arc(radius = 40 , initial_angle=a2r(-90) , final_angle=a2r(-180) , tolerance = 0.005 , final_width = 10 , **ld_P1P)
pathBackHTop.segment(length = 5 , direction = "+y" , **ld_P1P)

pathFrontHTop = gdspy.Path(width = 5 , initial_point=(pathHTop.x,pathHTop.y))
pathFrontHTop.arc(radius = 40 , initial_angle=a2r(-90) , final_angle=a2r(0) , tolerance = 0.005 , final_width = 10 , **ld_P1P)
pathFrontHTop.segment(length = 5 , direction = "+y" , **ld_P1P)

pathHBottom = gdspy.Path(width =5 ,initial_point= (pathBottom.x,pathBottom.y))
# pathHBottom.turn(radius = radius_bend , angle = 'r' , **ld_P1P)
# pathHBottom.segment(length = 100 , direction = "-y" , **ld_P1P)
# pathHBottom.turn(radius = radius_bend , angle = np.pi , **ld_P1P)
# pathHBottom.segment(length = 100 , direction = "+y" , **ld_P1P)
# pathHBottom.turn(radius = radius_bend , angle = 'r' , **ld_P1P)
pathHBottom.segment(length = pathHTop.x-pathHBottom.x , direction = "+x" , **ld_P1P)

pathBackHBottom = gdspy.Path(width = 5 , initial_point=(pathBottom.x,pathBottom.y))
pathBackHBottom.arc(radius = 30 , initial_angle=a2r(90) , final_angle=a2r(180) , tolerance = 0.005 , final_width = 10 , **ld_P1P)
pathBackHBottom.segment(length = 5 , direction = "-y" , **ld_P1P)

pathFrontkHBottom = gdspy.Path(width = 5 , initial_point=(pathHBottom.x,pathHBottom.y))
pathFrontkHBottom.arc(radius = 30 , initial_angle=a2r(90) , final_angle=a2r(0) , tolerance = 0.005 , final_width = 10 , **ld_P1P)
pathFrontkHBottom.segment(length = 5 , direction = "-y" , **ld_P1P)

ViaAndPad(pathBackHTop.x,pathBackHTop.y,-1)
ViaAndPad(pathFrontHTop.x,pathFrontHTop.y,-1)
ViaAndPad(pathBackHBottom.x,pathBackHBottom.y,1)
ViaAndPad(pathFrontkHBottom.x,pathFrontkHBottom.y,1)


cell.add([pathHTop,pathHBottom , pathBackHTop ,pathFrontHTop , pathBackHBottom , pathFrontkHBottom ])
#########################################################################################################################################################################

pathTop.turn(radius = radius_bend , angle = 'l' , **ld_X1)
pathTop.turn(radius = radius_bend , angle = -np.pi , **ld_X1)
pathTop.turn(radius = radius_bend , angle = 'l' , **ld_X1)

# pathBottom.turn(radius = radius_bend , angle = 'r' , **ld_X1)
# pathBottom.segment(length = 100 , direction = "-y" , **ld_X1)
# pathBottom.turn(radius = radius_bend , angle = np.pi , **ld_X1)
# pathBottom.segment(length = 100 , direction = "+y" , **ld_X1)
# pathBottom.turn(radius = radius_bend , angle = 'r' , **ld_X1)
pathBottom.segment(length = pathTop.x-pathBottom.x , direction = "+x" , **ld_X1)


pathTop.segment(length = 100 , direction = "+x" , **ld_X1)
pathBottom.segment(length = 100 , direction = "+x" , **ld_X1)

cell.add(gdspy.CellReference(MMI_1X2, (pathTop.x + 220  - 10 ,path1.y) , rotation = 180))

path1.x = pathTop.x + MMI_Length  - 2* Overlap_Length

path1.segment(length = Cell_Length - path1.x - 395 , direction = "+x" , **ld_X1)

cell.add(gdspy.CellReference(Taper_end, (path1.x - Overlap_Length ,path1.y)))


cell.add(path1)
cell.add(pathTop)
cell.add(pathBottom)



lib.write_gds('Modulator.gds')   





