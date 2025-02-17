import pya

# Simple script to merge three top level gds streams
#usage
# klayout -b -r make_TOP.py

layout = pya.Layout()
layout.dbu = 0.005
TOP = layout.create_cell("TOP")
gdsFiles=["MASK_BIUv4.gds","HUJI_LS_mask_20250120_v03_without_frame_no_overlap.gds","HUJI_IG_V5.gds"]
pos=[(0,0),(0,-100000),(300000,183000)]
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
layout.write("MASK_BIU_HUJI_V04.gds")