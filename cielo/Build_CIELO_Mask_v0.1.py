# Tower test Silicon nitride chip.
# Based on Tower SIN PDK PH18
#
# Confidential - do not distribute
# 28/05/2023 - David TroP, Boris Desiatov - BIU. ISRAEL

import gdspy
import numpy as np
import uuid
lib = gdspy.GdsLibrary()
lib1 = gdspy.GdsLibrary()

ld_LN = {"layer": 32, "datatype": 0}
ld_Metal = {"layer": 29, "datatype": 0}
ld_SU8 = {"layer": 50, "datatype": 0}

wafer_radius=0.5*3*2.54*10000-100

def a2r(ang):  # angle to radian
    return np.pi/180*ang




# Load Main Mask
lib.read_gds('cielo_ELOP_Rev1.0v1.0.GDS')
top_cell=lib.cells['TOP']
num_cell = lib.cells['WG$numbers']
dicing_cell = lib.cells['Dicing']


####
# Add dicing mark to Dicing Cell
cell_width=2100
cell_height=20010
shift_center_row_x= -wafer_radius-2000
shift_center_n=14
dicing_line_width=350
dicing_wafer_offset=1500
### 
# Create cell aray - (x,y) position of the cells
cells=np.zeros((shift_center_n*3*2,2))
## x lines
ii=0
for n in range(-shift_center_n,shift_center_n):
    dicing_x=n*cell_width
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

    x,y=cells[n,0]+dicing_line_width/2+600,cells[n,1]+dicing_line_width/2+1500
    label = gdspy.Label(str(n), (x,y), 'o',magnification=150,layer=32)
    arc = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_LN)
    label1 = gdspy.Label(str(n), (x,y), 'o',magnification=150,layer=29)
    arc1 = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_Metal)

    num_cell.add([label,arc])

## test cell createion 
# for n in range(0,np.shape(cells)[0]):
#     rectangle = gdspy.Rectangle((cells[n,0]-cell_width,cells[n,1] ), ((cells[n,0]+cell_width, cells[n,0]+cell_height)),layer=n+10)
#     dicing.add([rectangle]) 

# arc = gdspy.Round(
#     (0,0),
#     radius=wafer_radius,
#     inner_radius=wafer_radius-600,
#     layer=0    
# )



## populate mask with cells
lib.read_gds('cielo spliter_close.gds',rename={'TOP': 'spliter_close'})
spliter_close=lib.cells['spliter_close']
cell_to_insert=(0,1,2,3,4)
for n in cell_to_insert:
    top_cell.add(gdspy.CellReference(spliter_close, (cells[n,0]+cell_width/2,cells[n,1])))

lib.read_gds('cielo spliter.gds',rename={'TOP': 'spliter'})
spliter=lib.cells['spliter']
cell_to_insert=(10,11,12,15,16)
for n in cell_to_insert:
    top_cell.add(gdspy.CellReference(spliter, (cells[n,0]+cell_width/2,cells[n,1])))



exportname="test_CIELO_01"
lib.write_gds(exportname+'.gds')
# faltten_cell=top_cell.flatten()
# lib.write_gds(exportname+'_flattened.gds', cells=[faltten_cell])    
    
    

    
    
    
    


 
