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


# devices for ELOP
# wg
insert_tiles([0],"wgEL=0",cielo_wg,wg_length = 20000 ,x=0,y=0, el_length = 10000 , el_gap = 17 , el_width = 400  , Width_WG = 4)


exportname="Mask_Cielo_BIU_2025.v01"
lib.write_gds(exportname+'.gds')
# faltten_cell=top_cell.flatten()
# lib.write_gds(exportname+'_flattened.gds', cells=[faltten_cell])    
    
    

    
    
    
    
