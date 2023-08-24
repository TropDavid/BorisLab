# Tower test Silicon nitride chip.
# Based on Tower SIN PDK PH18
#
# Confidential - do not distribute
# 28/05/2023 - David TroP, Boris Desiatov - BIU. ISRAEL

import gdspy
import numpy as np
import uuid

from cielo import *
lib = gdspy.GdsLibrary()


wafer_radius=0.5*3*2.54*10000-100


def insert_tiles(tiles,cellname,fun, **arg):
    temp_cell = lib.new_cell(cellname)
    fun(temp_cell,**arg)
    for ii in tiles:
        top_cell.add(gdspy.CellReference(temp_cell, (cells[ii,0]+cell_width/2,cells[ii,1])))




# Load Main Mask
lib.read_gds('cielo_ELOP_Rev1.0v2.0.GDS')
top_cell=lib.cells['TOP']
num_cell = lib.cells['WG$numbers']
dicing_cell = lib.cells['Dicing']


####
# Add dicing mark to Dicing Cell
cell_width=2100
cell_height=20010
shift_x=400
shift_center_n=14
dicing_line_width=350
dicing_wafer_offset=1500
### 
# Create cell aray - (x,y) position of the cells
cells=np.zeros((shift_center_n*3*2,2))
## x lines
ii=0
for n in range(-shift_center_n,shift_center_n):
    dicing_x=n*cell_width+shift_x
    dicing_y=np.sqrt((wafer_radius-dicing_wafer_offset)**2-dicing_x**2)
    path1 = gdspy.FlexPath(width=dicing_line_width ,points= ((dicing_x,dicing_y),(dicing_x,-dicing_y)) , gdsii_path =True,**ld_SU8)    
    dicing_cell.add([path1])
    cells[ii,0]=dicing_x
    cells[ii,1]=-cell_height/2
    cells[ii+shift_center_n*2,0]=dicing_x
    cells[ii+shift_center_n*2,1]=-cell_height*3/2
    cells[ii+shift_center_n*4,0]=dicing_x
    cells[ii+shift_center_n*4,1]=cell_height*1/2
    ii+=1

## delete 5 first and last chip on row 1 and 3
cell_delete=list(range(-6,-0))+ list(range(-shift_center_n*2-5,-shift_center_n*2+5)) + list(range(-shift_center_n*4-1,-shift_center_n*4+5))
cells = np.delete(cells, [cell_delete],axis=0 )


## y lines
for n in [-3,-1,1,3]:
    dicing_y=n*cell_height/2
    dicing_x=np.sqrt((wafer_radius-dicing_wafer_offset)**2-dicing_y**2)
    path1 = gdspy.FlexPath(width=dicing_line_width ,points= ((-dicing_x,dicing_y),(dicing_x,dicing_y)) , gdsii_path =True,**ld_SU8)    
    dicing_cell.add([path1])  

## add dicing mark - metal layer 
dice_mark_cell= lib.new_cell('dice mark')
path1 = gdspy.FlexPath(width=20 ,points= ((0,115),(0,0),(115,0)) , gdsii_path =True,**ld_Metal)    
dice_mark_cell.add(path1)
for n in range(0,np.shape(cells)[0]):
    dicing_cell.add(gdspy.CellReference(dice_mark_cell, (cells[n,0]+dicing_line_width/2+30,cells[n,1]+dicing_line_width/2+30)))
    dicing_cell.add(gdspy.CellReference(dice_mark_cell,  (cells[n,0]+  cell_width - (dicing_line_width/2+30),
        cells[n,1] +dicing_line_width/2+30), rotation = 90))
    dicing_cell.add(gdspy.CellReference(dice_mark_cell,  (cells[n,0]+(dicing_line_width/2+30),
        cells[n,1]+ cell_height -(dicing_line_width/2+30)), rotation = 270))
    dicing_cell.add(gdspy.CellReference(dice_mark_cell,  (cells[n,0]+  cell_width - (dicing_line_width/2+30),
        cells[n,1]+ cell_height -(dicing_line_width/2+30)), rotation =180))

    x,y=cells[n,0]+dicing_line_width/2+300,cells[n,1]+dicing_line_width/2+1500
    label = gdspy.Label(str(n), (x,y), 'o',magnification=150,layer=32)
    arc = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_LN)
    label1 = gdspy.Label(str(n), (x,y), 'o',magnification=150,layer=29)
    arc1 = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_Metal)
    text = gdspy.Text(str(n),150, (x-100,y-100), **ld_Metal)
    text1 = gdspy.Text(str(n),150, (x-100,y-100), **ld_LN)

    num_cell.add([arc,text,arc1,text1])





# insert_tiles([1,12,14],"Spliter_Close_wg2",cielo_close_sbend,Width_WG=2)
# insert_tiles([2,33,40],"phase shifter_wg2",cielo_sbend,Width_WG=2)
# insert_tiles([33,13,11,29],"1x4_wg=2",cielo_1x4,Width_WG=2)
# insert_tiles([32,9,10,7],"1x8_wg=2",cielo1X8.cielo_1x8,Width_WG=2)
# devices for ELOP
# wg
insert_tiles([0],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 4)
insert_tiles([1],"wgEL=1",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 4.5)
insert_tiles([2],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 5)
insert_tiles([3],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 5.5)
insert_tiles([4],"wgEL=1",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 20  , Width_WG = 4)
insert_tiles([5],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 20  , Width_WG = 4.5)
insert_tiles([6],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 20  , Width_WG = 5)
insert_tiles([7],"wgEL=1",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5)
insert_tiles([8],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 15 , el_width = 20  , Width_WG = 4)
insert_tiles([9],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 15 , el_width = 20  , Width_WG = 4.5)
insert_tiles([10],"wgEL=1",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 15 , el_width = 20  , Width_WG = 5)
insert_tiles([11],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 15 , el_width = 20  , Width_WG = 5.5)
insert_tiles([12],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 20 , el_width = 200  , Width_WG = 4)
insert_tiles([13],"wgEL=1",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 20 , el_width = 200  , Width_WG = 4.5)
insert_tiles([14],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 17 , el_width = 200  , Width_WG = 5)
insert_tiles([15],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 17 , el_width = 200  , Width_WG = 5.5)





#closed Y splitters
insert_tiles([16],"Spliter_Close_16",cielo_close_sbend_old , Metal_width = 400 , diss_to_metal = 17 ,Width_WG=4)
insert_tiles([17],"Spliter_Close_17",cielo_close_sbend_old , Metal_width = 400 , diss_to_metal = 17  ,Width_WG=4.5)
insert_tiles([18],"Spliter_Close_16",cielo_close_sbend_old , Metal_width = 400 , diss_to_metal = 17  ,Width_WG=5)
insert_tiles([19],"Spliter_Close_17",cielo_close_sbend_old , Metal_width = 400 , diss_to_metal = 17  ,Width_WG=5.5)
insert_tiles([20],"Spliter_Close_16",cielo_close_sbend, Metal_width = 20 , diss_to_metal = 17  ,Width_WG=4)
insert_tiles([21],"Spliter_Close_17",cielo_close_sbend, Metal_width = 20 , diss_to_metal = 17  ,Width_WG=4.5)
insert_tiles([22],"Spliter_Close_16",cielo_close_sbend, Metal_width = 20 , diss_to_metal = 17  ,Width_WG=5)
insert_tiles([23],"Spliter_Close_17",cielo_close_sbend, Metal_width = 20 , diss_to_metal = 17  ,Width_WG=5.5)
insert_tiles([24],"Spliter_Close_16",cielo_close_sbend, Metal_width = 200 , diss_to_metal = 17   ,Width_WG=4)
insert_tiles([25],"Spliter_Close_17",cielo_close_sbend, Metal_width = 200 , diss_to_metal = 17  ,Width_WG=4.5)
insert_tiles([26],"Spliter_Close_16",cielo_close_sbend, Metal_width = 200 , diss_to_metal = 17  ,Width_WG=5)
insert_tiles([27],"Spliter_Close_17",cielo_close_sbend, Metal_width = 200 , diss_to_metal = 17  ,Width_WG=5.5)


# open Y-splitters
insert_tiles([28],"phase Spliter_Open_28",cielo_sbend, Metal_width = 20 , diss_to_metal = 17 ,Width_WG=4)
insert_tiles([29],"phase Spliter_Open_29",cielo_sbend, Metal_width = 20 , diss_to_metal = 17 ,Width_WG=4.5)
insert_tiles([30],"phase Spliter_Open_28",cielo_sbend, Metal_width = 20 , diss_to_metal = 17 ,Width_WG=5)
insert_tiles([31],"phase Spliter_Open_29",cielo_sbend, Metal_width = 20 , diss_to_metal = 17 ,Width_WG=5.5)
insert_tiles([32],"phase Spliter_Open_28",cielo_sbend_old, Metal_width = 200 , diss_to_metal = 17 ,Width_WG=4)
insert_tiles([33],"phase Spliter_Open_29",cielo_sbend_old, Metal_width = 200 , diss_to_metal = 17 ,Width_WG=4.5)
insert_tiles([34],"phase Spliter_Open_28",cielo_sbend_old, Metal_width = 200 , diss_to_metal = 17 ,Width_WG=5)
insert_tiles([35],"phase Spliter_Open_29",cielo_sbend_old, Metal_width = 200 , diss_to_metal = 17 ,Width_WG=5.5)

# 1x4 tree
insert_tiles([36],"1x4_wg=4",cielo_1x4,Width_WG=4 , C = 1)
insert_tiles([37],"1x4_wg=4",cielo_1x4,Width_WG=4.5, C = 1)
insert_tiles([38],"1x4_wg=4",cielo_1x4,Width_WG=5, C = 1)
insert_tiles([39],"1x4_wg=4",cielo_1x4,Width_WG=5.5, C = 1)
insert_tiles([40],"1x4_wg=4",cielo_1x4,Width_WG=4, C = 0)
insert_tiles([41],"1x4_wg=4",cielo_1x4,Width_WG=4.5, C = 0)
insert_tiles([42],"1x4_wg=4",cielo_1x4,Width_WG=5, C = 0)
insert_tiles([43],"1x4_wg=4",cielo_1x4,Width_WG=5.5, C = 0)


# 1x8 tree
#insert_tiles([40],"1x8_wg=4",cielo_1x8,Width_WG=4)


# devices for CIELO
# wg
insert_tiles([44+1],"wgCielo=1",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 5.5)
insert_tiles([44+3],"wgCielo=3",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 5)
insert_tiles([44+5],"wgCielo=5",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 200  , Width_WG = 5.5)
insert_tiles([44+7],"wgCielo=7",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 200  , Width_WG = 5)
insert_tiles([44+9],"wgCielo=9",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5)
insert_tiles([44+11],"wgCielo=11",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 20  , Width_WG = 5)
insert_tiles([44+13],"wgCielo=13",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 17 , el_width = 400  , Width_WG = 5.5)
insert_tiles([44+14],"wgCielo=14",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5)
insert_tiles([44+15],"wgCielo=15",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 18 , el_width = 400  , Width_WG = 5.5)
insert_tiles([44+16],"wgCielo=16",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 15000 , el_gap = 18 , el_width = 20  , Width_WG = 5.5)
# ysplitters
insert_tiles([44+2],"Spliter_Close_16",cielo_close_sbend_old , Metal_width = 400 , diss_to_metal = 17 ,Width_WG=5.5)
insert_tiles([44+4],"Spliter_Close_17",cielo_close_sbend_old , Metal_width = 400 , diss_to_metal = 17  ,Width_WG=5)
insert_tiles([44+6],"Spliter_Close_16",cielo_close_sbend_old , Metal_width = 200 , diss_to_metal = 17  ,Width_WG=5.5)
insert_tiles([44+8],"Spliter_Close_17",cielo_close_sbend_old , Metal_width = 200 , diss_to_metal = 17  ,Width_WG=5)
insert_tiles([44+10],"Spliter_Close_16",cielo_close_sbend, Metal_width = 20 , diss_to_metal = 17  ,Width_WG=5.5)
insert_tiles([44+12],"Spliter_Close_17",cielo_close_sbend, Metal_width = 20 , diss_to_metal = 17  ,Width_WG=5)



exportname="test_CIELO_02"
lib.write_gds(exportname+'.gds')
# faltten_cell=top_cell.flatten()
# lib.write_gds(exportname+'_flattened.gds', cells=[faltten_cell])    
    
    

    
    
    
    
