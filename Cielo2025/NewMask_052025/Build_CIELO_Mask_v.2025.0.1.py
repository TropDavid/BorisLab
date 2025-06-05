# Build CIELO MASK FOR LN APE DEVICES
# 
#
# Confidential - do not distribute
# 28/05/2025 - David TroP, Boris Desiatov - BIU. ISRAEL

import gdspy
import numpy as np
import uuid
from cielo import *
from cielo import lib,cell_width,cells



def insert_tiles(tiles,cellname,fun, **arg):
    temp_cell = lib.new_cell(cellname)
    fun(temp_cell,**arg)
    for ii in tiles:
        top_cell.add(gdspy.CellReference(temp_cell, (cells[ii,0]+cell_width/2,cells[ii,1])))

Create_wafer_map()

x_wg_split=200
# =========================devices 2cm ============================
# devices for ELOP
# wg 

insert_tiles([0],"wgEL=0.0",Straigh,length_WG = 20000 ,x=-0,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-0)
insert_tiles([1],"wgEL=1.0",Straigh,length_WG = 20000 ,x=-0,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.0,y_pads_shift=-0)


insert_tiles([2],"wgEL=2.L",Straigh,length_WG = 20000 ,x=-x_wg_split,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-3000)
insert_tiles([2],"wgEL=2.R",Straigh,length_WG = 20000 ,x=+x_wg_split,y=0, El_length = 19000 , el_gap = 14 , el_width = 20  , Width_WG = 5.5,y_pads_shift=+2700)

insert_tiles([3],"wgEL=3.L",Straigh,length_WG = 20000 ,x=-x_wg_split,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.0,y_pads_shift=-3000)
insert_tiles([3],"wgEL=3.R",Straigh,length_WG = 20000 ,x=+x_wg_split,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.0,y_pads_shift=+2700)
# Y-split
insert_tiles([4],"wgEL=4.0",Y_splitter,Width_WG = 5.5 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 17 )
insert_tiles([5],"wgEL=5.0",Y_splitter,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 17 )
insert_tiles([6],"wgEL=6.0",Y_splitter,Width_WG = 5.5 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 17 )
insert_tiles([7],"wgEL=7.0",Y_splitter,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 17 )
insert_tiles([8],"wgEL=8.0",Y_splitter,Width_WG = 5.5 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 15 )
insert_tiles([9],"wgEL=9.0",Y_splitter,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 15 )
insert_tiles([10],"wgEL=10.0",Y_splitter,Width_WG = 5.5 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 15 )
insert_tiles([11],"wgEL=11.0",Y_splitter,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 15 )

    



# devices for BIU
# wg 

insert_tiles([12],"wgEL=12.L",Straigh,length_WG = 20000 ,x=-x_wg_split,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-3000)
insert_tiles([12],"wgEL=12.R",Straigh,length_WG = 20000 ,x=+x_wg_split,y=0, El_length = 19000 , el_gap = 17 , el_width = 20  , Width_WG = 5.0,y_pads_shift=+2700)

insert_tiles([13],"wgEL=13.L",Straigh,length_WG = 20000 ,x=-x_wg_split,y=0, El_length = 19000 , el_gap = 14 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-3000)
insert_tiles([13],"wgEL=13.R",Straigh,length_WG = 20000 ,x=+x_wg_split,y=0, El_length = 19000 , el_gap = 14 , el_width = 20  , Width_WG = 5.0,y_pads_shift=+2700)
# MZ
insert_tiles([14],"wgEL=14",MZ,A_length=5000,x=-0,y=0, El_length = 5000, el_gap = 17 , el_width = 20  , Width_WG = 5.5)
insert_tiles([15],"wgEL=15",MZ,A_length=5000,x=-0,y=0, El_length = 5000, el_gap = 17 , el_width = 20  , Width_WG = 5.0)
insert_tiles([16],"wgEL=16",MZ,A_length=5000,x=-0,y=0, El_length = 5000, el_gap = 15 , el_width = 20  , Width_WG = 5.5)
insert_tiles([17],"wgEL=17",MZ,A_length=5000,x=-0,y=0, El_length = 5000, el_gap = 15 , el_width = 20  , Width_WG = 5.0)



# Y-splitter
# 

insert_tiles([18],"wgEL=18.0",Y_splitter,Width_WG = 5.5 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 17 )
insert_tiles([19],"wgEL=19.0",Y_splitter,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 , El_length = 14000,el_gap = 15 )

# =========================devices 4cm ============================
# devices for ELOP
# wg 
# wg
insert_tiles([20],"wgEL=20.L",Straigh,length_WG = 40000 ,x=-x_wg_split,y=0, El_length = 39000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-3000)
insert_tiles([20],"wgEL=20.R",Straigh,length_WG = 40000 ,x=+x_wg_split,y=0, El_length = 39000 , el_gap = 17 , el_width = 20  , Width_WG = 5.0,y_pads_shift=+2700)

insert_tiles([21],"wgEL=21.L",Straigh,length_WG = 40000 ,x=-x_wg_split,y=0, El_length = 39000 , el_gap = 17 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-3000)
insert_tiles([21],"wgEL=21.R",Straigh,length_WG = 40000 ,x=+x_wg_split,y=0, El_length = 39000 , el_gap = 17 , el_width = 20  , Width_WG = 5.0,y_pads_shift=+2700)

insert_tiles([22],"wgEL=22.L",Straigh,length_WG = 40000 ,x=-x_wg_split,y=0, El_length = 39000 , el_gap = 15 , el_width = 20  , Width_WG = 5.5,y_pads_shift=-3000)
insert_tiles([22],"wgEL=22.R",Straigh,length_WG = 40000 ,x=+x_wg_split,y=0, El_length = 39000 , el_gap = 15 , el_width = 20  , Width_WG = 5.0,y_pads_shift=+2700)

# Y-split
# devices for ELOP

insert_tiles([23],"wgEL=23.L",Y_splitter,Width_WG = 5.5 , x = -x_wg_split*2 , y = 0 , el_width = 20 , El_length = 34000,el_gap = 17 ,A_length = 40010 - 700 - 4500)
insert_tiles([23],"wgEL=23.R",Y_splitter,Width_WG = 5.0 , x = +x_wg_split*2 , y = 0 , el_width = 20 , El_length = 34000,el_gap = 17,A_length = 40010 - 700 - 4500)

insert_tiles([24],"wgEL=24.L",Y_splitter,Width_WG = 5.5 , x = -x_wg_split*2 , y = 0 , el_width = 20 , El_length = 34000,el_gap = 17 ,A_length = 40010 - 700 - 4500)
insert_tiles([24],"wgEL=24.R",Y_splitter,Width_WG = 5.0 , x = +x_wg_split*2 , y = 0 , el_width = 20 , El_length = 34000,el_gap = 17,A_length = 40010 - 700 - 4500)

insert_tiles([25],"wgEL=25.L",Y_splitter,Width_WG = 5.5 , x = -x_wg_split*2 , y = 0 , el_width = 20 , El_length = 34000,el_gap = 15 ,A_length = 40010 - 700 - 4500)
insert_tiles([25],"wgEL=25.R",Y_splitter,Width_WG = 5.0 , x = +x_wg_split*2 , y = 0 , el_width = 20 , El_length = 34000,el_gap = 15,A_length = 40010 - 700 - 4500)

# 1x4
# devices for ELOP
insert_tiles([26],"wgEL=26.0",Splitter1X4,Width_WG = 5.5 , x = 0 , y = 0 , el_width = 20 ,el_gap = 17)
insert_tiles([27],"wgEL=27.0",Splitter1X4,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 ,el_gap = 17)
insert_tiles([28],"wgEL=28.0",Splitter1X4,Width_WG = 5.0 , x = 0 , y = 0 , el_width = 20 ,el_gap = 15)

# MZ
# single E
insert_tiles([29],"wgEL=29.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=5)
insert_tiles([29],"wgEL=29.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=5)

insert_tiles([30],"wgEL=30.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=5)
insert_tiles([30],"wgEL=30.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=5)

insert_tiles([31],"wgEL=31.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 7500, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=5)
insert_tiles([31],"wgEL=31.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 7500, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=5)

# Regular
insert_tiles([32],"wgEL=32.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([32],"wgEL=32.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=2)

insert_tiles([33],"wgEL=33.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([33],"wgEL=33.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=2)


insert_tiles([34],"wgEL=34.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 7500, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([34],"wgEL=34.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 7500, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=2)


insert_tiles([35],"wgEL=35.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([35],"wgEL=35.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=2)

insert_tiles([36],"wgEL=36.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([36],"wgEL=36.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=2)

insert_tiles([37],"wgEL=37.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 15 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([37],"wgEL=37.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 15 , el_width = 20  , Width_WG = 5.0,left_right=2)


insert_tiles([38],"wgEL=38.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([38],"wgEL=38.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 17 , el_width = 20  , Width_WG = 5.0,left_right=2)

insert_tiles([39],"wgEL=39.L",MZ,A_length= 20005 - 5002.5,x=-x_wg_split-100 ,y=0, El_length = 17000, el_gap = 15 , el_width = 20  , Width_WG = 5.5,left_right=1)
insert_tiles([39],"wgEL=39.R",MZ,A_length= 20005 - 5002.5,x=+x_wg_split+100 ,y=0, El_length = 17000, el_gap = 15 , el_width = 20  , Width_WG = 5.0,left_right=2)


exportname="Mask_Cielo_BIU_2025.v02"
lib.write_gds(exportname+'.gds')
# faltten_cell=top_cell.flatten()
# lib.write_gds(exportname+'_flattened.gds', cells=[faltten_cell])    
    
    

    
    
    
    
