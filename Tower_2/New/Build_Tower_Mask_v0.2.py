# Tower test Silicon nitride chip.
# Based on Tower SIN PDK PH18
#
# Confidential - do not distribute
# 28/05/2023 - David TroP, Boris Desiatov - BIU. ISRAEL

import gdspy
import numpy as np
import uuid
lib = gdspy.GdsLibrary()

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
ld_PHMMI = {"layer": 118, "datatype": 164}

ld_dataExtend = {"layer": 118, "datatype": 134}



chip_length = 5000 #microns
Chip_Height = 5000 #microns
Spacing_length_at_start = 206
Spacing_Height_at_start = 206
Taper_length = 200
Taper_Width = 0.15
SUS_spacing = 0
SUS_width=70
VG_spacing=-5
VG_width=78
chip_X0, chip_Y0= -chip_length/2,-Chip_Height/2

top_cell =lib.new_cell('TOP')



    
#draw chip boundaries
chip= gdspy.Rectangle((chip_X0, chip_Y0), (chip_length+chip_X0,Chip_Height+chip_Y0 ), **ld_dataExtend)
top_cell.add(chip)

borderL= gdspy.Rectangle((chip_X0, chip_Y0-SUS_width),(chip_X0-SUS_spacing - SUS_width, Chip_Height+chip_Y0+SUS_width), **ld_SUS)
borderR= gdspy.Rectangle((chip_length+chip_X0, chip_Y0-SUS_width),(chip_length+chip_X0+SUS_spacing + SUS_width, Chip_Height+chip_Y0+SUS_width), **ld_SUS)

VGL= gdspy.Rectangle((chip_X0-VG_spacing , chip_Y0-VG_width),(chip_X0 - VG_width, Chip_Height+chip_Y0+VG_width), **ld_VG1)
VGR= gdspy.Rectangle((chip_length+chip_X0+VG_spacing , chip_Y0-VG_width),
    (chip_length+chip_X0+VG_width, Chip_Height+chip_Y0+VG_width), **ld_VG1)

top_cell.add([ borderR,borderL,VGL,VGR ])








filenames=('MMI_1X8.gds',"MMI_hanukah.gds")
cell_names=('MMI_1x8','MMI_hanukah')
cell_coord=((-2500,800),(-2500,-1500))

print(len(filenames))
for n in range(0,len(filenames)):
    lib.read_gds(filenames[n],rename={'TOP': cell_names[n]})
    tile_cell=lib.cells[cell_names[n]]      
    top_cell.add(gdspy.CellReference(tile_cell, (cell_coord[n])))






exportname="tower_chip_BIU_02"
# lib.write_gds('Rings.gds')
    
lib.write_gds(exportname+'.gds')
# faltten_cell=top_cell.flatten()
# lib.write_gds(exportname+'_flattened.gds', cells=[faltten_cell])    
    
    

    
    
