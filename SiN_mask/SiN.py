# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:37:59 2025

@author: user
"""

import gdspy
import numpy as np
import uuid
lib = gdspy.GdsLibrary()
cell =lib.new_cell('TOP')

ld_WG = {"layer": 1,    "datatype": 0} 

def a2r(ang):  # angle to radian
    return np.pi/180*ang


def GC_my_Script(R0 = 25,period = 1.2 ,period_r = 0 ,ff0 = 0.65 ,ff_r = 0.0 ,gc_number = 20 ,sector_angle = 25 ,wg_width = 1.2 , S = 1 ,x = 0, y = 0):  
    CurrentX = R0
    CurrentPeriod = period
    CurrentFF = ff0

    for i in range(gc_number):
        GC = gdspy.Round(center = (x + R0,y), radius =  CurrentX + CurrentPeriod  
                             , inner_radius =  CurrentX + (1-CurrentFF)*CurrentPeriod ,initial_angle = a2r(-sector_angle/2) 
                             , final_angle = a2r(sector_angle/2) , tolerance = 0.0001,**ld_WG)
        CurrentX = CurrentX + CurrentPeriod
        CurrentFF = CurrentFF*(1-ff_r)
        CurrentPeriod = CurrentPeriod*(1 + period_r)
        if(S == 1):
            GC = GC.mirror((x,y + 5),(x ,y -5))
        cell.add(GC)
    
    
    Tape = gdspy.Round(center = (x+ R0,y), radius = R0 , inner_radius = 0 , initial_angle = a2r(-sector_angle/2) , final_angle = a2r(sector_angle/2), tolerance = 0.0001 , **ld_WG )
    WG = gdspy.Rectangle((x,y + wg_width/2), (x + R0 + R0/5, y - wg_width/2) , **ld_WG)
    if(S == 1):
        Tape = Tape.mirror((x,y + 5),(x ,y -5))
        WG = WG.mirror((x,y + 5),(x ,y -5))
    
    cell.add(Tape)
    cell.add(WG)
    
    # lib.write_gds('GC_Dor_code.gds')

def GC_WG_GC(R0 = 25,period = 1.001 ,period_r = 0 ,ff0 = 0.55 ,ff_r = 0.101 ,gc_number = 20 ,sector_angle = 25 ,wg_width = 2,x = 0, y = 0):
    GC_my_Script(R0 = R0,period = period,ff0 = ff0,ff_r = ff_r,gc_number=gc_number,sector_angle=sector_angle,wg_width=wg_width,S = 1,x = x,y = y)
    path = gdspy.Path(width = wg_width , initial_point = (x,y))
    path.segment(length = 100 , direction="+x" , **ld_WG)
    path.turn(radius = 100 , angle = 'l' , tolerance = 0.0001 , **ld_WG)
    path.turn(radius = 100 , angle = 'r' , tolerance = 0.0001 , **ld_WG)
    path.segment(length = 100 , direction = "+x" , **ld_WG)
    GC_my_Script(R0 = R0,period = period,ff0 = ff0,ff_r = ff_r,gc_number=gc_number,sector_angle=sector_angle,wg_width=wg_width,S = 0,x = path.x,y = path.y)
    cell.add(path)

def GC_WG_Ring_GC(Radius = 100,Gap = 0.6 ,R0 = 25,period = 1.001 ,period_r = 0 ,ff0 = 0.55 ,ff_r = 0.101 ,gc_number = 20 ,sector_angle = 25 ,wg_width = 2,x = 0, y = 0):
    GC_my_Script(R0 = R0,period = period,ff0 = ff0,ff_r = ff_r,gc_number=gc_number,sector_angle=sector_angle,wg_width=wg_width,S = 1,x = x,y = y)
    path = gdspy.Path(width = wg_width , initial_point = (x,y))
    path.segment(length =  200 , direction="+x" , **ld_WG)
    x = path.x
    y = path.y + wg_width + Gap
    path.segment(length = 150 , direction="+x" , **ld_WG)
    path.turn(radius = 100 , angle = 'l' , tolerance = 0.0001 , **ld_WG)
    path.turn(radius = 100 , angle = 'r' , tolerance = 0.0001 , **ld_WG)
    path.segment(length = 30 , direction = "+x" , **ld_WG)
    pathRing = gdspy.Path(width = wg_width , initial_point = (x,y))
    pathRing.turn(radius = Radius , angle = 'll' , tolerance = 0.0001 , **ld_WG)
    pathRing.turn(radius = Radius , angle = 'll' , tolerance = 0.0001 , **ld_WG)
    GC_my_Script(R0 = R0,period = period,ff0 = ff0,ff_r = ff_r,gc_number=gc_number,sector_angle=sector_angle,wg_width=wg_width,S = 0,x = path.x,y = path.y)
    cell.add(path)
    cell.add(pathRing)

def WG_Whole_chip(C_length = 6000, Radius = 100 , Gap = 0.6 , x = 0,y = 0 , wg_width = 1.2 ,Number = 5 , TurnAt = 2000 , Rings = 0):
    text = gdspy.Text("W = "+str(wg_width),20,(x + 500 ,y + 30) , **ld_WG)
    cell.add(text)
    text = gdspy.Text("W = "+str(wg_width),20,(x + C_length - 100 ,y+2*Radius + 30) , **ld_WG)
    cell.add(text)
    
    for i in range(0,Number):
        path = gdspy.Path(width = wg_width , initial_point = (x,y - 30*i))
        path.segment(length =  TurnAt + (2*Radius+50)*i , direction="+x" , **ld_WG)
        x1 = path.x - 25
        if(Rings ==1):
            y1 = path.y + wg_width + Gap[i]
        else:
            y1 = path.y + wg_width + Gap
            
        path.turn(radius = Radius , angle = 'l' , tolerance = 0.0001 , **ld_WG)
        path.turn(radius = Radius , angle = 'r' , tolerance = 0.0001 , **ld_WG)
        path.segment(length =  C_length - path.x , direction="+x" , **ld_WG)
        if(Rings == 1):
            pathRing = gdspy.Path(width = wg_width , initial_point = (x1,y1))
            pathRing.turn(radius = Radius , angle = 'll' , tolerance = 0.0001 , **ld_WG)
            text = gdspy.Text("G = "+str(Gap[i]),15,(pathRing.x - Radius/2 ,pathRing.y - Radius) , **ld_WG)
            cell.add(text)
            pathRing.turn(radius = Radius , angle = 'll' , tolerance = 0.0001 , **ld_WG)
            
            cell.add(pathRing)
        
        cell.add(path)
    

def GC_Ushape(R0 = 25,period = 1.05 ,period_r = 0 ,ff0 = 0.52 ,ff_r = 0 ,gc_number = 20 ,sector_angle = 25 ,wg_width = 1.2 ,x = 0, y = 0 , Radius = 100 , spacing = 127):
    GC_my_Script(R0 = R0,period = period,ff0 = ff0,ff_r = ff_r,gc_number=gc_number,sector_angle=sector_angle,wg_width=wg_width,S = 1,x = x,y = y)
    path = gdspy.Path(width = wg_width , initial_point = (x,y))
    path.segment(length =  100 , direction="+x" , **ld_WG)
    y1 = path.y
    path.arc(radius = Radius , initial_angle = a2r(-90) , final_angle = a2r(-45) , tolerance = 0.0001 , **ld_WG)
    path.arc(radius = Radius , initial_angle = a2r(135) , final_angle = a2r(90) , tolerance = 0.0001 , **ld_WG)
    dif = path.y - y1
    temp = 127 + dif*2 - 2*Radius  
    
    path.turn(radius = Radius,angle = "r" , tolerance = 0.0001 ,**ld_WG)
    path.segment(length =  temp , direction="-y" , **ld_WG)
    path.turn(radius = Radius,angle = "r" , tolerance = 0.0001 ,**ld_WG)
    
    path.arc(radius = Radius , initial_angle = a2r(-90) , final_angle = a2r(-135) , tolerance = 0.0001 , **ld_WG)
    path.arc(radius = Radius , initial_angle = a2r(45) , final_angle = a2r(90) , tolerance = 0.0001 , **ld_WG)
    path.segment(length =  100 , direction="-x" , **ld_WG)
    GC_my_Script(R0 = R0,period = period,ff0 = ff0,ff_r = ff_r,gc_number=gc_number,sector_angle=sector_angle,wg_width=wg_width,S = 1,x = path.x,y = path.y)
    cell.add(path)
    return temp
    
    
wg_width = 1.2

period = [1.1,1.15,1.2]
FF = [0.55,0.6,0.65]
Angle = 25
Gap = [0.6,0.64,0.68,0.72,0.76]
# diss_in_y_bet_angle = 50
diss_in_x_bet_FF = 60 + 300
diss_in_x_bet_Period = (60+300)*len(FF)



for j in range(0,len(Gap)):
    y = 2320
    count = 0
    text = gdspy.Text("G = "+str(Gap[j]),20,(150 + 900*j ,y + 325) , **ld_WG)
    cell.add(text)
    for k in range(0,len(period)):
        
        for i in range(0,len(FF)):
            # text = gdspy.Text("FF = "+str(FF[i]),20,(-10 + diss_in_x_bet_Period*k + diss_in_x_bet_FF*i ,y - 40) , **ld_WG)
            # cell.add(text)
            count = count + 1
         
            text = gdspy.Text(str(period[k]),20,(-130 + 900*j - 30 ,y- diss_in_x_bet_FF*i - diss_in_x_bet_Period*k + 10) , **ld_WG)
            cell.add(text)
            text = gdspy.Text(str(FF[i]),20,(-130 + 900*j -30 ,y- diss_in_x_bet_FF*i - diss_in_x_bet_Period*k  - 30) , **ld_WG)
            cell.add(text)
            GC_WG_Ring_GC(Radius = 100,Gap = Gap[j] ,R0 = 25 , period = period[k] , period_r = 0 , ff0 = FF[i] , ff_r = 0 , gc_number = 25 ,sector_angle = Angle
                          , wg_width = wg_width , x = 900*j , y = y - diss_in_x_bet_FF*i - diss_in_x_bet_Period*k )
            

WG_Whole_chip(x = -600,y = 3000 , wg_width=1.2)
WG_Whole_chip(x = -600,y = 3350 , wg_width=1.5)

WG_Whole_chip(x = -600,y = 3700 , Gap = Gap , wg_width=1.2 , Number= len(Gap) ,Rings=1)
WG_Whole_chip(x = -600,y = 4050 , Gap = Gap , wg_width=1.5 , Number= len(Gap),Rings=1)

for k in range(0,len(period)):  
    for i in range(0,len(FF)):
        text = gdspy.Text(str(period[k]),20,(4400 - 30 ,y- diss_in_x_bet_FF*i - diss_in_x_bet_Period*k + 10) , **ld_WG)
        cell.add(text)
        text = gdspy.Text(str(FF[i]),20,(4400 -30 ,y- diss_in_x_bet_FF*i - diss_in_x_bet_Period*k  - 30) , **ld_WG)
        cell.add(text)
        GC_Ushape(R0 = 25 , period = period[k] , period_r = 0 , ff0 = FF[i] , ff_r = 0 , gc_number = 25 ,sector_angle = Angle
                      , wg_width = wg_width , x = 4400 , y = y - diss_in_x_bet_FF*i - diss_in_x_bet_Period*k, Radius = 100 , spacing = 127)

for k in range(0,len(period)):  
    for i in range(0,len(FF)):
        text = gdspy.Text(str(period[k]),20,(4850 - 30 ,y- diss_in_x_bet_FF*i - diss_in_x_bet_Period*k + 10) , **ld_WG)
        cell.add(text)
        text = gdspy.Text(str(FF[i]),20,(4850 -30 ,y- diss_in_x_bet_FF*i - diss_in_x_bet_Period*k  - 30) , **ld_WG)
        cell.add(text)
        GC_Ushape(R0 = 25 , period = period[k] , period_r = 0 , ff0 = FF[i] , ff_r = 0 , gc_number = 25 ,sector_angle = Angle
                      , wg_width = 1.5 , x = 4850 , y = y - diss_in_x_bet_FF*i - diss_in_x_bet_Period*k, Radius = 100 , spacing = 127)
        


cell.add(gdspy.Rectangle((-400, 6000),(-300,5500),**ld_WG))
cell.add(gdspy.Rectangle((-600, 6000),(-500,5500),**ld_WG))

cell.add(gdspy.Rectangle((5500, 6000),(5400,5500),**ld_WG))
cell.add(gdspy.Rectangle((5700, 6000),(5600,5500),**ld_WG))

cell.add(gdspy.Rectangle((-400, -1000),(-300,-1500),**ld_WG))
cell.add(gdspy.Rectangle((-600, -1000),(-500,-1500),**ld_WG))

cell.add(gdspy.Rectangle((5500, -1000),(5400,-1500),**ld_WG))
cell.add(gdspy.Rectangle((5700, -1000),(5600,-1500),**ld_WG))


lib.write_gds("SiN.gds")