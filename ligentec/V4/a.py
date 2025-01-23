import pya

# Simple script to merge three top level gds streams
#usage
# klayout -b -r make_TOP.py

layout = pya.Layout()
layout.dbu = 0.001
TOP = layout.create_cell("TOP")
gdsFiles=["Chip.gds","PC_Modulator.gds","Modulator.gds","Try_PC.gds"]
pos=[(0,0),(0,280000),(0,680000),(0,1150000)]
ind=0
for gdsF in gdsFiles:
  layout.read(gdsF)
  
  for i in layout.top_cells():
  # we don't want to insert the topcell itself
    if (i.name != "TOP"):
      print ("Adding "+i.name)
#      i.name = gdsF + "_cell"
      cell_index=i.cell_index()
#      new_instance=pya.CellInstArray(cell_index,pya.Trans(pya.Point(0,0)))
      new_instance=pya.CellInstArray(cell_index,pya.Trans(pya.Point(pos[ind][0],pos[ind][1])))
      TOP.insert(new_instance)
  ind=ind+1
layout.write("MASK_BIU.gds")